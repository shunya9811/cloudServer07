import boto3
import json
from PIL import Image
from PIL import ImageDraw

f_img = 'test.jpg'
in_img = Image.open(f_img)
w, h = in_img.size

r_obj = boto3.client('rekognition')
with open(f_img, 'rb') as file:
  r_out = r_obj.detect_faces(
    Image={'Bytes': file.read()},
    Attributes=['ALL']
  )
  print(json.dumps(r_out, indent=2))

draw = ImageDraw.Draw(in_img)

out_img = Image.new('RGB', (w, h), (256, 256, 256))
for face in r_out['FaceDetails']:
    box = face['BoundingBox']
    left = int(box['Left']*w)
    top = int(box['Top']*h)
    width = int(box['Width']*w)
    height = int(box['Height']*h)

    draw.rectangle([(left, top), (left+width, top+height)], outline='lime', width=2)

in_img.save('show_' + f_img)

