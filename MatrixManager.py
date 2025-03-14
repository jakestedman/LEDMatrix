import logging
import asyncio
import AlbumCoverMode
from rgbmatrix import RGBMatrix, RGBMatrixOptions


# Do as much work as possible in single methods for matrix
class MatrixManager:
    def __init__(self, options):
        self.matrix = RBGMatrix(options)
        self.album_cover_mode = AlbumCoverMode.AlbumCoverMode(self.matrix)

        # add more modes as needed
        logging.info("Matrix manager initialised!")

    def start(self):
        logging.info("Starting matrix loop...")
        # Run loop
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.run())
        loop.run_forever()
        loop.close()

    async def run(self):
        logging.info("Running loop.")
        if self.album_cover_mode.is_playing():
            await self.album_cover_mode.run()

