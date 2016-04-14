# send a tweet with a picture and timestamp
# tweet code from tweepy

# takes picture and sends tweet but not on start up yet

import tweepy, picamera, time
import os

#time.sleep(60)


# Consumer keys and access tokens, used for OAuth
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# set up camera and take a picture
# first, get a unique file name to work with
def directory(path,extension):
  list_dir = []
  list_dir = os.listdir(path)
  count = 0
  for file in list_dir:
    if file.endswith(extension): # eg: '.txt'
      count += 1
  return count

# create new camera object
camera = picamera.PiCamera()
#make sure pic is right way round
camera.hflip = True
camera.vflip = True
# add one to the number of images as its the next one
nowTime = str(directory('/home/pi', '.jpg') + 1)
camera.capture(nowTime + '.jpg')
 
# Sample method, used to update a status
photo_path = nowTime + '.jpg'
status = 'Just started up my Raspberry Pi ;)'
api.update_with_media(photo_path, status=status)





