import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QHBoxLayout, QVBoxLayout, QPushButton,
                               QStackedWidget, QLabel, QGridLayout, QLineEdit)
from PySide6.QtCore import Qt


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
    def __init__(self, parent_obj):
        super().__init__()

        self.parent = parent_obj
        self.current_theme = COLOR_THEMES[self.parent.current_theme]
        print(self.current_theme)
        # TODO: parent_obj.current_theme does not change if switch_theme() is called
        # TODO: maybe add something like update_theme() at the start of the class

        # setup page layout
        page_layout = QGridLayout(self)
        page_title = QLabel("Submit Lyrics to LRCLIB")
        page_title.setStyleSheet("font-size: 24pt")
        # TODO: Add QWidget with QVlayout to place title of input box and stuff

        title_box = QWidget()
        title_box_layout = QVBoxLayout(title_box)
        title_box_layout.setSpacing(5)
        title_box_layout.setContentsMargins(0, 0, 0, 0)
        title_label = QLabel("Song Title")
        title_label.setStyleSheet("font-size: 12pt")
        title_input = QLineEdit()
        title_input.setFixedWidth(120)
        title_input.setStyleSheet("background-color: #FFFFFF; color: #000000;")

        title_box_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignBottom)
        title_box_layout.addWidget(title_input, alignment=Qt.AlignmentFlag.AlignTop)

        label2 = QLabel("PAGE 1")
        label3 = QLabel("PAGE 1")
        label4 = QLabel("PAGE 1")
        label5 = QLabel("PAGE 1")


        page_layout.addWidget(page_title, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        page_layout.addWidget(title_box, 1, 0)
        page_layout.addWidget(label3, 2, 0)
        page_layout.addWidget(label4, 3, 0)
        page_layout.addWidget(label5, 4, 0)

    def update_theme(self):
        # label.setStyleSheet(f"""QLabel {{
        #    background-color: {self.current_theme['secondary']};
        #    font-size: 24pt;
        # }}""")
        print(f"Page1 current_theme: {self.current_theme}")




# youtube to mp3 page
class Page2(QWidget):
    def __init__(self, parent_obj):
        super().__init__()

        # setup page layout
        page_layout = QGridLayout(self)
        label = QLabel("PAGE 2")

        page_layout.addWidget(label, 0, 0)


class MainWindow(QMainWindow):
    def __init__(self, title: str, size):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedSize(size[0], size[1])

        self.current_theme = None
        self.active_button = None

        self.switch_theme('dark_mode')

        self.p1 = Page1(self)
        self.p2 = Page2(self)


        # TODO: fix error when like using switch_theme() it only partially changes the theme

        #self.switch_theme('light_mode')

        # TODO: add content to secondary container

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

        # anything after this in the sidebar will make it appear on the bottom for some reason
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



def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(f"""

        QWidget {{
            color: black;
        }}

    """)

    window = MainWindow("LRCLIB Submit", (450 + 90, 450))

    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

