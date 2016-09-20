# gets images off internet

from PIL import Image
from io import BytesIO
import csv, urllib.request
import requests


with open('GZ_clean_abridged.csv') as inputfile:
	data = csv.DictReader(inputfile)
	for line in data:
		response = requests.get("http://skyservice.pha.jhu.edu/DR12/ImgCutout/getjpeg.aspx?ra=" + line['RA'] + "&dec=" + line['DEC'] + "&scale=0.08%20&width=192&height=192")
		img = Image.open(BytesIO(response.content))
		img.save("./images/" + line['OBJID'] + ".png", "PNG")
