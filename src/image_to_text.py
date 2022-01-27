import pytesseract
from PIL import Image
import csv
import pandas as pd
from csv import writer
import glob
from csv import DictReader

path = r"/Users/sezinoztufek/Desktop/data_with_images/*.csv"

for file in glob.glob(path):
   df = pd.read_csv(file)
   df["image description"] = ""
   for index, row in df.iterrows():
        if row['image'] != -1:
            image_number_path = '/Users/sezinoztufek/Desktop/data_with_images/images/' + str(row['image']) + '.jpg'
            myImage = Image.open(image_number_path)
            row['image description'] = pytesseract.image_to_string(myImage)

