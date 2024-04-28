import asyncio
import os
from PIL import Image
from LastFm import LastFm
from dotenv import load_dotenv


# TODO: LED Matrix goodies
# TODO: Remove all calls to print() when finished, it's slow as fuck

async def run():
    while True:
        new_song = await last_fm.get_now_playing_album_art(5)

        if new_song == True:
            image = last_fm.current_artwork
            # Make image fit our screen.
            image.thumbnail((matrix.width, matrix.height), Image.LANCZOS)

            matrix.SetImage(image.convert('RGB'))

        # If not in music listening mode do not search for album art


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
