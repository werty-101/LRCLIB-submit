import sys
import submit_lyrics
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QHBoxLayout, QVBoxLayout, QPushButton,
                               QStackedWidget, QLabel, QGridLayout,
                               QLineEdit, QSizePolicy)
from PySide6.QtCore import Qt

# folder constants, creates folder before assigning to variable
MP3S_FOLDER = Path("songs\\mp3s")
LYRICS_FOLDER = Path("songs\\lyrics_folder")

MP3S_FOLDER.mkdir(parents=True, exist_ok=True)
LYRICS_FOLDER.mkdir(exist_ok=True)

COLOR_THEMES = {

    'dark_mode': {

        "primary": "#202020",
        "secondary": "#252525",
        "accent": "#505050",
        "highlight": "#FFFFFF"

    },

    'light_mode': {

        "primary": "#e4e5f1",
        "secondary": "#d2d3db",
        "accent": "#9394a5",
        "highlight": "#484b6a"

    },

}


# LRCLIB submit
class Page1(QWidget):
    def __init__(self):
        super().__init__()

        self.current_theme = None

        # setup page layout
        page_layout = QGridLayout(self)
        page_title = QLabel("Submit Lyrics to LRCLIB")
        page_title.setStyleSheet("font-size: 24pt")
        #page_title.setWordWrap(True)
        page_title.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        page_title.setMinimumWidth(250)

        page_layout.addWidget(page_title, 0, 0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        grid_layout_text = ["Song Title", "Artist Name", "Album Name", "Duration"]
        input_list = []

        # creates qwidgets as frames for text input boxes + labels above boxes then places qwidgets in page_layout
        y = 1
        x = 0
        for i in range(len(grid_layout_text)):
            if x > 1:
                x = 0
                y += 1
            frame = QWidget()
            frame_layout = QVBoxLayout(frame)
            frame_layout.setSpacing(5)
            frame_layout.setContentsMargins(0, 0, 0, 0)

            label = QLabel(grid_layout_text[i])

            text_input = QLineEdit()
            text_input.setFixedWidth(120)
            #text_input.setFixedHeight(20)
            #text_input.setStyleSheet("background-color: #FFFFFF; color: #000000; font-size: 12pt; border: none;")

            frame_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignBottom)
            frame_layout.addWidget(text_input, alignment=Qt.AlignmentFlag.AlignTop)

            page_layout.addWidget(frame, y, x, alignment=Qt.AlignmentFlag.AlignCenter)
            print(y, x)
            input_list.append(text_input)
            x += 1

        # Builds the file frame for inputting file title and input box as well as "browse" button

        file_frame = QWidget()
        file_frame_layout = QGridLayout(file_frame)

        file_label = QLabel("Lyrics File")

        file_input = QLineEdit()
        file_input.setFixedWidth(200)

        browse_button = QPushButton("Browse")
        browse_button.setFixedHeight(30)
        browse_button.setFixedWidth(75)

        # add widgets to the file frame

        file_frame_layout.setVerticalSpacing(0)
        file_frame_layout.setHorizontalSpacing(5)
        file_frame_layout.addWidget(file_label, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        file_frame_layout.addWidget(file_input, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        file_frame_layout.addWidget(browse_button, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        # add file frame to the page frame thing

        #page_layout.addWidget(title_box, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        #page_layout.addWidget(artist_box, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        page_layout.addWidget(file_frame, 3, 0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        submit_button = QPushButton("Submit")
        submit_button.setFixedHeight(45)
        submit_button.setFixedWidth(85)

        page_layout.addWidget(submit_button, 4, 0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)


    def update_theme(self, theme):
        self.current_theme = theme

        self.setStyleSheet(f"""
            QLabel {{
                font-size: 12pt
            }}
            
            QLineEdit {{
                background-color: #FFFFFF;
                color: #000000;
                font-size: 12pt;
                border: none;
                height: 20px;
            }}
            
            QPushButton {{
                color: {self.current_theme["secondary"]};
                background-color: {self.current_theme["highlight"]};
            }}
            
            QPushButton:hover {{
                color: {self.current_theme["highlight"]};
                background-color: {self.current_theme["accent"]};
            }}
            
            QPushButton:pressed {{
                color: {self.current_theme["highlight"]};
                background-color: {self.current_theme["secondary"]};
            }}
            
        """)


# youtube to mp3 page
class Page2(QWidget):
    def __init__(self):
        super().__init__()

        self.current_theme = None

        # setup page layout
        page_layout = QGridLayout(self)
        page_title = QLabel("YouTube to MP3")
        page_title.setStyleSheet("font-size: 24pt")

        # QLineEdit here
        link_input_frame = QWidget(self)
        link_input_layout = QVBoxLayout(link_input_frame)

        link_input_label = QLabel("Insert Link") 

        link_input = QLineEdit(self)
        link_input.setFixedWidth(200)

        link_input_layout.addWidget(link_input_label)
        link_input_layout.addWidget(link_input)


        # QPushButton to download video
        download_button = QPushButton("Download")
        download_button.setFixedHeight(50)
        download_button.setFixedWidth(100)
        download_button.clicked.connect(lambda: self.download_video(link_input.text()))

        # Add widgets here
        page_layout.addWidget(page_title, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        page_layout.addWidget(link_input_frame, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        page_layout.addWidget(download_button, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)


    # function to communicate with submit_lyrics.py
    def download_video(self, link):
        submit_lyrics.yt_link = link
        submit_lyrics.yt_to_mp3("songs\mp3s")



    # styling TODO: would be nice if it inherited styling from a base class
    def update_theme(self, theme):
        self.current_theme = theme

        self.setStyleSheet(f"""
            QLabel {{
                font-size: 12pt
            }}
                           
            QLineEdit {{
                background-color: #FFFFFF;
                color: #000000;
                font-size: 12pt;
                border: none;
                height: 20px;
            }}
                           
            QPushButton {{
                color: {self.current_theme["secondary"]};
                background-color: {self.current_theme["highlight"]};
            }}

            QPushButton:hover {{
                color: {self.current_theme["highlight"]};
                background-color: {self.current_theme["accent"]};
            }}

            QPushButton:pressed {{
                color: {self.current_theme["highlight"]};
                background-color: {self.current_theme["secondary"]};
            }}

        """)




class MainWindow(QMainWindow):
    def __init__(self, title: str, size):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedSize(size[0], size[1])

        self.current_theme = None
        self.active_button = None

        self.p1 = Page1()
        self.p2 = Page2()

        self.switch_theme('dark_mode')

        # main container for the entire WINDOW

        main_container = QWidget()
        self.setCentralWidget(main_container)

        main_layout = QHBoxLayout(main_container)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # sidebar placed at the LEFT of the WINDOW

        sidebar = QWidget()
        sidebar.setFixedWidth(90)
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        main_layout.addWidget(sidebar)

        # add buttons to sidebar

        button_texts = ["Submit\nLyrics", "Youtube\nto MP3"]
        button_list = []

        for text in button_texts:
            button = QPushButton(text)
            button.setFixedHeight(50)
            sidebar_layout.addWidget(button)
            button_list.append(button)

        # anything after this in the SIDEBAR will make it appear on the bottom for some reason
        sidebar_layout.addStretch()

        button_list[0].clicked.connect(lambda: self.page_switch(button_list[0], 0))
        button_list[1].clicked.connect(lambda: self.page_switch(button_list[1], 1))

        # secondary container is used for holding pages (kind  of like a list)

        self.secondary_container = QStackedWidget()

        self.secondary_container.addWidget(self.p1)
        self.secondary_container.addWidget(self.p2)

        main_layout.addWidget(self.secondary_container)

        self.page_switch(button_list[0], 0)

    # unhighlights active button, highlights pressed button and sets it as active button
    def page_switch(self, b, page_num):
        if self.active_button is not None:
            self.active_button.setStyleSheet(f"""{{
                background-color: {COLOR_THEMES[self.current_theme]['secondary']}
            }}""")
        print(f"MainWindow current_theme: {self.current_theme}")
        b.setStyleSheet(f"background-color: {COLOR_THEMES[self.current_theme]['primary']}")  # button thats pressed
        self.active_button = b
        print(f"you pressed {b}, page: {page_num}")
        self.secondary_container.setCurrentIndex(page_num)

    def switch_theme(self, theme_name):
        app = QApplication.instance()
        current_theme = COLOR_THEMES[theme_name]  # NOT A FRAUD, YOU'RE NOT A FRAUD, BELIEVE IN YOURSELF

        app.setStyleSheet(f"""
    QWidget {{
        background-color: {current_theme["primary"]};
        color: {current_theme["highlight"]};
    }}
    #sidebar {{
        background-color: {current_theme["secondary"]};
    }}
    QPushButton {{
        background-color: {current_theme["secondary"]};
        color: {current_theme["highlight"]};
        border: none;
    }}
    QPushButton:hover {{
        background-color: {current_theme["accent"]};
    }}
    QPushButton:pressed {{
        background-color: {current_theme["primary"]};
    }}

    """)

        self.current_theme = theme_name

        self.p1.update_theme(current_theme)
        self.p2.update_theme(current_theme)



def main():
    app = QApplication(sys.argv)

    window = MainWindow("LRCLIB Submit", (450 + 90, 450))

    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

