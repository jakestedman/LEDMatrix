import asyncio
import os
from LastFm import LastFm
from dotenv import load_dotenv


# TODO: LED Matrix goodies
# TODO: Remove all calls to print() when finished, it's slow as fuck

async def run():
    while True:
        new_song = await last_fm.get_now_playing_album_art(5)

        # if new_song == 1
        #   put new image on LED Matrix

        # If not in music listening mode do not search for album art


if __name__ == '__main__':
    # Load env variables
    load_dotenv()

    last_fm = LastFm(os.getenv("LAST_FM_USERNAME"), os.getenv("LAST_FM_PASSWORD"),
                     os.getenv("LAST_FM_API_KEY"), os.getenv("LAST_FM_SS"))

    # Run loop
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run())
    loop.run_forever()
    loop.close()
