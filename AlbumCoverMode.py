import zope.interface
import Config
import os
import logging
from ReturnCodes import AlbumCoverCodes
from IMode import IMode
from LastFm import LastFm
from PIL import Image


@zope.interface.implementer(IMode)
class AlbumCoverMode:
    def __init__(self, matrix):
        logging.info("Initialising album cover mode...")
        self.matrix = matrix
        self.last_fm = LastFm(os.getenv("LAST_FM_USERNAME"), os.getenv("LAST_FM_PASSWORD"),
                              os.getenv("LAST_FM_API_KEY"), os.getenv("LAST_FM_SS"))
        self.running = False
        logging.info("Album cover mode initialised!")

    async def run(self):
        logging.info("Running album cover mode.")
        self.running = True

        # Loop until the song stops playing
        while self.running:
            logging.info(f"run loop")
            album_art_success = await self.last_fm.get_now_playing_album_art(Config.album_search_freq)

            # If new album art has been downloaded, display it on the matrix
            if album_art_success == AlbumCoverCodes.NOT_PLAYING:
                logging.info("Music stopped, exiting album cover mode")
                self.running = False
                self.matrix.Clear()

            elif album_art_success == AlbumCoverCodes.SUCCESS:
                logging.info("Displaying album art...")

                await self.display_image(self.last_fm.current_artwork)

                logging.info("Album art displayed!")

            # If new album art has not been downloaded, display placeholder
            elif album_art_success == AlbumCoverCodes.FAILED_DOWNLOAD:
                # TODO: Add the backup image if the album art was unable to be found
                #       could be just the name of the song, for now skip
                logging.info("Unable to find album art.")

                await self.display_image("assets/doodle_man/picture-not-found-placeholder.jpg")




    async def display_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((self.matrix.width, self.matrix.height), Image.LANCZOS)
        image = image.rotate(180)

        self.matrix.SetImage(image.convert('RGB'))

    async def stop(self):
        pass
