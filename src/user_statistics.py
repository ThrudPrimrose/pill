from csv import DictReader
import constants
import os.path
from pmaw import PushshiftAPI
import datetime as dt


def find_unique_active_users(filepath_comments, filepath_posts):
    unique_users = set()

    with open(filepath_posts, "r") as csv_file:
        csv_reader = DictReader(csv_file)
        for row in csv_reader:
            unique_users.add(row["author"])

    with open(filepath_comments, "r") as csv_file:
        csv_reader = DictReader(csv_file)
        for row in csv_reader:
            unique_users.add(row["author"])

    return unique_users


sets = []

for (sub, subreddit_short) in constants.subreddits:
    for y in constants.years_asc:
        for m in constants.months:
            filepath_posts = "data/" + \
                str(subreddit_short) + "_" + "posts" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            filepath_comments = "data/" + \
                str(subreddit_short) + "_" + "comments" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            if os.path.isfile(filepath_comments) and os.path.isfile(filepath_posts):
                unique_active_users = find_unique_active_users(
                    filepath_comments, filepath_posts)

                print(subreddit_short + " had during: " + str(y) + "." +
                      str(m) + " " + str(len(unique_active_users)) + " unique users")

                sets.append(unique_active_users)
            else:
                sets.append(set())


def find_user_count(sub, short):
    api = PushshiftAPI()
    limit = 1
    total_users = []

    fname = "data/" + short + "_users.txt"
    if not os.path.isfile(fname):
        for y in constants.years_asc:
            for m in constants.months:
                if m == 12:
                    end = int(dt.datetime(y + 1, 1, 1, 0, 0).timestamp())
                    begin = int(dt.datetime(y, 12, 1, 0, 0).timestamp())

                    posts = api.search_submissions(
                        subreddit=sub, limit=limit, before=end, after=begin)

                    for p in posts:
                        # print(p)
                        ss = p["subreddit_subscribers"]
                        total_users.append(y)
                        total_users.append(m)
                        total_users.append(ss)
                else:
                    end = int(dt.datetime(y, m + 1, 1, 0, 0).timestamp())
                    begin = int(dt.datetime(y, m, 1, 0, 0).timestamp())

                    posts = api.search_submissions(
                        subreddit=sub, limit=limit, before=end, after=begin)

                    for p in posts:
                        # print(p)
                        ss = p["subreddit_subscribers"]
                        total_users.append(y)
                        total_users.append(m)
                        total_users.append(ss)

        f = open(fname, "w")
        for i in total_users:
            f.write(str(i))
            f.write(",")

        f.write("END")
    else:
        f = open(fname, "r")
        line = f.readline()
        strvec = line.split(",")

        for strint in strvec:
            if strint != "END":
                total_users.append(int(strint))

    return total_users


for (sub, subreddit_short) in constants.subreddits:
    for i in range(len(sets)-1):
        set_pre = sets[i]
        set_next = sets[i+1]

        intersection = set.intersection(set_pre, set_next)
        lost = set_pre.difference(set_next)
        gained = set_next.difference(set_pre)

        staying_user_count = len(intersection)
        lost_user_count = len(lost)
        gained_user_count = len(gained)

        print("(Active Users) From " + str(i) + " to " + str(i+1) + " " + subreddit_short + " has gained " + str(gained_user_count) +
              " has lost " + str(lost_user_count) + " and " + str(staying_user_count) + " remained in the subreddit")


for (sub, short) in constants.subreddits:
    total_users = find_user_count(sub, short)

    s = "(Total Users) User amount of " + short + ": ["
    for i in range(len(total_users)//3):
        users_at_month = total_users[3*i + 2]
        s += str(users_at_month)
        s += ", "
    s += "end]"
    print(s)
