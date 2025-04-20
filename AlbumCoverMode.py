import os
import Config
import logging
from time import sleep
from ReturnCodes import AlbumCoverCodes
from Mode import Mode
from LastFm import LastFm
from PIL import Image


class AlbumCoverMode(Mode):
    def __init__(self, name, album_not_playing_event):
        super().__init__(name)
        logging.info("(AlbumCoverMode::__init__) Starting album cover mode...")

        self.album_not_playing_event = album_not_playing_event
        self.last_fm = None

        logging.info("(AlbumCoverMode::__init__) Album cover mode started!")

    def init(self, matrix):
        self.matrix = matrix

        logging.info("(AlbumCoverMode::init) Album cover mode initialised!")

    def run(self):
        self.last_fm = LastFm(os.getenv("LAST_FM_USERNAME"), os.getenv("LAST_FM_PASSWORD"),
                              os.getenv("LAST_FM_API_KEY"), os.getenv("LAST_FM_SS"))


        # Loop until the song stops playing
        while True:
            sleep(Config.album_search_freq)

            # No song is playing, tell the matrix manager and keep checking
            if not self.last_fm.is_playing():
                self.album_not_playing_event.set()
                continue

            # A song is playing, tell the matrix manager
            self.album_not_playing_event.clear()

            album_art_success = self.last_fm.get_live_album_art()

            if album_art_success == AlbumCoverCodes.NOT_PLAYING:
                logging.info("(AlbumCoverMode::run) Exiting album cover mode")
                self.matrix.Clear()
                self.album_not_playing_event.set()

            elif album_art_success == AlbumCoverCodes.SUCCESS:
                logging.info("(AlbumCoverMode::run) Displaying album art...")

                self.display_image(self.last_fm.current_artwork)
                logging.info("(AlbumCoverMode::run) Album art displayed!")

            elif album_art_success == AlbumCoverCodes.FAILED_DOWNLOAD:
                logging.info("(AlbumCoverMode::run) Unable to find album art.")
                self.display_image("assets/doodle_man/picture-not-found-placeholder.jpg")

            elif album_art_success == AlbumCoverCodes.DEFAULT_IMG:
                logging.info("(AlbumCoverMode::run) Default image, ignoring")

                self.display_image("assets/doodle_man/picture-not-found-placeholder.jpg")

    def display_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((self.matrix.width, self.matrix.height), Image.LANCZOS)
        image = image.rotate(180)

        self.matrix.SetImage(image.convert('RGB'))

    def stop(self):
        pass
