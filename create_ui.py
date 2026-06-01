# imports
import tkinter as tk
import submit_lyrics
import threading
from tkinter import filedialog, messagebox
from pathlib import Path

# constants
MP3S_FOLDER = Path("songs\\mp3s")
LYRICS_FOLDER = Path("songs\\lyrics_folder")

# theme colors
dark_mode_colors = {
    "primary": "#202020",
    "secondary": "#252525",
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
        self.minsize(width=size[0], height=size[1])
        #self.maxsize(width=size[0], height=size[1])

        self.frame = MainView(self)


# Base class, used as template for frames
class Base(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background=dark_mode_colors["primary"])

    def show(self):
        self.tkraise()


# Menu class, creates side menu for switching pages
class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config(background=dark_mode_colors["secondary"], width=90)
        self.pack(side="left", fill="both", expand=True)
        self.propagate(False)

        self.active_button = None
        self.button_texts = ["Submit Lyrics to LRCLIB", "YouTube to MP3"]
        self.buttons = []

        # loop for creating buttons and assigning them to self.buttons
        for b in self.button_texts:
            button = tk.Button(self, text=b,
                               wraplength=100,
                               background=dark_mode_colors["accent"],
                               foreground=dark_mode_colors["highlight"],
                               activebackground=dark_mode_colors["secondary"],
                               activeforeground=dark_mode_colors["highlight"],
                               border=0,
                               height=4,
                               relief="flat",
                               pady=2
                               )
            self.buttons.append(button)

        self.buttons[0].config(command=lambda: page_switch(self.buttons[0], parent.p1))
        self.buttons[0].pack(side="top")

        self.buttons[1].config(command=lambda: page_switch(self.buttons[1], parent.p2))  # idiot
        self.buttons[1].pack(side="top")

        # switches page and sets the color of the button that is clicked as primary
        def page_switch(b_obj, page):
            #for b in self.buttons:
            #    b.config(background=dark_mode_colors["accent"])
            if self.active_button is not None:
                self.active_button.config(background=dark_mode_colors["accent"])
            b_obj.config(background=dark_mode_colors["primary"])
            self.active_button = b_obj
            page.show()


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
        def assign_vars(**kwargs):  # (title, artist, album, duration, path):
            # assign names to submit_lyrics
            # USE RAW STRINGS, do I need to use raw strings?
            for i in kwargs:
                print(i, kwargs[i], kwargs[i].__class__)
                if kwargs[i] == "":
                    print(f"{i} is an empty value")
                    return

            submit_lyrics.track_name = kwargs["title"]
            submit_lyrics.artist_name = kwargs["artist"]
            submit_lyrics.album_name = kwargs["album"]
            submit_lyrics.duration = kwargs["duration"]
            submit_lyrics.file_path = kwargs["path"]
            is_existing = submit_lyrics.check_existing()
            if is_existing:
                q = messagebox.askquestion(title="Warning",
                                           message="That song is already in LRCLIB! Are you sure you want to submit it?"
                                           )
                if q == "yes":
                    submit_lyrics.test_main()
            elif not is_existing:
                submit_lyrics.test_main()
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
                # todo: use dictionary lookup table / match case (maybe)
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
        # TODO: clear previous name after file is browsed
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
        b.config(command=lambda: threading.Thread(target=assign_vars, kwargs={'title': entry_field_dict[0].get(),
                                                                              'artist': entry_field_dict[1].get(),
                                                                              'album': entry_field_dict[2].get(),
                                                                              'duration': entry_field_dict[3].get(),
                                                                              'path': self.file_dir
                                                                              }
                                                  ).start()
                 )
        # assign_vars(title=entry_field_dict[0],
        #                                              artist=entry_field_dict[1],
        #                                              album=entry_field_dict[2],
        #                                              duration=entry_field_dict[3],
        #                                              path=self.file_dir)
        b.grid(row=3, column=0, columnspan=2, pady=(20, 50), sticky="n")


# Page2 class, youtube to mp3 downloader
class Page2(Base):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(side="top", fill="x", expand=True)
        self.propagate(False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # title label
        tk.Label(master=self, text="Youtube to MP3",
                 background=dark_mode_colors["primary"],
                 foreground=dark_mode_colors["highlight"],
                 font=[None, 15]
                 ).pack(side="top", pady=10)

        entry_container = tk.Frame(self)
        tk.Label(master=entry_container,text="Insert Youtube Video Link", background=dark_mode_colors["primary"],
                 foreground=dark_mode_colors["highlight"]).pack(anchor="nw", fill="x")
        link_entry = tk.Entry(master=entry_container, width=50)
        link_entry.pack(side="bottom")
        entry_container.grid(row=0, column=0)

        search_yt_button = tk.Button(self, text="Download", width=10, height=2)
        search_yt_button.config(command=lambda: threading.Thread(target=search_yt, args=(link_entry, MP3S_FOLDER)
                                                                 ).start())
        search_yt_button.grid(row=1, column=0, sticky="n", pady=(0, 200))

        def search_yt(entry, path):
            submit_lyrics.yt_link = entry.get()
            submit_lyrics.yt_to_mp3(path)


# MainView class, used as a container for frames, in case other pages are added onto app
class MainView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.p1 = Page1(self)
        self.p2 = Page2(self)
        self.menu = Menu(self)

        # container to hold the page
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        self.menu.pack(side='left', fill='both', expand=False)

        self.pack(side='top', fill='both', expand=True)

        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        self.p1.show()


# calls Application class and mainloop
def main():
    app = Application("Submit Lyrics to LRCLIB", (450 + 90, 450))
    app.mainloop()


if __name__ == '__main__':
    main()

