import pylast
import requests
import shutil
import os
import hashlib
from ReturnCodes import AlbumCoverCodes
from pathlib import Path


class LastFm:
    default_img_hash = "c903567bed54233fdd17377cdef3a344"

    def __init__(self, username, password, api_key, api_secret, running=True):
        print("(LastFm::__init__) Starting LastFm...")
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

        print("(LastFm::__init__) LastFm started!")

    def get_live_album_art(self):
        while True:
            new_track = self.is_playing()
            #print(new_track)

            # If a new song is playing, update current playing
            if new_track != self.current_playing:
                self.current_playing = new_track

                # Nothing is playing
                if self.current_playing is None:
                    print("(LastFm::get_now_playing_album_art) Nothing is playing")

                    return AlbumCoverCodes.NOT_PLAYING

                print(f"(LastFm::get_now_playing_album_art) Now playing - {str(self.current_playing)}")

                # Download new album art
                get_art_success = self.get_album_art(self.current_playing)

                # Failed to download album art
                if get_art_success != AlbumCoverCodes.SUCCESS:
                    return get_art_success

                return AlbumCoverCodes.SUCCESS

    def delete_album_art(self):
        current_dir = os.getcwd()
        files = os.listdir(current_dir)

        for file in files:
            if Path(file).name == "temp_album":
                os.remove(file)

    def is_playing(self):
        try:
            track = self.username.get_now_playing()
            print(track)
        except Exception as e:
            print(e)
            return False
        return track

    def get_album_art(self, track):
        print(f"(LastFm::get_album_art) Getting album art for song {track.get_album()}")
        get_attempts = 0
        current_folder = os.getcwd()  # Get current folder to create image path later

        image_url = track.get_cover_image(3)
        image_file_type = image_url[-4:]

        for i in range(5):
            print(f"(LastFm::get_album_art) Attempt {i}...")
            image = requests.get(image_url, stream=True)

            if image.status_code == 200:
                print("(LastFm::get_album_art) Album art succesfully downloaded!")

                # Save file data to file
                with open(f"{current_folder}/assets/album_art/temp_album{image_file_type}", "wb") as temp_file:
                    shutil.copyfileobj(image.raw, temp_file)

                image_path = current_folder + f"/assets/album_art/temp_album{image_file_type}"

                # If image is default last fm image, return false
                with open(image_path, "rb") as saved_file:
                    md5_hash = hashlib.md5(saved_file.read()).hexdigest()

                if md5_hash == LastFm.default_img_hash:
                    return AlbumCoverCodes.DEFAULT_IMG

                self.current_artwork = image_path
                return AlbumCoverCodes.SUCCESS

            i += 1

        print(f"(LastFm::get_album_art) Attempted get of artwork for album {track.get_album} failed. Exceeded five attempts.")
        self.current_artwork = None
        return AlbumCoverCodes.FAILED_DOWNLOAD

    def get_album(self, artist, song):
        return self.network.get_album(artist, song)

    def set_running(self, running):
        self.running = running

    def check_connection(self):
        # check if connection to last fm is up
        pass
