import AlbumCoverMode
import threading
import logging
from rgbmatrix import RGBMatrix, RGBMatrixOptions


# Do as much work as possible in single methods for matrix
class MatrixManager:
    def __init__(self, options):
        logging.info("(MatrixManager::__init__) Initialising matrix manager...")
        self.matrix = RGBMatrix(options=options)
        self.album_not_playing_event = threading.Event()

        # Add and initialise modes here
        album_cover_mode = AlbumCoverMode.AlbumCoverMode("Album cover mode", self.album_not_playing_event)

        # Add modes to list
        self.playing_modes = [album_cover_mode]

        # Initialise the standard modes
        for mode in self.playing_modes:
            logging.info(f"(MatrixManager::__init__) Initialising {mode.name}...")
            mode.init(self.matrix)

        logging.info("(MatrixManager::__init__) Display modes initialised!")

        # Initialise the modes that need separate threads
        matrix_loop_thread = threading.Thread(target=self.run, daemon=True)
        album_cover_thread = threading.Thread(target=album_cover_mode.run, daemon=True)
        album_cover_thread.start()
        matrix_loop_thread.start()

        logging.info("(MatrixManager::__init__) Matrix manager initialised!")

        album_cover_thread.join()
        matrix_loop_thread.join()

    def run(self):
        logging.info("(MatrixManager::run) Running loop")

        # This loop will run all the time, except for when the AlbumCoverMode has detected a song playing
        # in which case the album cover mode will play
        while True:
            self.album_not_playing_event.wait()

            # Add playing modes here

