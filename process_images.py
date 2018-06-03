# USAGE
# bird_detector.py - take pictures of birds
# set up object detection
# if there's an object find out if it's a bird
# if it's a bird take it's picture

# process_images.py - to be used to help train the model
# load image
# these should all be birds
# if it is take out foreground and save
# is it a blue tit?

# 


# import the necessary packages
import numpy as np
import imutils
import time
import cv2

# will need to cycle through all the images in the folder
img = cv2.imread('examples/03.jpg')
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

# how do we get this of the bird?
rect = (0,0,400,300)

cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
 
tempFilename = 'blue_tit.jpg'
cv2.imwrite(tempFilename,img) 


# cleanup the camera and close any open windows
cv2.destroyAllWindows()
