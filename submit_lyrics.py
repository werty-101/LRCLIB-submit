# imports
import hashlib
import requests

# variables
track_name = ""
artist_name = ""
album_name = ""
duration = 0
file_path = ""
# todo: get synced lyrics and plain lyrics from file_path
# todo: verify if file path exists
plain_lyrics = ""
synced_lyrics = ""

data = {"trackName": track_name,
        "artistName": artist_name,
        "albumName": album_name,
        "duration": duration,
        "plainLyrics": plain_lyrics,
        "syncedLyrics": synced_lyrics
        }


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


def print_name():
    print(rf"{track_name}, {artist_name}, {album_name}, {duration}, {file_path}")


def synced_to_plain_lyrics():
    # max split = 1
    plain_list = []
    with open(file_path, "r") as file:
        lines_list = file.readlines()
        for i in range(len(lines_list)):
            try:
                plain_list.append(lines_list[i].split(" ", maxsplit=1)[1])
            except IndexError:
                plain_list.append("\n")
            print(plain_list[i])  # plain lyrics
            # todo: convert stuff from plain_list into big string

            #print(lines_list[i].split(" ", maxsplit=1))

# todo: check if song is already in LRCLIB by performing /api/get-cached with vars from above


def main():
    url = "https://lrclib.net/api/request-challenge"
    header = {'User-Agent': 'rmm youtube bot v?.?.? (https://github.com/werty-101/rmm-youtube-bot)'}

    r = requests.post(url, headers=header)

    print(r.json())
    prefix = r.json()["prefix"]
    nonce = solve_challenge(prefix, r.json()["target"])

    url = "https://lrclib.net/api/publish"
    header = {"X-Publish-Token": f"{prefix}:{nonce}",
              "User-Agent": "rmm youtube bot v?.?.? (https://github.com/werty-101/rmm-youtube-bot)"}

    r = requests.post(url, headers=header, data=data)

    if r.status_code == 201:
        print("OMGGG NO WAy")
    else:
        print("NOOOOOO")

