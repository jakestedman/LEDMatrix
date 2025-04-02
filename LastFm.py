import pylast
import requests
import shutil
import os
import logging
import asyncio
import hashlib
from ReturnCodes import AlbumCoverCodes
from pathlib import Path


class LastFm:
    default_img_hash = "c903567bed54233fdd17377cdef3a344"

    def __init__(self, username, password, api_key, api_secret, running=True):
        logging.info("Initialising LastFm...")

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

        logging.info("LastFm initialised!")

    async def get_now_playing_album_art(self, timeout):
        # Ability to turn off get now playing
        while self.running:
            logging.info(f"get_now_playing_album_art loop")
            # Get now playing every timeout seconds
            await asyncio.sleep(timeout)
            new_track = self.get_now_playing()
            logging.info(f"new_track: {new_track}")

            while not new_track:
                new_track = self.get_now_playing()
                logging.info(f"new_track: {new_track}")
            # If a new song is playing, update current playing
            if new_track != self.current_playing:
                self.current_playing = new_track

                # Nothing is playing
                if self.current_playing is None:
                    return AlbumCoverCodes.NOT_PLAYING

                logging.info(f"Now playing: {str(self.current_playing)}")

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

    def get_now_playing(self):
        try:
            track = self.username.get_now_playing()
        except Exception as e: 
            logging.info(e)
            return False
        return track

    def get_album_art(self, track):
        logging.info(f"Getting album art for song {track.get_album()}")
        get_attempts = 0
        current_folder = os.getcwd()  # Get current folder to create image path later

        image_url = track.get_cover_image(3)
        image_file_type = image_url[-4:]

        for i in range(5):
            logging.info(f"Attempt {i}...")
            image = requests.get(image_url, stream=True)

            if image.status_code == 200:
                logging.info("Album art succesfully downloaded!")

                # Save file data to file
                with open(f"{current_folder}/assets/album_art/temp_album{image_file_type}", "wb") as temp_file:
                    shutil.copyfileobj(image.raw, temp_file)

                image_path = current_folder + f"/assets/album_art/temp_album{image_file_type}"

                # If image is default last fm image, return false
                with open(image_path, "rb") as saved_file:
                    md5_hash = hashlib.md5(saved_file.read()).hexdigest()

                if md5_hash == LastFm.default_img_hash:
                    logging.info(f"Album art for track doesn't exist.")

                    return AlbumCoverCodes.DEFAULT_IMG
                self.current_artwork = image_path
                return AlbumCoverCodes.SUCCESS

            i += 1

        logging.info(f"Attempted get of artwork for album {track.get_album} failed. Exceeded five attempts.")
        return AlbumCoverCodes.FAILED_DOWNLOAD

    def get_album(self, artist, song):
        return self.network.get_album(artist, song)

    def set_running(self, running):
        self.running = running

    def check_connection(self):
        # check if connection to last fm is up
        pass
