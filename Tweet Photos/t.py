import os
import subprocess
import io
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont

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


#for i in tweets:
    #print(i.entities)


#for i in tweets[1].entities['media']:
    #print(i['media_url'])

