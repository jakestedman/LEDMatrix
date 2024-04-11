import time
import pylast
import requests
import shutil
import os
import asyncio


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
        self.now_playing = None

    async def get_now_playing_album_art(self, timeout):
        # Ability to turn off get now playing
        while self.running:
            # Get now playing every timeout seconds
            await asyncio.sleep(timeout)
            new_track = self.get_now_playing()

            # If a new song is playing, update current playing
            if new_track != self.now_playing:
                self.now_playing = new_track

                # If nothing is playing skip album art get
                if self.now_playing is None:
                    continue

                print(f"Now playing: {str(self.now_playing)}")
                self.get_album_art(self.now_playing)

                return 1

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

        # If there's an error but less than 5 get attempts, try again
        if image.status_code != 200 and get_attempts < 5:
            print("There was an error downloading album art, trying again..")
            get_attempts += 1

            self.get_album_art(track)

        elif image.status_code == 200:
            print("Album art succesfully downloaded!")

            with open(f"temp_album{image_file_type}", "wb") as temp_file:
                shutil.copyfileobj(image.raw, temp_file)

            image_path = current_folder + f"/temp_album{image_file_type}"

            return image_path  # Return image path so you can delete the file after use

        else:
            print(f"Attempted get of artwork for album {track.get_album} failed. Exceeded five attempts.")

    def get_album(self, artist, song):
        return self.network.get_album(artist, song)

    def set_running(self, running):
        self.running = running

    def check_connection(self):
        # check if connection to last fm is up
        pass
