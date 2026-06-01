# imports
import hashlib
import json
import requests
from yt_dlp import YoutubeDL

# variables
track_name = ""
artist_name = ""
album_name = ""
duration = int(0)
file_path = ""
yt_link = ""
# todo: verify if file path exists
synced_lyrics = ""
plain_lyrics = ""


# verifies nonce once calculated by solve_challenge
def verify_nonce(result, target) -> bool:
    if len(result) != len(target):
        return False

    for i in range(len(result) - 1):
        if result[i] > target[i]:
            return False
        elif result[i] < target[i]:
            break

    return True


# solves challenge given by request-challenge api endpoint
def solve_challenge(prefix: str, target_hex: str) -> str:
    nonce = 0
    target = bytes.fromhex(target_hex)

    while True:
        context = hashlib.sha256()
        prefix_nonce = f"{prefix}{nonce}"
        context.update(prefix_nonce.encode())
        hashed = context.digest()
        result = verify_nonce(hashed, target)

        if result:
            break
        else:
            nonce += 1

    print(f"nonce: {str(nonce)}")
    return str(nonce)


# converts (hh:mm:ss) into seconds
def to_seconds(dur):
    if dur.__class__ == str:
        if ":" in dur:
            dur_split = dur.split(":", 2)
            for i in range(len(dur_split)):
                if i + 1 < len(dur_split):
                    dur_split[i+1] = int(dur_split[i+1])
                    dur_split[i+1] += int(dur_split[i]) * 60
            return int(dur_split[len(dur_split) - 1])
        try:
            return int(dur)
        except ValueError:
            return "INVALID STRING"

    else:
        print(dur, dur.__class__)
        return "INVALID FORMAT"


# Converts .lrc file into plain lyrics and saves plain_lyrics and synced_lyrics
def synced_to_plain_lyrics():
    global plain_lyrics
    global synced_lyrics
    plain_list = []
    with open(file_path, "r", encoding='utf-8') as file:  # thank you python documentation
        synced_lyrics = file.read()
    with open(file_path, "r", encoding='utf-8') as file:
        lines_list = file.readlines()
    for i in range(len(lines_list)):
        try:
            plain_list.append(lines_list[i].split(" ", maxsplit=1)[1])
        except IndexError:
            if i < len(lines_list) - 1:
                plain_list.append("\n")

    plain_lyrics = "".join(plain_list)  # converts plain_list into like big string
    return plain_lyrics


# checks if there is an existing song with the same parameters in LRCLIB
def check_existing():

    url = "https://lrclib.net/api/get"
    params = {'artist_name': artist_name,
              'track_name': track_name,
              'album_name': album_name,
              'duration': to_seconds(duration)}
    header = {"Content-Type": "application/json",
              'User-Agent': 'LRCLIB-submit v?.?.? (https://github.com/werty-101/LRCLIB-submit)'}

    r = requests.get(url, params=params, headers=header)

    if r.status_code == 200:
        return True
    elif r.status_code == 404:
        return False
    else:
        print(f"unknown error, r.status_code: {r.status_code}")
        return None


# converts youtube video link to mp3 and saves it to path (MP3_FOLDER)
def yt_to_mp3(path):
    ydl_options = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': f'{path}/%(title)s.%(ext)s',
    }

    with YoutubeDL(ydl_options) as ydl:
        ydl.download([yt_link])


# Main func, API calls to request-challenge and publish
def main():

    # TODO: check if fields are filled
    # if val = "" then print('you must fill the required fields')

    url = "https://lrclib.net/api/request-challenge"
    header = {"Content-Type": "application/json",
              'User-Agent': 'LRCLIB-submit v?.?.? (https://github.com/werty-101/LRCLIB-submit)'}

    r = requests.post(url, headers=header)

    print(r.json())
    prefix = r.json()["prefix"]
    nonce = solve_challenge(prefix, r.json()["target"])

    url = "https://lrclib.net/api/publish"
    header = {"X-Publish-Token": f"{prefix}:{nonce}",
              "Content-Type": "application/json",
              "User-Agent": "LRCLIB-submit v?.?.? (https://github.com/werty-101/LRCLIB-submit)"}
    data = {"trackName": track_name,
            "artistName": artist_name,
            "albumName": album_name,
            "duration": to_seconds(duration),
            "plainLyrics": synced_to_plain_lyrics(),
            "syncedLyrics": synced_lyrics
            }

    r = requests.post(url, headers=header, data=json.dumps(data))

    print(r.status_code)

    if r.status_code == 201:
        print("OMGGG NO WAy")
    else:
        print("NOOOOOO")


def test_main():

    data = {"trackName": track_name,
            "artistName": artist_name,
            "albumName": album_name,
            "duration": to_seconds(duration),
            "plainLyrics": synced_to_plain_lyrics(),
            "syncedLyrics": synced_lyrics
            }

    print(data)

