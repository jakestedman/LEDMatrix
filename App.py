import Config
import MatrixManager
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from dotenv import load_dotenv

# TODO: Remove all calls to print() when finished, it's slow as fuck
# TODO: Create log file when running to know when bugs occur (pipe output of this)
# TODO: Add gif playing functionality (https://gist.github.com/Simon-Ince/910c440eb34bb722afa90853ecfb1d85)
# TODO: After x seconds of no song playing play slideshow of images (mona lisa etc)
# TODO: If USB stick plugged in automatically put images on display
# TODO: Make Pi launch with app running correctly
# TODO: Refactor to tidy up as needed
# TODO: try catch around http request for when errors occur

if __name__ == '__main__':

    # Load env variables
    load_dotenv()
    print("(App::__main__) Environment variables loaded!")

    print("(App::__main__) Loading matrix configuration...")

    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = Config.matrix_height
    options.cols = Config.matrix_width
    options.chain_length = Config.matrix_chain_length
    options.parallel = Config.matrix_parallel
    options.hardware_mapping = Config.matrix_hardware_mapping
    options.brightness = Config.matrix_brightness

    print("(App::__main__) Matrix configuration loaded!")

    # Initialise matrix
    matrix = MatrixManager.MatrixManager(options)
