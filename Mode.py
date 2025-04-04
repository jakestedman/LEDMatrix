from abc import ABC, abstractmethod


class Mode(ABC):
    def __init__(self, name):
        self.name = name
        self.matrix = None

    @abstractmethod
    def init(self, matrix):
        pass

    @abstractmethod
    # Run the mode
    async def run(self):
        pass

    @abstractmethod
    # Stop the mode
    async def stop(self):
        pass

    @abstractmethod
    # Display an image
    async def display_image(self, image_path):
        pass
