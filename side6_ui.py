import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QHBoxLayout, QVBoxLayout, QPushButton,
                               QStackedWidget, QLabel, QGridLayout)
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

QSS_TEMPLATE = """
    QWidget {{
        background-color: {primary};
        color: {highlight};
    }}
    #sidebar {{
        background-color: {secondary};
    }}
    QPushButton {{
        background-color: {secondary};
        color: {highlight};
    }}
    QPushButton:hover {{
        background-color: {accent};
    }}
    QPushButton:pressed {{
        background-color: {primary};
    }}
"""


class MainWindow(QMainWindow):
    def __init__(self, title: str, size):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedSize(size[0], size[1])

        self.current_theme = None
        self.active_button = None

        self.switch_theme('dark_mode')

        # TODO: make a mainContainer and put sidebar container and secondary container
        # TODO: add LAYOUTS to BOTH sidebar container and secondary container
        # TODO: put grid layout inside secondary container
        # TODO: add buttons inside the sidebar container
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
        sidebar_layout.setSpacing(5)

        main_layout.addWidget(sidebar)

        # add buttons to sidebar

        button_texts = ["Submit\nLyrics", "Youtube\nto MP3"]
        button_list = []

        for text in button_texts:
            button = QPushButton(text)
            button.setFixedHeight(40)
            sidebar_layout.addWidget(button)
            button_list.append(button)

        sidebar_layout.addStretch()

        button_list[0].clicked.connect(lambda: self.page_switch(button_list[0], "page 0"))
        button_list[1].clicked.connect(lambda: self.page_switch(button_list[1], "page 1"))


        # SECONDARY CONTAINER IS USED FOR PAGE SWITCHING

        secondary_container = QWidget()

        main_layout.addWidget(secondary_container)

    # def apply_custom_theme(self, theme_name):
    #    """Dynamically applies a chosen custom theme profile."""
    #    theme_colors = COLOR_THEMES[theme_name]
    #    # Format the QSS template with the dictionary values
    #    formatted_qss = QSS_TEMPLATE.format(**theme_colors)  # FRAUD YOU'RE A FRAUD YOU KNOW NOTHING
    #
    #    # Apply globally to the entire application scope
    #    QApplication.instance().setStyleSheet(formatted_qss)

    # unhighlights active button, highlights pressed button and sets it as active button
    def page_switch(self, b, page):
        if self.active_button is not None:
            self.active_button.setStyleSheet(f"background-color: {COLOR_THEMES[self.current_theme]["secondary"]}")
        b.setStyleSheet(f"background-color: {COLOR_THEMES[self.current_theme]["primary"]}")
        self.active_button = b
        print(f"you pressed {b}, {page}")

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
    }}
    QPushButton:hover {{
        background-color: {current_theme["accent"]};
    }}
    QPushButton:pressed {{
        background-color: {current_theme["primary"]};
    }}

    """)
        self.current_theme = theme_name

class Page1(QWidget):
    def __init__(self):
        super().__init__()

        pass


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

