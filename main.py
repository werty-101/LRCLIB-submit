# imports
import pydirectinput
import pygetwindow
import subprocess
from time import sleep
from bs4 import BeautifulSoup

screen_size = pydirectinput.size()
middle_x, middle_y = round(screen_size[0] * 0.5), round(screen_size[1] * 0.5)


def custom_triple_click(location_x: int, location_y: int):
    pydirectinput.moveTo(location_x, location_y)
    pydirectinput.moveRel(1, 0)
    for i in range(3):
        pydirectinput.mouseDown()
        #sleep(0.000000001)
        pydirectinput.mouseUp()
    pydirectinput.moveRel(-1, 0)




# activates the macro
def change_lyrics(time_start: int, lyric: str, time_end: int):
    # int(f"{(screen_size[0] * 0.5) :.0f}") looks ugly
    custom_triple_click(middle_x, middle_y)
    subprocess.run('clip', text=True, input=lyric)
    print(lyric)

    pydirectinput.keyDown('ctrl')
    pydirectinput.press('v')
    sleep(0.01)
    pydirectinput.keyUp('ctrl')
    pydirectinput.moveRel(0, round(screen_size[1] * 0.1))
    pydirectinput.moveRel(1, 0)
    pydirectinput.moveRel(-1, 0)
    pydirectinput.click()
    sleep((time_end - time_start) - 0.01)


# finds lyrics using song title and author in:
# https://www.eurobeat-prime.com/database.php?a=Author+Name&t=Song+Title&search=1
def find_lyrics(song_title: str, author: str):
    pass


def main():
    attempts = 0
    assert attempts < 10, "could not switch to 'Roblox' window within 10 attempts"
    # initial switch
    pygetwindow.getWindowsWithTitle('Roblox')[0].activate()

    # switch to roblox window
    while pygetwindow.getActiveWindowTitle() != 'Roblox' and attempts < 10:
        pygetwindow.getWindowsWithTitle('Roblox')[0].activate()
        sleep(0.02)
        attempts += 1

    print(pygetwindow.getActiveWindowTitle())
    pydirectinput.press('1')  # sign gear slot
    pydirectinput.click(middle_x, middle_y)
    pydirectinput.moveRel(1, 0)

    sleep(0.5)

    # thinking about doing something like for lyric in lyrics do change_lyrics
    # for that I'd need a list of all lyrics

    change_lyrics(123, "hello guys", 125)
    change_lyrics(125, "i am using this to test stuff", 126)

    pydirectinput.press('1')  # sign gear slot


if __name__ == '__main__':
    main()


