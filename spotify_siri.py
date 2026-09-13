# ============================================================
# TERMINAL INSTRUCTIONS
# ============================================================
#
# 1. Open Terminal.
#
# 2. Create the folder:
#
# mkdir -p ~/spotify-siri
#
# 3. Open the Python file:
#
# nano ~/spotify-siri/spotify_siri.py
#
# 4. Paste this entire file into nano.
#
# 5. Find the section called "Spotify credentials".
#
# 6. Replace:
#
# YOUR_CLIENT_ID_HERE
#
# with your Spotify Client ID.
#
# 7. Replace:
#
# YOUR_CLIENT_SECRET_HERE
#
# with your Spotify Client Secret.
#
# Example:
#
# CLIENT_ID = "1234567890abcdef"
# CLIENT_SECRET = "abcdef1234567890"
#
# 8. Save the file:
# Control + O
# Enter
#
# 9. Exit nano:
# Control + X
#
# 10. Make the script executable:
#
# chmod +x ~/spotify-siri/spotify_siri.py
#
# 11. Install Spotipy:
#
# /Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pip install spotipy
#
# 12. Test it:
#
# /Library/Frameworks/Python.framework/Versions/3.14/bin/python3 ~/spotify-siri/spotify_siri.py "Blinding Lights"
#
# 13. Test another song:
#
# /Library/Frameworks/Python.framework/Versions/3.14/bin/python3 ~/spotify-siri/spotify_siri.py "Song Name"
#
# ============================================================


import sys
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# ============================================================
# SPOTIFY CREDENTIALS
# ============================================================

CLIENT_ID = "YOUR_CLIENT_ID_HERE"
CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"


# ============================================================
# SPOTIFY AUTHENTICATION
# ============================================================

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope="user-read-playback-state user-modify-playback-state",
        redirect_uri="http://127.0.0.1:8888/callback"
    )
)


# ============================================================
# GET SONG NAME
# ============================================================

if len(sys.argv) < 2:
    print('Usage: python3 spotify_siri.py "Song Name"')
    sys.exit(1)

song_name = " ".join(sys.argv[1:])


# ============================================================
# NORMALIZE TEXT FOR SONG MATCHING
# ============================================================

def normalize(text):
    return "".join(
        character.lower()
        for character in text
        if character.isalnum()
    )


# ============================================================
# SEARCH FOR THE SONG
# ============================================================

results = sp.search(
    q=f'track:"{song_name}"',
    type="track",
    limit=10
)

tracks = results["tracks"]["items"]


# Fallback search if exact search finds nothing
if not tracks:
    results = sp.search(
        q=song_name,
        type="track",
        limit=10
    )
    tracks = results["tracks"]["items"]


if not tracks:
    print(f"Song not found: {song_name}")
    sys.exit(1)


# ============================================================
# FIND THE CLOSEST EXACT TITLE
# ============================================================

normalized_song = normalize(song_name)

track = None

for candidate in tracks:
    if normalize(candidate["name"]) == normalized_song:
        track = candidate
        break


# If no exact title match, use the first result
if track is None:
    track = tracks[0]


print(
    f"Selected: {track['name']} — "
    f"{track['artists'][0]['name']}"
)


# ============================================================
# FIND AN AVAILABLE SPOTIFY DEVICE
# ============================================================

devices = sp.devices()["devices"]

if not devices:
    print("No Spotify devices available.")
    sys.exit(1)


active_device = next(
    (device for device in devices if device["is_active"]),
    None
)


computer_device = next(
    (
        device
        for device in devices
        if device["type"].lower() == "computer"
        and not device["is_restricted"]
    ),
    None
)


usable_device = next(
    (
        device
        for device in devices
        if not device["is_restricted"]
    ),
    None
)


device = active_device or computer_device or usable_device


if device is None:
    print("No usable Spotify device found.")
    sys.exit(1)


print(f"Using device: {device['name']}")


# ============================================================
# PLAY THE EXACT TRACK USING SPOTIFY'S NATIVE APPLESCRIPT
# ============================================================

track_uri = track["uri"]


apple_script = f'''
tell application "Spotify"
    play track "{track_uri}"
    delay 0.1
end tell
'''


subprocess.run(
    ["osascript", "-e", apple_script],
    check=True
)


print("Playback command sent to Spotify.")
