import glob
import pandas as pd
import vocab

gatekeep_counter = 0

for short in ["fds", "bps"]:
    path = short + "_data" + "/" + short + "_posts*.csv"
    for file in glob.glob(path):
        df = pd.read_csv(file)
        for index, row in df.iterrows():
            if row['image'] != -1:
                image_description = row[image_description].split('; ')
                body = row['body'].split('; ')
                collective = image_description + body
                for word in collective:
                    detector = short + '_gatekeeping'
                    if word in vocab.detector:
                        gatekeep_counter += 1
                    break
        gatekeep_counter = 0


                   