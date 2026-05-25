# imports
import tkinter as tk
import submit_lyrics
from tkinter import filedialog
from pathlib import Path

LYRICS_FOLDER = "lyrics_folder"

# theme colors
dark_mode_colors = {
    "primary": "#202020",
    "secondary": "#303030",
    "accent": "#505050",
    "highlight": "#FFFFFF"

}


# Application class used in main()
class Application(tk.Tk):
    def __init__(self, title: str, size: tuple):
        super().__init__()
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.geometry(f"{size[0]}x{size[1]}")

        self.frame = MainView(self)


# Base class, used as template for frames
class Base(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background=dark_mode_colors["primary"])

    def show(self):
        self.tkraise()


# Page1 class, insert required fields and search/submit song
class Page1(Base):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_dir = ""

        self.pack(side="top", fill="x", expand=True)
        self.propagate(False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # look up .lrc and .txt files and insert them into the file entry field
        def browse_files(entry_field):
            file_name = filedialog.askopenfilename(initialdir=LYRICS_FOLDER,
                                                   title="Browse File",
                                                   filetypes=(
                                                       ("Lyric Files", "*.lrc"),
                                                       ("Text Files", "*.txt"),
                                                       ("All Files", "*.*")
                                                    )
                                                   )
            entry_field.insert(0, Path(file_name).name)
            self.file_dir = file_name

        # assign names to submit_lyrics using raw strings
        def assign_vars(title, artist, album, duration, path):
            # assign names to submit_lyrics
            # USE RAW STRINGS
            # todo: check if fields are filled
            submit_lyrics.track_name = title.get()
            submit_lyrics.artist_name = artist.get()
            submit_lyrics.album_name = album.get()
            submit_lyrics.duration = duration.get()
            submit_lyrics.file_path = path
            submit_lyrics.print_name()
            submit_lyrics.synced_to_plain_lyrics()
            # submit lyrics to function to like break down the lyrics
            # send it to main

        # title label
        tk.Label(master=self, text="Submit Lyrics to LRCLIB",
                 background=dark_mode_colors["primary"],
                 foreground=dark_mode_colors["highlight"],
                 font=[None, 15]
                 ).pack(side="top", pady=10)

        # creates container for each required field, ranges from 0-2

        entry_field_dict = {}

        for x in range(2):
            for y in range(2):
                # todo: use dictionary lookup table / match case
                if x + y == 0:
                    label_text = "Song Title Here"
                    entry_key = 0
                elif x + y == 2:
                    label_text = "Song Duration Here"
                    entry_key = 3
                elif y == 1:
                    label_text = "Song Artist Here"
                    entry_key = 1
                elif x == 1:
                    label_text = "Song Album Here"
                    entry_key = 2
                else:
                    label_text = "none"
                    entry_key = -1
                parent_frame = tk.Frame(master=self, background=dark_mode_colors["primary"], width=50, height=50)
                parent_frame.grid(row=x, column=y, sticky="nw", padx=20, pady=(50, 50))
                tk.Label(master=parent_frame, text=label_text,
                         background=dark_mode_colors["primary"],
                         foreground=dark_mode_colors["highlight"]
                         ).pack(anchor="nw", fill="y", expand=False)
                entry_value = tk.Entry(master=parent_frame)
                entry_value.pack(side="bottom", fill="both", expand=True)
                entry_field_dict[entry_key] = entry_value

        # file search frame
        file_frame = tk.Frame(master=self, background=dark_mode_colors["primary"])
        tk.Label(master=file_frame, text="Lyric File Path",
                 background=dark_mode_colors["primary"],
                 foreground=dark_mode_colors["highlight"]
                 ).pack(anchor="nw", fill="y", expand=True)
        file_entry = tk.Entry(master=file_frame, width=50, )
        file_entry.pack(side="left", fill="x", expand=True)
        file_browse_button = tk.Button(master=file_frame, text="Browse", width=10)
        file_browse_button.config(command=lambda: browse_files(file_entry))  # save returned str as var
        # something like (command=lambda: funct_return = browse_files(file_entry)
        file_browse_button.pack(side="right", padx=(10, 0))

        file_frame.grid(row=2, column=0, columnspan=2, sticky="n")

        # submit button
        b = tk.Button(master=self, text="Submit", width=10, height=2)
        b.config(command=lambda: assign_vars(entry_field_dict[0],
                                             entry_field_dict[1],
                                             entry_field_dict[2],
                                             entry_field_dict[3],
                                             self.file_dir))
        b.grid(row=3, column=0, columnspan=2, pady=(20, 50), sticky="n")






# MainView class, used as a container for frames, in case other pages are added onto app
class MainView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.p1 = Page1(self)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        self.pack(side='top', fill='both', expand=True)

        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        self.p1.show()


# calls Application class and mainloop
def main():
    app = Application("Submit Lyrics to LRCLIB", (450, 450))
    app.mainloop()


if __name__ == '__main__':
    main()

