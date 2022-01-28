from csv import DictReader

import constants
import os.path
from pmaw import PushshiftAPI
import datetime as dt
import matplotlib.pyplot as plt


def gen_user_stats(sub, subreddit_short):
    # calculates the amount of unique active users over the history of subreddit
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

    # find unique active users per month, save it as a vector of sets of unique active users
    sets = []
    # total amount over all months
    total_unique_active_users = set()

    for y in constants.years_asc:
        for m in constants.months:
            filepath_posts = subreddit_short + "_data/" + \
                str(subreddit_short) + "_" + "posts" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            filepath_comments = subreddit_short + "_data/" + \
                str(subreddit_short) + "_" + "comments" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            if os.path.isfile(filepath_comments) and os.path.isfile(filepath_posts):
                unique_active_users = find_unique_active_users(
                    filepath_comments, filepath_posts)

                print(subreddit_short + " had during: " + str(y) + "." +
                      str(m) + " " + str(len(unique_active_users)) + " unique users")

                sets.append(unique_active_users)
                total_unique_active_users = total_unique_active_users.union(
                    unique_active_users)
            else:
                sets.append(set())

    # pull one post from every month to see the total amount of users in a subreddit

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
                            try:
                                ss = p["subreddit_subscribers"]
                                total_users.append(y)
                                total_users.append(m)
                                total_users.append(ss)
                            except Exception as e:
                                total_users.append(y)
                                total_users.append(m)
                                total_users.append(0)

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

    def monthly_difference():
        users_left = [0]
        users_joined = [0]
        users_remained = [0]

        for i in range(len(sets)-1):
            set_pre = sets[i]
            set_next = sets[i+1]

            intersection = set.intersection(set_pre, set_next)
            lost = set_pre.difference(set_next)
            gained = set_next.difference(set_pre)

            staying_user_count = len(intersection)
            lost_user_count = len(lost)
            gained_user_count = len(gained)

            users_left.append(lost_user_count)
            users_remained.append(staying_user_count)
            users_joined.append(gained_user_count)

            print("(Active Users) From " + str(i) + " to " + str(i+1) + " " + subreddit_short + " has gained " + str(gained_user_count) +
                  " has lost " + str(lost_user_count) + " and " + str(staying_user_count) + " remained in the subreddit")

        return (users_left, users_joined, users_remained)

    # for any user that first post at month x, find when they posted their last post

    def last_active_month():
        user_last_posted_at_that_month = [0] * len(sets)

        for usr in total_unique_active_users:
            last_month = 0

            for i in range(len(sets) - 1, -1, -1):
                set_pre = sets[i]

                if usr in set_pre:
                    last_month = i
                    break

            user_last_posted_at_that_month[last_month] += 1

        label_arr = []

        for y in range(len(constants.years_asc)*len(constants.months)):
            label_arr.append(y)

        fig = plt.figure()
        plt.bar(label_arr, user_last_posted_at_that_month)
        plt.xlabel(
            "A mount of user that wrote their last post or comment at that month")

        fig.savefig(subreddit_short + "_last_month_active.pdf")

    # calculates the total footprint of users over all monnths

    def footprint():
        userfootprints = [0] * 500000
        id_to_1k = list(range(0, 500000))
        maxfootprint = 0

        local_unique_active_users = total_unique_active_users
        footprint_dict = dict()

        for usr in local_unique_active_users:
            footprint_dict[usr] = 0

        for y in constants.years_asc:
            for m in constants.months:
                filepath_posts = subreddit_short + "_data/" + \
                    str(subreddit_short) + "_" + "posts" + \
                    "-" + str(y) + "-" + str(m) + ".csv"

                filepath_comments = subreddit_short + "_data/" + \
                    str(subreddit_short) + "_" + "comments" + \
                    "-" + str(y) + "-" + str(m) + ".csv"

                with open(filepath_posts, "r") as csv_file:
                    csv_reader = DictReader(csv_file)
                    for row in csv_reader:
                        if row["author"] != "[removed]" and row["author"] != "[deleted]":
                            footprint_dict[row["author"]] += 1

                with open(filepath_comments, "r") as csv_file:
                    csv_reader = DictReader(csv_file)
                    for row in csv_reader:
                        if row["author"] != "[removed]" and row["author"] != "[deleted]":
                            footprint_dict[row["author"]] += 1

        for (_, v) in footprint_dict.items():
            userfootprints[v] += 1

        all_values = footprint_dict. values()
        maxfootprint = max(all_values)

        fig = plt.figure()
        idsubset = id_to_1k[1:maxfootprint]
        footprintsubset = userfootprints[1:maxfootprint]

        idsubset50 = id_to_1k[1:50]
        footprintsubset50 = userfootprints[1:50]

        idsubset20 = id_to_1k[1:20]
        footprintsubset20 = userfootprints[1:20]

        fig, ax = plt.subplots(3)
        ax[0].plot(idsubset, footprintsubset)
        fig.suptitle("Amount of posts + comments of a user")
        ax[0].set_title("Y axis: Users that have post N comments + posts")
        ax[1].bar(idsubset50, footprintsubset50)
        ax[2].bar(idsubset20, footprintsubset20)

        fig.savefig(subreddit_short + "_footprint.pdf")

    total_users = find_user_count(sub, subreddit_short)

    last_active_month()
    footprint()

    culled = []

    s = "(Total Users) User amount of " + subreddit_short + ": ["
    for i in range(len(total_users)//3):
        users_at_month = total_users[3*i + 2]
        culled.append(users_at_month)
        s += str(users_at_month)
        s += ", "
    s += "end]"
    print(s)

    active_users = []
    for st in sets:
        active_users.append(len(st))

    (left, joined, remained) = monthly_difference()

    fig = plt.figure()
    plt.plot(culled, label="user count")
    plt.plot(active_users, label="active user count")
    plt.plot(left, label="users posted last month but not this month")
    plt.plot(joined, label="users posted this month but didnt post last month")
    plt.plot(remained, label="user posted both last and this month")

    plt.xlabel("month, as a distance from creation of subreddit")
    plt.legend(loc='best')

    fig.savefig(subreddit_short + "_user_count.pdf")

    fig = plt.figure()
    plt.plot(active_users, label="active user count")
    plt.plot(left, label="users posted last month but not this month")
    plt.plot(joined, label="users posted this month but didnt post last month")
    plt.plot(remained, label="user posted both last and this month")

    plt.xlabel("month, as a distance from creation of subreddit")
    plt.legend(loc='best')

    fig.savefig(subreddit_short + "_user_activity_change.pdf")


for (subreddit, subreddit_short) in constants.subreddits:
    gen_user_stats(subreddit, subreddit_short)
