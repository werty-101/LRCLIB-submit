# imports
import pydirectinput
import pygetwindow
import subprocess
import requests
import string
import os
import time

SCREEN_SIZE = pydirectinput.size()
MIDDLE_X, MIDDLE_Y = round(SCREEN_SIZE[0] * 0.5), round(SCREEN_SIZE[1] * 0.5)
BLACKLIST = "to_be_added.txt"  # used for song titles that return wrong lyrics so they can be added manually
SONGS_FOLDER = "lyrics_folder"  # todo: check if folder exists and check if its a folder item
FPS_CAP = 60


def custom_triple_click(location_x: int, location_y: int):
    pydirectinput.moveTo(location_x, location_y)
    pydirectinput.moveRel(1, 0)
    for i in range(3):
        pydirectinput.mouseDown()
        #sleep(0.000000001)
        pydirectinput.mouseUp()
    pydirectinput.moveRel(-1, 0)


def convert_to_seconds(timestamp: str):
    seconds = timestamp.translate(str.maketrans('', '', "[]")).split(":")
    return round(float((int(seconds[0]) * 60) + float(seconds[1])), 2)


def get_file_titles():
    local_titles = {}  # key = dir, value = item parts
    for title in os.scandir(SONGS_FOLDER):
        if title.is_file():
            file_dir = os.path.basename(title)
            file_items = file_dir.split(".")[0].translate(str.maketrans('', '', string.punctuation)).lower().split()
            local_titles[file_dir] = file_items

    return local_titles


# activates the macro and moves mouse slightly to wake up the mouse
def change_lyrics(time_start: float, lyric: str, time_end: float, current_fps: int):
    # int(f"{(screen_size[0] * 0.5) :.0f}") looks ugly
    custom_triple_click(MIDDLE_X, MIDDLE_Y)
    subprocess.run('clip', text=True, input=lyric)

    pydirectinput.keyDown('ctrl')
    pydirectinput.press('v')
    time.sleep(0.01)
    pydirectinput.keyUp('ctrl')
    pydirectinput.moveRel(0, round(SCREEN_SIZE[1] * 0.1))
    pydirectinput.moveRel(1, 0)
    pydirectinput.moveRel(-1, 0)
    pydirectinput.click()
    start_timer = time.perf_counter()
    # counts the time accurately, displays lyrics, keeps up with low fps, caps at FPS_CAP
    # current time <
    while time.perf_counter() - start_timer < ((time_end - time_start) * (current_fps / FPS_CAP)):
        time.sleep(0.001)
        

def test_change_lyrics(time_start: float, lyric: str, time_end: float, current_fps: int):
    start_timer = time.perf_counter()
    print(lyric)
    # todo: add something to check for fps, maybe OCR but I really dont want to
    if current_fps > FPS_CAP:
        current_fps = FPS_CAP
    # counts the time accurately, displays lyrics, keeps up with low fps by displaying lyrics faster
    # the slower the fps, the slower the input so you need to make up for it by making the wait time shorter
    # by how much?
    while time.perf_counter() - start_timer < ((time_end - time_start) * (current_fps / FPS_CAP)):
        time.sleep(0.001)


# find lyrics using song title and author on local database, if fail search https://lrclib.net
def find_lyrics(song_title: str, lyrics_folder: dict, author: str = ''):
    # todo: check if song is in to_be_added.txt if yes add song manually

    highest_match = 0
    match_dict = {}
    song_items = song_title.translate(str.maketrans('', '', string.punctuation)).lower().split()  # cleans up title name
    song_items.extend(author.lower().split())

    # loop thru each file in SONGS_FOLDER,
    for file in lyrics_folder:
        match_ratio = len(set(lyrics_folder[file]).intersection(song_items)) / len(lyrics_folder[file])

        if match_ratio > 0.50:
            match_dict[match_ratio] = file
            if match_ratio == 1:
                with open(f"{SONGS_FOLDER}//{match_dict[match_ratio]}", "r") as text_file:
                    # print(text_file.read())
                    return text_file.readlines()

        # print(f"\nfile name: {file_name}, compared with: {song_items}")
        # print(f"match %: {match_ratio}, common items: {set(file_name).intersection(song_items)} \n")
        if match_ratio > highest_match:
            highest_match = match_ratio

    print(lyrics_folder[match_dict[highest_match]])

    # title match
    try:
        with open(f"{SONGS_FOLDER}//{match_dict[highest_match]}", "r") as file:
            #print(file.read())
            return file.readlines()
    except KeyError:
        print("could not find potential lyrics in local db, switching to lrclib api")

        # try to get first result from search
        params = {'q': f"{song_title} {author}"}
        header = {'User-Agent': 'rmm youtube bot v?.?.? (https://github.com/werty-101/rmm-youtube-bot)'}

        r = requests.get("https://lrclib.net/api/search", params=params, headers=header)

        # if search fails, search local storage
        # what to do abt false positives
        # add them to the blacklist, so they can later be manually added to local db
        if r.json() and r.status_code == 200:
            # fetched lyrics! download to db instead of printing
            # todo: add clean version of lyrics to database
            # if item exists / another try except (dont really want another tho)
            print(f"\nlyrics found! from: {r.json()[0]['artistName']} title: {r.json()[0]['trackName']}\n")
            print("Lyrics:")
            print(r.json()[0]["syncedLyrics"])
            # print(os.path.join(SONGS_FOLDER, f"{author} - {song_title}.lrc"))
            if input("save lyrics? (y/n): ").lower() == 'y':
                # f = open(os.path.join(SONGS_FOLDER, f"{author} - {song_title}.lrc"), "x")
                f = open(f"{SONGS_FOLDER}//{author} - {song_title}.lrc", 'x')
                f.write(r.json()[0]["syncedLyrics"])
                f.close()
                print(f"saved lyrics to {SONGS_FOLDER} folder")
        elif not r.json() and r.status_code == 200:
            print("could not find lyrics using lrclib api")
            return [f'could not find lyrics for {song_title}']
        else:
            print(f"an unknown error occurred: r.status_code = {r.status_code}")


