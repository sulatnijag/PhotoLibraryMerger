import piexif
from PIL import Image

img = Image.open('/Users/jag/git_repo/PhotoLibraryMerger/source/ModifiedEXIF.NEF')
img.info()


exif_dict = piexif.load(img.info['exif'])

altitude = exif_dict['GPS'][piexif.GPSIFD.GPSAltitude]
print(altitude)


getEXIF('/Users/jag/git_repo/PhotoLibraryMerger/source/ModifiedEXIF.NEF')

exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] = (140, 1)

import piexif
from PIL import Image

img = Image.open(fname)
exif_dict = piexif.load(img.info['exif'])

altitude = exif_dict['File Modification Date/Time'][piexif.GPSIFD.GPSAltitude]
print(altitude)

exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] = (140, 1)

exif_bytes = piexif.dump(exif_dict)
img.save('_%s' % fname, "jpeg", exif=exif_bytes)