from module import grovepi
import os

# Takes a serie of photos
#
# Params : string, int
def takePhotos(fileName, n):
    for k in range(n):
        os.system("raspistill -n -o \""+fileName+str(k)+"\" -t 1")
    