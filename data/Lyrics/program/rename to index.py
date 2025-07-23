import os
import re

def rename_files_sequentially():
    """
    Renames files in the current directory from the format "NUMBER. ANY_TEXT.txt"
    to "NUMBER.txt".
    """
    # Get the current working directory where the script is executed.
    directory = os.getcwd()
    print(f"Scanning directory: {directory}\n")

    # Compile a regular expression pattern to match the desired file names.
    # Explanation of the pattern:
    # ^          : Asserts position at the start of the string.
    # (\d+)      : Captures one or more digits (this will be our 'NUMBER').
    # \.         : Matches a literal dot (the one after the number).
    # .* : Matches any character (except for line terminators) zero or more times
    #              (this is the 'ANY_TEXT' part).
    # \.txt$     : Matches a literal '.txt' at the end of the string.
    # re.IGNORECASE: Makes the matching case-insensitive for the '.txt' extension.
    pattern = re.compile(r'^(\d+)\..*\.txt$', re.IGNORECASE)

    renamed_count = 0 # Counter for successfully renamed files

    # Iterate over all entries (files and directories) in the current directory.
    for filename in os.listdir(directory):
        # Construct the full path for the current file/directory.
        old_filepath = os.path.join(directory, filename)

        # Check if the current entry is actually a file (and not a directory or symlink).
        if os.path.isfile(old_filepath):
            # Attempt to match the filename against our defined pattern.
            match = pattern.match(filename)
            if match:
                # If a match is found, extract the captured number (group 1 from the regex).
                file_number = match.group(1)
                # Construct the new desired filename.
                new_filename = f"{file_number}.txt"
                # Construct the full new path.
                new_filepath = os.path.join(directory, new_filename)

                # Check if the old and new file paths are already the same.
                # This prevents unnecessary operations if a file is already in the target format.
                if old_filepath == new_filepath:
                    print(f"Skipping '{filename}' as it's already in the target format.")
                    continue # Move to the next file

                try:
                    # Attempt to rename the file.
                    os.rename(old_filepath, new_filepath)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                    renamed_count += 1 # Increment the counter
                except OSError as e:
                    # Catch and print any OS-related errors during renaming (e.g., permission denied, file in use).
                    print(f"Error renaming '{filename}': {e}")
            else:
                # If the filename does not match the pattern, inform the user.
                print(f"Skipping '{filename}' as it does not match the expected pattern.")
        else:
            # If the entry is not a file (e.g., a directory), inform the user.
            print(f"Skipping '{filename}' as it is a directory.")

    print(f"\n--- Renaming process complete. Renamed {renamed_count} files. ---")

rename_files_sequentially()
