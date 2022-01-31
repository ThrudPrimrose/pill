from pmaw import PushshiftAPI
import datetime as dt
import constants
import csv
import requests
import os
import logging
import traceback

api = PushshiftAPI()
# local order of saved images
image_id = int(os.getenv('IMAGE_ID_BEGIN', 0))


def pull_posts_from_subreddit(subreddit, short_name, begin, end, limit, suffix):
    # API request for the posts
    posts = api.search_submissions(
        subreddit=subreddit, limit=limit, before=end, after=begin)

    print(f"Retrieved {len(posts)} posts from Pushshift")

    # python considers . as the directory where the program is run so run the program
    # as python3 src/raw_collector.py and the data will be created in the right place
    dirpath = short_name + "_data"
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

    file = open(dirpath + "/" + short_name + "_posts-" + suffix + ".csv",
                "w", newline="", encoding="utf-8")
    writer = csv.writer(file, lineterminator="\n")
    writer.writerow(("post_id", "author", "title", "body", "image"))

    global image_id

    for post in posts:
        # print(post)
        author = post["author"]
        title = post["title"]
        post_id = post["id"]
        body = "Image Only"
        link_image = -1

        if "selftext" in post:
            body = post["selftext"]
            body = body.replace("\n", " ")
            body = body.replace("\r", " ")
            body = body.replace("\t", " ")

        if "url" in post:
            # it can be a video, image or a crosspost
            image_url = post["url"]

            # pull image if it is from i.redd.it
            prefix = "https://i.redd.it/"
            if image_url[0:len(prefix)] == prefix:
                response = requests.get(image_url)
                # in the posts i saw they were always jpg
                if not os.path.exists(dirpath):
                    os.mkdir(dirpath)
                imagepath = dirpath + "/images"
                if not os.path.exists(imagepath):
                    os.mkdir(imagepath)

                image_file = open(dirpath + "/images/" +
                                  str(image_id)+".jpg", "wb")
                image_file.write(response.content)
                image_file.close()
                link_image = image_id
                image_id += 1

        if body == "":
            if link_image == -1:
                body = "[No Access To Image]"
            else:
                body = "[Image Only]"

        writer.writerow(
            [post_id, author, title, body, str(link_image)])


def pull_comments_from_subreddit(subreddit, short_name, begin, end, limit, suffix):
    # API request for the comments
    comments = api.search_comments(
        subreddit=subreddit, limit=limit, before=end, after=begin)

    print(f"Retrieved {len(comments)} comments from Pushshift")

    # python considers . as the directory where the program is run so run the program
    # as python3 src/raw_collector.py and the data will be created in the right place
    dirpath = short_name + "_data"
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

    file = open(dirpath + "/" + short_name + "_comments-" + suffix + ".csv",
                "w", newline="", encoding="utf-8")
    writer = csv.writer(file, lineterminator="\n")
    writer.writerow(("comment_id", "author", "body"))

    for comment in comments:
        author = comment["author"]
        comment_id = comment["id"]
        body = comment["body"]

        body = body.replace("\n", "\\n ")
        writer.writerow([comment_id, author, body])


for y in constants.years:
    for m in constants.months:
        for (sub, short) in [("TheRedPill", "trp")]:
            if m == 12:
                end = int(dt.datetime(y + 1, 1, 1, 0, 0).timestamp())
                begin = int(dt.datetime(y, 12, 1, 0, 0).timestamp())

                suf = str(y) + "-" + str(m)
                print("pulling posts of " + short +
                      ": " + str(y) + "." + str(m))
                try:
                    pull_posts_from_subreddit(
                        sub, short, begin, end, constants.limit, suf)
                except Exception as e:
                    print("SKIP DUE TO ERROR | pulling posts of: " +
                          short + ": " + str(y) + "." + str(m))
                    logging.error(traceback.format_exc())
            else:
                end = int(dt.datetime(y, m + 1, 1, 0, 0).timestamp())
                begin = int(dt.datetime(y, m, 1, 0, 0).timestamp())

                suf = str(y) + "-" + str(m)
                print("pulling posts of " + short +
                      ": " + str(y) + "." + str(m))
                try:
                    pull_posts_from_subreddit(
                        sub, short, begin, end, constants.limit, suf)
                except Exception as e:
                    print("SKIP DUE TO ERROR | pulling posts of: " +
                          short + ": " + str(y) + "." + str(m))
                    logging.error(traceback.format_exc())

for y in constants.years:
    for m in constants.months:
        for (sub, short) in [("TheRedPill", "trp")]:
            if m == 12:
                end = int(dt.datetime(y + 1, 1, 1, 0, 0).timestamp())
                begin = int(dt.datetime(y, 12, 1, 0, 0).timestamp())

                suf = str(y) + "-" + str(m)
                print("pulling comments of " + short +
                      ": " + str(y) + "." + str(m))
                try:
                    pull_comments_from_subreddit(
                        sub, short, begin, end, constants.limit, suf)
                except Exception as e:
                    print("SKIP DUE TO ERROR | pulling comments of: " +
                          short + ": " + str(y) + "." + str(m))
                    logging.error(traceback.format_exc())
            else:
                end = int(dt.datetime(y, m + 1, 1, 0, 0).timestamp())
                begin = int(dt.datetime(y, m, 1, 0, 0).timestamp())

                suf = str(y) + "-" + str(m)
                print("pulling comments of " + short +
                      ": " + str(y) + "." + str(m))
                try:
                    pull_comments_from_subreddit(
                        sub, short, begin, end, constants.limit, suf)
                except Exception as e:
                    print("SKIP DUE TO ERROR | pulling comments of: " +
                          short + ": " + str(y) + "." + str(m))
                    logging.error(traceback.format_exc())
