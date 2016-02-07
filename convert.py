from PIL import Image

def convert(filename) :
    im = Image.open(str(filename) + ".jpg")
    im.save(str(filename) + ".ppm")
    return im
