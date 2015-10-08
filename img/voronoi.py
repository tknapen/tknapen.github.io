import numpy
from PIL import Image


NR_DOTS = 1500
X_SIZE = 1600
Y_SIZE = 56


def voronoi(points,shape=(X_SIZE,Y_SIZE)):
    depthmap = numpy.ones(shape,numpy.float)*1e308
    colormap = numpy.zeros(shape,numpy.int)

    def hypot(X,Y):
        return (X-x)**2 + (Y-y)**2

    for i,(x,y) in enumerate(points):
        paraboloid = numpy.fromfunction(hypot,shape)
        colormap = numpy.where(paraboloid < depthmap,i+1,colormap)
        depthmap = numpy.where(paraboloid <
depthmap,paraboloid,depthmap)

    # for (x,y) in points:
    #     colormap[x-1:x+2,y-1:y+2] = 0

    return colormap

def draw_map(colormap):
    shape = colormap.shape

    palette = numpy.array([
            0x00000011,
            0x11111111,
            0x22222211,
            0x33333311,
            0x44444411,
            0x55555511,
            0x66666611,
            0x77777711,
            0x88888811,
            0x99999911,
            0xAAAAAA11,
            0xBBBBBB11,
            0xCCCCCC11,
            0xDDDDDD11,
            0xEEEEEE11,
            0xFFFFFF11,
            ])

    colormap = numpy.transpose(numpy.mod(colormap, palette.shape[0]))
    pixels = numpy.empty(colormap.shape+(4,),numpy.int8)

    pixels[:,:,3] = palette[colormap] & 0xFF
    pixels[:,:,2] = (palette[colormap]>>8) & 0xFF
    pixels[:,:,1] = (palette[colormap]>>16) & 0xFF
    pixels[:,:,0] = (palette[colormap]>>24) & 0xFF

    image = Image.fromstring("RGBA",shape,pixels)
    image.save('voronoi.png')

if __name__ == '__main__':

    a = numpy.random.randint(0,X_SIZE,NR_DOTS)
    b = numpy.random.randint(0,Y_SIZE,NR_DOTS)
    ab = numpy.array([a,b]).T

    draw_map(voronoi(ab))