import pylast
import threading
import requests
import shutil
import os


class LastFm(threading.Thread):
    def __init__(self, username, password, api_key, api_secret):
        # initiate a session
        super().__init__()
        password_hash = pylast.md5(password)
        self.network = pylast.LastFMNetwork(api_key=api_key,
                                            api_secret=api_secret,
                                            username=username,
                                            password_hash=password_hash)

        self.username = self.network.get_user(username)

    def get_now_playing(self):
        current_playing = None
        new_track = self.username.get_now_playing()

        # If a new song is playing, update current playing
        if new_track != current_playing:
            current_playing = new_track

            res = current_playing.split(" - ")
            song = res[0]
            artist = res[1]

            print(f"Now playing: {current_playing}")

            return song, artist

    def get_album_art(self, song, artist):
        print(f"Getting album art for song {song} - {artist}")
        get_attempts = 0
        current_folder = os.getcwd()  # Get current folder to create image path later

        album = self.network.get_album(artist, song)
        image_url = album.get_cover_image(4)

        image_file_type = image_url[-4:]
        image = requests.get(image_url, stream=True)

        # If there's an error but less than 5 get attempts, try again
        if image.status_code != 200 and get_attempts < 5:
            print("There was an error downloading album art, trying again..")
            self.get_album_art(song, artist)

            get_attempts += 1

        elif image.status_code == 200:
            print("Album art succesfully downloaded!")

            with open(f"temp_album{image_file_type}", "wb") as temp_file:
                shutil.copyfileobj(image.raw, temp_file)

            image_path = current_folder + f"/temp_album{image_file_type}"

            return image_path  # Return image path so you can delete the file after use

        else:
            print(f"Attempted get of artwork for album {album} failed. Exceeded five attempts.")

    def check_connection(self):
        # check if connection to last fm is up
        pass
