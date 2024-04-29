import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar


class ProfileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Profile Manager")

        # Sample profile IDs (you can replace this with actual data fetching logic)
        self.profile_ids = ['profile1', 'profile2', 'profile3', 'profile4']

        # Create a button to fetch all profiles
        self.fetch_button = tk.Button(root, text="取所有profile", command=self.fetch_profiles)
        self.fetch_button.pack(pady=10)

        # Create a frame for the listbox and scrollbar
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        # Create a listbox to display profile IDs
        self.listbox = Listbox(self.frame, width=50, height=20)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind double-click event to open the selected profile
        self.listbox.bind('<Double-1>', self.open_profile)

        # Create a scrollbar for the listbox
        self.scrollbar = Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link the scrollbar to the listbox
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

    def fetch_profiles(self):
        # Clear existing entries in the listbox
        self.listbox.delete(0, tk.END)

        # Populate the listbox with profile IDs and their indices
        for index, profile_id in enumerate(self.profile_ids, start=1):
            self.listbox.insert(tk.END, f"{index}. {profile_id}")

    def open_profile(self, event):
        # Get the selected item from the listbox
        selection = self.listbox.curselection()
        if selection:
            # Get the text of the selected item
            selected_text = self.listbox.get(selection[0])
            # Extract the profile ID from the text (remove the index and dot)
            profile_id = selected_text.split('. ')[1]
            messagebox.showinfo("Profile Opened", f"Opening profile: {profile_id}")
            # Here you can add the logic to open the profile
            print(f"Opening profile: {profile_id}")


if __name__ == "__main__":
    root = tk.Tk()

