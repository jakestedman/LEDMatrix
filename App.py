import asyncio
import os
import Config
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from LastFm import LastFm
from dotenv import load_dotenv

# TODO: Remove all calls to print() when finished, it's slow as fuck
# TODO: Create log file when running to know when bugs occur (pipe output of this)
# TODO: Add gif playing functionality (https://gist.github.com/Simon-Ince/910c440eb34bb722afa90853ecfb1d85)
# TODO: After x seconds of no song playing play slideshow of images (mona lisa etc)
# TODO: If USB stick plugged in automatically put images on display
# TODO: Make Pi launch with app running correctly
# TODO: Refactor to tidy up as needed
# TODO: try catch around http request for when errors occur

async def run():
    while True:
        album_art_success = await last_fm.get_now_playing_album_art(5)

        # If new album art has been downloaded, display it on the matrix
        if album_art_success == True:
            image = Image.open(last_fm.current_artwork)
            # TODO: Check image type and if it's a gif, play the gif
            # Make image fit our screen.
            image.thumbnail((matrix.width, matrix.height), Image.LANCZOS)
            image = image.rotate(180)
            matrix.SetImage(image.convert('RGB'))

        # If new album art has not been downloaded, display placeholder
        elif album_art_success == False:
            # TODO: Add the backup image if the album art was unable to be found
            #       could be just the name of the song, for now skip
            continue

        # If music has been stopped, clear matrix
        # TODO: Switch to ambient image displaying mode with
        #       pictures of renaissance paintings
        elif album_art_success == None:
            matrix.Clear()

if __name__ == '__main__':
    # Load env variables
    load_dotenv()

    last_fm = LastFm(os.getenv("LAST_FM_USERNAME"), os.getenv("LAST_FM_PASSWORD"),
                     os.getenv("LAST_FM_API_KEY"), os.getenv("LAST_FM_SS"))

    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = Config.matrix_height
    options.cols = Config.matrix_width
    options.chain_length = Config.matrix_chain_length
    options.parallel = Config.matrix_parallel
    options.hardware_mapping = Config.matrix_hardware_mapping

    # Initialise matrix
    matrix = RGBMatrix(options=options)

    # Run loop
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run())
    loop.run_forever()
    loop.close()
