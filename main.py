# imports
import pydirectinput
import pygetwindow
import subprocess
import requests
import string
import os
from time import sleep
from dotenv import load_dotenv


load_dotenv()
SCREEN_SIZE = pydirectinput.size()
MIDDLE_X, MIDDLE_Y = round(SCREEN_SIZE[0] * 0.5), round(SCREEN_SIZE[1] * 0.5)
TITLE_DB = "lyric_database.txt"
BLACKLIST = "blacklist.txt"
SONGS_FOLDER = "lyrics_folder"


def custom_triple_click(location_x: int, location_y: int):
    pydirectinput.moveTo(location_x, location_y)
    pydirectinput.moveRel(1, 0)
    for i in range(3):
        pydirectinput.mouseDown()
        #sleep(0.000000001)
        pydirectinput.mouseUp()
    pydirectinput.moveRel(-1, 0)


# activates the macro and moves mouse slightly to wake up the mouse
def change_lyrics(time_start: int, lyric: str, time_end: int):
    # int(f"{(screen_size[0] * 0.5) :.0f}") looks ugly
    custom_triple_click(MIDDLE_X, MIDDLE_Y)
    subprocess.run('clip', text=True, input=lyric)
    print(lyric)

    pydirectinput.keyDown('ctrl')
    pydirectinput.press('v')
    sleep(0.01)
    pydirectinput.keyUp('ctrl')
    pydirectinput.moveRel(0, round(SCREEN_SIZE[1] * 0.1))
    pydirectinput.moveRel(1, 0)
    pydirectinput.moveRel(-1, 0)
    pydirectinput.click()
    sleep((time_end - time_start) - 0.01)


# find lyrics using song title and author on local database, if fail search https://lrclib.net
def find_lyrics(song_title: str, author: str = '', length: int = 0):
    # todo: check if song is in blacklist.txt if yes go search on api

    highest_match = 0
    match_dict = {}
    print()
    song_items = song_title.translate(str.maketrans('', '', string.punctuation)).split()  # cleans up title name
    song_items.extend(author.split())

    # loop thru each item in SONGS_FOLDER,
    for title in os.scandir(SONGS_FOLDER):
        if title.is_file():
            # compares common items between file title and song items and returns % as decimal
            file_name = (os.path.basename(title).split(".")[0]
                         .translate(str.maketrans('', '', string.punctuation)).split())  # cleans up file name
            match_ratio = len(set(file_name).intersection(song_items)) / len(file_name)

            if match_ratio > 0.50:
                match_dict[match_ratio] = title

            print(f"file name: {file_name}, compared with: {song_items}")
            print(f"match %: {match_ratio} \n")
            if match_ratio > highest_match:
                highest_match = match_ratio
                print(f"highest match: {highest_match}")

    # title match
    try:
        with open(match_dict[highest_match].path, "r") as file:
            print(file.read())
            return file.readlines()
    except KeyError:
        print("could not find potential lyrics in local db, switching to lrclib api")

        # try to get first result from search
        if length > 0 and author:
            params = {'artist_name': f"{author}", 'track_name': f"{song_title}", 'duration': length}
        elif length > 0:
            params = {'track_name': f"{song_title}", 'duration': length}
        elif author:
            params = {'artist_name': f"{author}", 'track_name': f"{song_title}"}
        else:
            params = {'track_name': f"{song_title}"}

        r = requests.get("https://lrclib.net/api/get", params=params)

        # if search fails, search local storage
        # what to do abt false positives
        # add them to the blacklist, so they can later be manually added to local db
        if r.status_code == 404:
            print("song not found on lrclib")
            return f"{song_title} not found in local db nor api"
        elif r.status_code == 200:
            # fetched lyrics! download to db instead of printing
            # todo: download lyrics to SONGS_FOLDER as .lrc (or txt i could not care any less as long as its readable)
            print(r.json()["syncedLyrics"])
        else:
            print(f"an unknown error occurred: r.status_code = {r.status_code}")


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
    pydirectinput.press('1')  # sign gear slot (open)
    pydirectinput.click(MIDDLE_X, MIDDLE_Y)
    pydirectinput.moveRel(1, 0)

    sleep(0.5)

    # thinking about doing something like for lyric in lyrics do change_lyrics
    # for that I'd need a list of all lyrics

    change_lyrics(123, "hello guys", 125)
    change_lyrics(125, "i am using this to test stuff", 126)

    pydirectinput.press('1')  # sign gear slot (close)

# to test use: Fever the Night by Matt Land, Virtual Love by Ken Martin, and With you (1984) by Helena
# also try to use mixes into the player
if __name__ == '__main__':
    #genius_auth()
    find_lyrics("Yo Mama", "Mama")
    #main()


