import zope.interface

class IMode(zope.interface.Interface):
    # Run the mode
    async def run(self):
        pass

    # Stop the mode
    async def stop(self):
        pass

    # Display an image
    async def display_image(self, image_path):
        pass