def main():
    attempts = 0
    assert attempts < 10, "could not switch to 'Roblox' window within 10 attempts"
    # initial switch
    try:
        pygetwindow.getWindowsWithTitle('Roblox')[0].activate()
    except IndexError:
        print("'Roblox' window not detected")
        time.sleep(1)
        exit(0)

    # switch to roblox window
    while pygetwindow.getActiveWindowTitle() != 'Roblox' and attempts < 10:
        pygetwindow.getWindowsWithTitle('Roblox')[0].activate()
        time.sleep(0.02)
        attempts += 1

    print(pygetwindow.getActiveWindowTitle())
    pydirectinput.press('1')  # sign gear slot (open)
    pydirectinput.click(MIDDLE_X, MIDDLE_Y)
    pydirectinput.moveRel(1, 0)

    time.sleep(0.5)

    # thinking about doing something like for lyric in lyrics do change_lyrics
    # for that I'd need a list of all lyrics

    current_fps = 45  # assume 15-18 for test, caps at FPS_CAP, the fps is so inconsistent
    test_song = 'Fireball'
    test_author = 'Ken Martin'
    file_titles = get_file_titles()
    synced_lyrics = find_lyrics(test_song, file_titles, test_author)
    if synced_lyrics is not None:
        # separate the timestamp from the lyric then convert timestamp to seconds
        for i in range(len(synced_lyrics)):
            if i + 1 < len(synced_lyrics):
                # PERFORMS VERY BAD ON LOW FPS
                current_lyric = synced_lyrics[i].split(' ', 1)
                timestamp = convert_to_seconds(current_lyric[0])
                lyric_str = current_lyric[1].replace("\n", "")
                next_timestamp = convert_to_seconds(synced_lyrics[i+1].split(' ', 1)[0])
                change_lyrics(timestamp, lyric_str, next_timestamp, current_fps)

    else:
        print("None returned")

    pydirectinput.press('1')  # sign gear slot (close)


def test_main():
    # testing cuz I dont wanna launch app
    # thinking abt removing author field bcuz song could be uploaded by someone else
    # happens pretty often ^^^
    current_fps = 60  # assume 15-18 for test, caps at 60, still goes too fast
    file_titles = get_file_titles()
    # file titles
    print("in app")
    # after title and author fetched, def fetch_vid_title:
    test_song = 'fireball'
    test_author = 'Ken Martin'
    synced_lyrics = find_lyrics(test_song, file_titles, test_author)
    if synced_lyrics is not None:
        # separate the timestamp from the lyric then convert timestamp to seconds
        # idea: check the time since running so it can display the correct lyrics (and skip unused ones)
        # have fun dealing with 15 fps idiot
        # startup time is so annoying
        # todo: assume every song starts at 0, without needing to check timestamp
        for i in range(len(synced_lyrics)):
            if i + 1 < len(synced_lyrics):
                current_lyric = synced_lyrics[i].split(' ', 1)
                timestamp = convert_to_seconds(current_lyric[0])
                lyric_str = current_lyric[1].replace("\n", "")
                next_timestamp = convert_to_seconds(synced_lyrics[i+1].split(' ', 1)[0])
                # print(round(end_time - start_time, 8))
                test_change_lyrics(timestamp, lyric_str, next_timestamp, current_fps)

    else:
        print("None returned")


# to test use: Fever the Night by Matt Land, Virtual Love by Ken Martin, and With you (1994) by Helena
# more tests: In My Dreams by Denise, Can't Stay A Dreamy Girl by Nikita Jr
# also try to use mixes into the player
if __name__ == '__main__':
    main()


