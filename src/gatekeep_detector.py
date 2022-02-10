from asyncio import constants
import glob
import pandas as pd
import vocab
import utility
import constants
import os
import matplotlib.pyplot as plt

fig = plt.figure()
plt.title("possible unique gatekeeping posts per subreddit")

for (_, short) in constants.subreddits:
    gatekeeping_possible_posts = []
    print(short)

    for y in constants.years:
        for m in constants.months:
            gatekeeping_counter = 0
            #p_path = utility.get_post_path(short, y, m)
            p_path = utility.get_appended_path(
                short, y, m, True, "lemmetized-img")

            if os.path.exists(p_path):
                df = pd.read_csv(p_path)
                for index, row in df.iterrows():
                    if row['image'] != -1:
                        image_description = str(row["image description"]).split(
                            '; ')
                        body = str(row['body']).split('; ')
                        title = str(row['title']).split('; ')
                        collective = image_description + body + title
                        for word in collective:
                            arr = []
                            if short == "trp" or short == "mr" or short == "pp":
                                arr = vocab.trp_gatekeeping
                            if short == "bps":
                                arr = vocab.bps_gatekeeping
                            if short == "fds":
                                arr = vocab.fds_gatekeeping

                            if word in arr:
                                gatekeeping_counter += 1
                            break
                    else:
                        body = str(row['body']).split('; ')
                        title = str(row['title']).split('; ')
                        collective = body + title
                        ctr = 0
                        for word in collective:
                            if short == "trp" or short == "mr" or short == "pp":
                                arr = vocab.trp_gatekeeping
                            if short == "bps":
                                arr = vocab.bps_gatekeeping
                            if short == "fds":
                                arr = vocab.fds_gatekeeping

                            if word in arr:
                                ctr += 1
                                if ctr >= 2:
                                    gatekeeping_counter += 1
                                    break

            gatekeeping_possible_posts.append(gatekeeping_counter)

    print(gatekeeping_possible_posts)

    plt.plot(gatekeeping_possible_posts, label=short)
    plt.xlabel("month, as a distance from creation of subreddit")
    plt.legend(loc='best')


fig.savefig("gatekeeping.pdf")
