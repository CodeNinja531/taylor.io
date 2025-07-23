import os

def capitalize_first_letter_of_txt_files():
    """
    Renames all .txt files in the current directory,
    capitalizing the first letter of each filename.
    """
    current_directory = os.getcwd() # Get the current working directory
    print(f"Scanning directory: {current_directory}")

    # Iterate over all files in the current directory
    for filename in os.listdir(current_directory):
        # Check if the file is a .txt file and is actually a file (not a directory)
        if filename.endswith(".txt") and os.path.isfile(os.path.join(current_directory, filename)):
            # Get the base name and extension separately
            base_name, extension = os.path.splitext(filename)

            # Check if the base name is not empty
            if base_name:
                # Capitalize the first letter of the base name
                new_base_name = base_name[0].upper() + base_name[1:]
                new_filename = new_base_name + extension

                # Construct full paths for old and new filenames
                old_filepath = os.path.join(current_directory, filename)
                new_filepath = os.path.join(current_directory, new_filename)

                # Check if the new filename is different from the old one to avoid unnecessary renames
                if old_filepath != new_filepath:
                    try:
                        os.rename(old_filepath, new_filepath)
                        print(f"Renamed '{filename}' to '{new_filename}'")
                    except OSError as e:
                        print(f"Error renaming '{filename}': {e}")
                else:
                    print(f"'{filename}' is already capitalized or has an empty base name, skipping.")
            else:
                print(f"Skipping '{filename}' as its base name is empty.")
    print("Renaming process complete.")

# Call the function to execute the renaming process
if __name__ == "__main__":
    capitalize_first_letter_of_txt_files()
