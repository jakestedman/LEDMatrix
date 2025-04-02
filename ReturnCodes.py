from enum import Enum


class AlbumCoverCodes(Enum):
    SUCCESS = 0
    NOT_PLAYING = 1
    FAILED_DOWNLOAD = 2
    DEFAULT_IMG = 3
