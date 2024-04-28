import pylast
import requests
import shutil
import os
import asyncio
from pathlib import Path


class LastFm:
    def __init__(self, username, password, api_key, api_secret, running=True):
        # Initiate a session
        password_hash = pylast.md5(password)
        self.network = pylast.LastFMNetwork(api_key=api_key,
                                            api_secret=api_secret,
                                            username=username,
                                            password_hash=password_hash)

        self.username = self.network.get_user(username)
        self.running = running
        self.current_playing = None
        self.current_artwork = None

    async def get_now_playing_album_art(self, timeout):
        # Ability to turn off get now playing
        while self.running:
            # Get now playing every timeout seconds
            await asyncio.sleep(timeout)
            new_track = self.get_now_playing()

            # If a new song is playing, update current playing
            if new_track != self.current_playing:
                self.current_playing = new_track

                # If nothing is playing skip getting album art
                if self.current_playing is None:
                    continue

                # Delete album art already saved
                self.delete_album_art()

                print(f"Now playing: {str(self.current_playing)}")

                # Download new album art
                self.current_artwork = self.get_album_art(self.current_playing)

                return True

    def delete_album_art(self):
        current_dir = os.getcwd()
        files = os.listdir(current_dir)

        for file in files:
            if Path(file).name == "temp_album":
                os.remove(file)

    def get_now_playing(self):
        track = self.username.get_now_playing()

        return track

    def get_album_art(self, track):
        print(f"Getting album art for song {track.get_album()}")
        get_attempts = 0
        current_folder = os.getcwd()  # Get current folder to create image path later

        image_url = track.get_cover_image(3)
        image_file_type = image_url[-4:]
        image = requests.get(image_url, stream=True)

        if image.status_code == 200:
            print("Album art succesfully downloaded!")

            with open(f"{current_folder}/temp_album{image_file_type}", "wb") as temp_file:
                shutil.copyfileobj(image.raw, temp_file)

                temp_file.close()

            image_path = current_folder + f"/temp_album{image_file_type}"

            return image_path  # Return image path so you can delete the file after use

        # If there's an error but less than 5 get attempts, try again
        elif image.status_code != 200 and get_attempts < 5:
            print("There was an error downloading album art, trying again..")
            get_attempts += 1

            self.get_album_art(track)

        else:
            print(f"Attempted get of artwork for album {track.get_album} failed. Exceeded five attempts.")

    def get_album(self, artist, song):
        return self.network.get_album(artist, song)

    def set_running(self, running):
        self.running = running

    def check_connection(self):
        # check if connection to last fm is up
        pass
