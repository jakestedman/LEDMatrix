import os
from LastFm import LastFm
from dotenv import load_dotenv, dotenv_values

# TODO: Create a way of notifying thread 0 that a new song is playing
# When notified of a new song convert to image type for matrix
# write to LED matrix

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()

    last_fm = LastFm(os.getenv("LAST_FM_USERNAME"), os.getenv("LAST_FM_PASSWORD"),
                     os.getenv("LAST_FM_API_KEY"), os.getenv("LAST_FM_SS"))

    last_fm.start()
    # last_fm.get_now_playing()
    path = last_fm.get_album_art("These Walls", "Kendrick Lamar")

    # Do as much work as possible in single functions for matrix

    # Thread 0 - LED Matrix
    # Thread 1 - Last fm
    # Queue between them
