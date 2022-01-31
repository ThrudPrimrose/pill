import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import csv
import pandas as pd
from csv import writer
import glob

def preprocess_image(img):
    img = img.convert('RGBA')
    print('Im in 2')
    pix = img.load()
    print('Im in 3')
    for y in range(img.size[1]):
        print('Im in 4')
        for x in range(img.size[0]):
            print('Im in 5')
            if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
                print('Im in 6')
                pix[x, y] = (0, 0, 0, 255)
                print('Im in 7')
            else:
                pix[x, y] = (255, 255, 255, 255)
                print('Im in 8')
    img = img.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.convert('1')
    img.save('temp2.jpg')
    text = pytesseract.image_to_string(Image.open('temp2.jpg'))
    return text

#doesnt work quite right
path = r"/Users/sezinoztufek/Desktop/data_with_images/to/dir/*.csv"
print('Hey')
for file in glob.glob(path):
    df = pd.read_csv(file)
    df["image description"] = ""
    for index, row in df.iterrows():
        if row['image'] != -1:
            print('heyhey')
            image_number_path = '/Users/sezinoztufek/Desktop/data_with_images/images/' + \
            str(row['image']) + '.jpg'
            try:
                myImage = Image.open(image_number_path)
                print('Im in 1')
            except:
                print('Image does not exist')
            else:
                description = preprocess_image(myImage)
                print(description)
                row['image description'] = description

    df.to_csv(r'/Users/sezinoztufek/Desktop/changed files.csv', index=False)
