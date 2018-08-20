# PhotoLibraryMerger
Merge Apple Photo Libraries
- Scan images from multiple sources.
- Copy only unique version of the image based following EXIF metadata
  - Image Type
  - File Name
  - File Modification Date/Time
  - File Size
  - File Type
  
- Unique images are organise based on File Modification Date/Time:
   - Year
   - Month
   - Day

- Duplicate file name within the same directory are appended with _00* 

###Requirements
 - Python 3
 - PIL - Python Image Library
 - ExifTool from http://owl.phy.queensu.ca/~phil/exiftool/
 
 
###File Supported
