import pytesseract
from PIL import Image
import pandas as pd
import glob
import cv2
import numpy as np
import constants
# change path name (leave /*.csv) to where the data is at


for short in ["trp", "fds", "bps"]:

    path = "data/" + short + "_data" + "/" + short + "_posts*.csv"
    counter = 1
    # reads all the files inside a folder
    for file in glob.glob(path):
        if "lemmetized" in file:
            continue

        # print(file)
        df = pd.read_csv(file)
        # creating a new column
        df["image description"] = ""
        # iterating through the individual files
        for index, row in df.iterrows():
            # if row has an image:
            if row['image'] != -1:
                # change path name (leave  + str(row['image']) + '.jpg') to where your images are at
                image_number_path = "data/" + short + "_data" + '/images/' + \
                    str(row['image']) + '.jpg'
                # print(image_number_path)
                try:
                    # if the image exists in the folder the process will continue
                    Image.open(image_number_path)
                except:
                    print('Image does not exist')
                else:
                    myImage = cv2.imread(image_number_path)
                    # if cv2 can not read it
                    if np.shape(myImage) == ():
                        print('Image did not work')
                    else:
                        # thresholding using opencv, binary thresholding to preprocess the images
                        img = cv2.cvtColor(myImage, cv2.COLOR_BGR2GRAY)
                        ret, thresh = cv2.threshold(
                            img, 120, 255, cv2.THRESH_BINARY)

                        description = ""
                        try:
                            description = pytesseract.image_to_string(
                                thresh, timeout=2.0)
                        except RuntimeError as timeout_error:
                            pass

                        if description == "":
                            description = "[No Text]"
                        # adding the image description to the given row
                        description = description.replace("\n", " ")
                        description = description.replace("\r", " ")
                        description = description.replace("\t", " ")

                        # print(description)
                        df.loc[index, 'image description'] = description
                        row['image description'] = description
        # change path to save updated data frame to wherever you want to
        df.to_csv(file[0:len(file)-4] +
                  '-img' + '.csv', index=False)
        counter += 1
