import zope.interface
import ReturnCodes
import Config
import os
import logging
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
        logging.info("Album cover mode initialised!")

    async def run(self):
        while True:
            album_art_success = await self.last_fm.get_now_playing_album_art(Config.album_search_freq)

            # If new album art has been downloaded, display it on the matrix
            if album_art_success:
                logging.info("Displaying album art...")

                await self.display_image(self.last_fm.current_artwork)

                logging.info("Album art displayed!")

            # If new album art has not been downloaded, display placeholder
            elif not album_art_success:
                # TODO: Add the backup image if the album art was unable to be found
                #       could be just the name of the song, for now skip
                logging.info("Unable to find album art.")

                await self.display_image("assets/doodle_man/picture-not-found-placeholder.jpg")

            # If music has been stopped, clear matrix
            elif album_art_success == None:
                logging.info("Music stopped, exiting album cover mode.")
                self.matrix.clear()

                break

    async def display_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((self.matrix.width, self.matrix.height), Image.LANCZOS)
        image = image.rotate(180)

        self.matrix.SetImage(image.convert('RGB'))

    async def stop(self):
        pass

    def is_playing(self):
        return self.last_fm.get_now_playing()
