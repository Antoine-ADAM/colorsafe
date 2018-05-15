from colorsafe import ColorSafeImageFiles, InputPages
from PIL import Image
import re

MaxColorVal = 255

def sortStringsNumerically(l):
    def stringSplitByNumbers(x):
        r = re.compile('(\d+)')
        p = r.split(x)
        return [int(y) if y.isdigit() else y for y in p]

    return sorted(l, key=stringSplitByNumbers)

def getPageGrayPixel(pageNum, y, x, pagePixels, grayscale = True):
    pixel = pagePixels[pageNum][x,y]

    if grayscale:
        value = float(pixel)/MaxColorVal
        channels = (value, value, value)
    else:
        channels = (float(pixel[0])/MaxColorVal, float(pixel[1])/MaxColorVal, float(pixel[2])/MaxColorVal)

    return channels

class ColorSafeDecoder:
    def __init__(self, filenames, colorDepth, outfile, saveMetadata):
        #channelsPageList = list()
        self.pagePixels = list()

        for filename in sortStringsNumerically(filenames):
            image = Image.open(filename)
            pixels = image.load()
            self.pagePixels.append(pixels)

            #width = image.size[0]
            #height = image.size[1]

            ## Remove alpha channel, combine into an appropriate channels list.
            #channelsList = list()
            #for y in range(height):
            #    channelsRow = list()
            #    for x in range(width):
            #        pixel = pixels[x,y]

            #        try:
            #            channels = ColorChannels(pixel[0], pixel[1], pixel[2])
            #        except TypeError: # Grayscale
            #            channels = ColorChannels(pixel, pixel, pixel)

            #        channels.multiplyShade([1.0 / MaxColorVal])
            #        channelsRow.append(channels)
            #    channelsList.append(channelsRow)

            #channelsPageList.append(channelsList)

        try:
            len(self.pagePixels[0][0,0])
            grayscale = False
        except:
            grayscale = True

        def getPagePixel(self, pageNum, y, x):
            return getPageGrayPixel(pageNum, y, x, self.pagePixels, grayscale)

        pages = InputPages(len(self.pagePixels), image.size[1], image.size[0])
        pages.pagePixels = self.pagePixels
        pages.getPagePixel = getPagePixel.__get__(pages, pages.__class__)

        csFile = ColorSafeImageFiles()
        data,metadata = csFile.decode(pages, colorDepth)

        print "Decoded successfully with %.2f %% average damage" % (100*csFile.sectorDamageAvg)

        f = open(outfile,"w")
        f.write(data)
        f.close()

        if saveMetadata:
            f = open("metadata.txt","w")
            f.write(metadata)
            f.close()
