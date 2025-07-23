import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk # For themed widgets, especially for Treeview or better Listbox if needed

class FileReordererApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Reorderer")
        self.root.geometry("600x500") # Set a default window size
        self.root.resizable(True, True) # Allow resizing

        self.current_directory = os.getcwd()
        self.txt_files = [] # Stores original file names
        self.display_files = [] # Stores file names for display (can be reordered)

        self.create_widgets()
        self.load_txt_files()

    def create_widgets(self):
        # Frame for directory path and change button
        dir_frame = tk.Frame(self.root, padx=10, pady=10)
        dir_frame.pack(fill=tk.X)

        self.dir_label = tk.Label(dir_frame, text=f"Current Directory: {self.current_directory}", wraplength=550)
        self.dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        change_dir_button = tk.Button(dir_frame, text="Change Directory", command=self.change_directory)
        change_dir_button.pack(side=tk.RIGHT, padx=5)

        # Frame for the listbox and scrollbar
        list_frame = tk.Frame(self.root, padx=10, pady=5)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, font=('Arial', 10))
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the listbox
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # Bind drag-and-drop events
        self.file_listbox.bind('<Button-1>', self.on_listbox_click)
        self.file_listbox.bind('<B1-Motion>', self.on_listbox_drag)
        self.file_listbox.bind('<ButtonRelease-1>', self.on_listbox_release)

        # Frame for action buttons
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.pack(fill=tk.X)

        rename_button = tk.Button(button_frame, text="Rename Files", command=self.rename_files)
        rename_button.pack(side=tk.RIGHT, padx=5)

        # Add a refresh button
        refresh_button = tk.Button(button_frame, text="Refresh Files", command=self.load_txt_files)
        refresh_button.pack(side=tk.LEFT, padx=5)

        # Drag-and-drop state variables
        self._drag_data = {"item": None, "index": -1}

    def on_listbox_click(self, event):
        """Records the item being dragged."""
        try:
            index = self.file_listbox.nearest(event.y)
            self._drag_data["item"] = self.file_listbox.get(index)
            self._drag_data["index"] = index
        except IndexError:
            self._drag_data = {"item": None, "index": -1} # Reset if click is outside items

    def on_listbox_drag(self, event):
        """Handles the dragging motion to reorder items."""
        if self._drag_data["item"] is None:
            return

        try:
            current_index = self.file_listbox.nearest(event.y)
            drag_index = self._drag_data["index"]

            if current_index != drag_index:
                # Move the item in the display_files list
                item_to_move = self.display_files.pop(drag_index)
                self.display_files.insert(current_index, item_to_move)

                # Update the listbox display
                self.update_listbox_display()

                # Select the moved item to keep it highlighted
                self.file_listbox.selection_set(current_index)
                self._drag_data["index"] = current_index # Update drag index

        except IndexError:
            pass # Ignore if dragging outside valid listbox area

    def on_listbox_release(self, event):
        """Resets drag state after release."""
        self._drag_data = {"item": None, "index": -1}

    def load_txt_files(self):
        """Loads .txt files from the current directory into the listbox."""
        self.file_listbox.delete(0, tk.END) # Clear existing items
        self.txt_files = [] # Reset original files
        self.display_files = [] # Reset display files

        try:
            for filename in os.listdir(self.current_directory):
                if filename.lower().endswith(".txt") and os.path.isfile(os.path.join(self.current_directory, filename)):
                    self.txt_files.append(filename)
            self.txt_files.sort() # Sort alphabetically by default

            # Initialize display_files with the sorted original files
            self.display_files = list(self.txt_files) # Create a copy

            self.update_listbox_display()

            if not self.txt_files:
                messagebox.showinfo("No Files", "No .txt files found in this directory.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read directory: {e}")

    def update_listbox_display(self):
        """Updates the Listbox widget with the current contents of display_files."""
        self.file_listbox.delete(0, tk.END)
        for i, filename in enumerate(self.display_files):
            self.file_listbox.insert(tk.END, f"{i+1}. {filename}")

    def change_directory(self):
        """Allows the user to select a new directory."""
        new_directory = filedialog.askdirectory(initialdir=self.current_directory)
        if new_directory:
            self.current_directory = new_directory
            self.dir_label.config(text=f"Current Directory: {self.current_directory}")
            self.load_txt_files()

    def rename_files(self):
        """Renames the files based on the order in the listbox."""
        if not self.display_files:
            messagebox.showinfo("No Files", "No files to rename.")
            return

        confirm = messagebox.askyesno(
            "Confirm Rename",
            "Are you sure you want to rename these files based on the current order?\n"
            "This action cannot be undone."
        )
        if not confirm:
            return

        try:
            # Create a mapping from current display order to original names
            # This is crucial because display_files has been reordered,
            # but we need to rename the *original* files.
            # We assume display_files still contains the original names, just in a new order.

            renamed_count = 0
            for i, new_filename_base in enumerate(self.display_files):
                # Ensure we are not trying to rename a file that was already renamed in this session
                # This simple check assumes the original filenames don't start with "X. "
                # A more robust solution might involve storing original paths or using a temporary prefix.
                if new_filename_base.startswith(f"{i+1}. "):
                    # This file has already been processed or is incorrectly named
                    continue

                original_path = os.path.join(self.current_directory, new_filename_base)
                new_name = f"{i+1}. {new_filename_base}"
                new_path = os.path.join(self.current_directory, new_name)

                if os.path.exists(original_path):
                    os.rename(original_path, new_path)
                    renamed_count += 1
                else:
                    messagebox.showwarning("File Not Found", f"Original file '{new_filename_base}' not found. Skipping.")

            messagebox.showinfo("Renaming Complete", f"Successfully renamed {renamed_count} files.")
            self.load_txt_files() # Reload files to show new names
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during renaming: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileReordererApp(root)
    root.mainloop()
