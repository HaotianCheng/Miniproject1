import tweepy
from tweepy import OAuthHandler
import json
import wget
import os
import subprocess
import io
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont

consumer_key = 'wgQQ3aqqN04PEA4C7L72mepYb'
consumer_secret = 'gugaf2ho851bjKQUot3AwQ6WpsAVwppqKlWUsKI8mAdC6j9PPu'
access_token = '939914675923423232-6lmQYulypCv4SMjkem9Z3gaFux3KUj8'
access_secret = 'mqEjz8V2qTDKtoI61BAdnefU6BYMyqYN3IJr2l9ZXsOqd'



auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

if(api.verify_credentials):
    print('logged in')




tweets = api.user_timeline(screen_name='NatGeo',
                           count=33, include_rts=False,
                           exclude_replies=True)

tweets_pic=[]

for i in tweets:
    if 'media' in i.entities:
        for pic in i.entities['media']:
            tweets_pic.append(pic['media_url'])

print(tweets_pic)

for pic_url in tweets_pic:
    wget.download(pic_url)

for i,filename in enumerate(os.listdir(os.getcwd())):
    if filename.endswith('.jpg'):
        os.rename(filename,'A'+ str(i).zfill(3)+ ".jpg")

#cloud vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd()+'\\Vision.json'

client = vision.ImageAnnotatorClient()

for i,filename in enumerate(os.listdir(os.getcwd())):
    if filename.endswith('.jpg'):
        with io.open(filename,'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations

        Description = str('Labels:')

        for label in labels:
            print(label.description,end=' ')
            Description=Description+' '+label.description

        pic = Image.open(os.getcwd()+'\\'+filename)
        font_type = ImageFont.truetype("arial.ttf",13)
        draw = ImageDraw.Draw(pic)
        draw.text(xy=(10,10),text=Description[:len(Description)//2],fill=(255,255,255),font=font_type)
        draw.text(xy=(10,30),text=Description[len(Description)//2:],fill=(255,255,255),font=font_type)

        pic.save('B'+'{0:03}'.format(i)+'.jpg')

subprocess.call('ffmpeg.exe -framerate 1 -f image2 -i B%03d.jpg out.avi',shell=True)





