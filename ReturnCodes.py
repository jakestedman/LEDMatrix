import enum


class AlbumCoverCodes(enum):
    SUCCESS = 0
    NOT_PLAYING = 1
    FAILED_DOWNLOAD = 2
    DEFAULT_IMG = 3