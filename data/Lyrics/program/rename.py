import os
import re

def add_spaces_before_caps(text):
    """
    Adds a space before each capital letter in a string,
    except for the very first letter.
    Example: "HowYouGetTheGirl" -> "How You Get The Girl"
    """
    # Use a regex to find uppercase letters that are not at the beginning of the string
    # and replace them with a space followed by the letter.
    # This handles cases like "HowYou" -> "How You"
    # It also handles "TheGirl" -> "The Girl"
    # Ensure it doesn't add a space if the previous character is already a space
    s1 = re.sub(r'([A-Z])', r' \1', text)
    # Remove any double spaces that might result from the above
    s2 = re.sub(r'\s+', ' ', s1).strip()
    return s2

def process_filename(filename):
    """
    Processes a filename to remove specific strings and add spaces before capitals.
    """
    name_part, ext_part = os.path.splitext(filename)
    original_name_part = name_part

    # Convert to lowercase for checking, but work with original for replacement
    lower_name_part = name_part.lower()

    # 1. Remove "_FromTheVault_" (case-insensitive)
    string_from_the_vault = "_fromthevault_"
    if string_from_the_vault in lower_name_part:
        start_index = lower_name_part.find(string_from_the_vault)
        end_index = start_index + len(string_from_the_vault)
        name_part = name_part[:start_index] + name_part[end_index:]
        lower_name_part = name_part.lower() # Update lower_name_part after modification

    # 2. Remove "_TaylorsVersion_" (case-insensitive)
    string_taylors_version = "_taylorsversion_"
    if string_taylors_version in lower_name_part:
        start_index = lower_name_part.find(string_taylors_version)
        end_index = start_index + len(string_taylors_version)
        name_part = name_part[:start_index] + name_part[end_index:]
        lower_name_part = name_part.lower() # Update lower_name_part after modification

    # Note: The "Embed" removal from the filename was moved to clean_file_content as per user's clarification.
    # This section now only handles _FromTheVault_ and _TaylorsVersion_ removal from filename.

    # 3. Add spaces before all capital letters (except the first)
    # First, remove any remaining underscores to avoid them interfering with capitalization logic
    name_part = name_part.replace("_", "")
    
    # Apply the spacing logic
    final_name_part = add_spaces_before_caps(name_part).strip()

    # Ensure the first letter is capitalized if it's not already
    if final_name_part:
        final_name_part = final_name_part[0].upper() + final_name_part[1:]

    return final_name_part + ext_part if final_name_part else ""


def clean_file_content(filepath):
    """
    Removes all characters before and including the word 'Lyrics'
    (case-insensitive) from the content of a file.
    Also removes 'Embed' and any preceding integer from the end of the content.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content_length = len(content)

        # 1. Remove 'Embed' and preceding integer from the end of the content
        # This regex matches an optional group of one or more digits (\d+)? followed by 'Embed'
        # and optional whitespace (\s*) at the very end of the string ($).
        # It's case-insensitive.
        content = re.sub(r'\s*(\d+)?Embed\s*$', '', content, flags=re.IGNORECASE)
        if len(content) < original_content_length:
            print(f"    Content: Removed 'Embed' pattern from end.")
            
        # 2. Remove all characters before and including the word 'Lyrics'
        lower_content = content.lower()
        lyrics_keyword = "lyrics"
        index = lower_content.find(lyrics_keyword)

        if index != -1:
            # Extract the part of the string after 'Lyrics'
            new_content = content[index + len(lyrics_keyword):]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"    Content: Removed prefix before 'Lyrics'.")
            return True
        else:
            # If 'Lyrics' not found, just write back the content after 'Embed' removal
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"    Content: 'Lyrics' not found. Only 'Embed' removal (if any) applied.")
            return False
    except Exception as e:
        print(f"    Content: Error processing content: {e}")
        return False

def batch_process_files():
    """
    Main function to process all .txt files in the current directory:
    renames them and cleans their content.
    """
    current_directory = os.getcwd()
    print(f"Starting batch processing in: {current_directory}")

    for filename in os.listdir(current_directory):
        if filename.endswith(".txt"):
            old_filepath = os.path.join(current_directory, filename)
            
            print(f"\nProcessing file: {filename}")

            # --- Step 1: Process Filename ---
            new_filename = process_filename(filename)
            
            if new_filename and new_filename != filename:
                new_filepath = os.path.join(current_directory, new_filename)
                try:
                    os.rename(old_filepath, new_filepath)
                    print(f"  Renamed '{filename}' to '{new_filename}'.")
                    # Update old_filepath to the new path for content cleaning
                    old_filepath = new_filepath 
                    filename = new_filename # Update filename for subsequent prints
                except OSError as e:
                    print(f"  Error renaming '{filename}' to '{new_filepath}': {e}")
                    # If rename fails, continue to content cleaning with original path
            elif not new_filename:
                print(f"  Skipping rename: New filename for '{filename}' is empty.")
            else:
                print(f"  Filename: No renaming needed for '{filename}'.")

            # --- Step 2: Clean File Content ---
            clean_file_content(old_filepath) # Use the potentially new path


        else:
            print(f"\nSkipping non-.txt file: {filename}")

if __name__ == "__main__":
    batch_process_files()
    print("\nBatch processing complete.")
