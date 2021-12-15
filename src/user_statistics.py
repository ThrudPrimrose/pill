from csv import DictReader

import constants
import os.path
from pmaw import PushshiftAPI
import datetime as dt
import matplotlib.pyplot as plt


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
total_unique_active_users = set()

(sub, subreddit_short) = constants.subreddits[0]

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
            total_unique_active_users = total_unique_active_users.union(
                unique_active_users)
        else:
            sets.append(set())


def find_user_count(sub, short):
    api = PushshiftAPI()
    limit = 1
    total_users = []

    fname = "fds_data/" + short + "_users.txt"
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


def monthly_difference():
    users_left = [0]
    users_joined = [0]
    users_remained = [0]

    (sub, subreddit_short) = constants.subreddits[0]

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


def last_active_month():
    (sub, subreddit_short) = constants.subreddits[0]
    user_last_posted_at_that_month = [0] * len(sets)

    # print(total_unique_active_users)

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

    # plt.clf()
    fig = plt.figure()
    plt.bar(label_arr, user_last_posted_at_that_month)
    plt.xlabel(
        "A mount of user that wrote their last post or comment at that month")
    # plt.show()

    fig.savefig(subreddit_short + "_last_month_active.pdf")


def footprint():
    (sub, subreddit_short) = constants.subreddits[0]
    userfootprints = [0] * 500000
    id_to_1k = list(range(0, 500000))
    maxfootprint = 0

    local_unique_active_users = total_unique_active_users
    footprint_dict = dict()

    for usr in local_unique_active_users:
        footprint_dict[usr] = 0

    # print(total_unique_active_users)

    for y in constants.years_asc:
        for m in constants.months:
            filepath_posts = "data/" + \
                str(subreddit_short) + "_" + "posts" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            filepath_comments = "data/" + \
                str(subreddit_short) + "_" + "comments" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            with open(filepath_posts, "r") as csv_file:
                csv_reader = DictReader(csv_file)
                for row in csv_reader:
                    footprint_dict[row["author"]] += 1

            with open(filepath_comments, "r") as csv_file:
                csv_reader = DictReader(csv_file)
                for row in csv_reader:
                    footprint_dict[row["author"]] += 1

    for (k, v) in footprint_dict.items():
        userfootprints[v] += 1

    all_values = footprint_dict. values()
    maxfootprint = max(all_values)
    # print(maxfootprint)

    fig = plt.figure()
    idsubset = id_to_1k[1:maxfootprint]
    footprintsubset = userfootprints[1:maxfootprint]

    idsubset50 = id_to_1k[1:50]
    footprintsubset50 = userfootprints[1:50]

    idsubset20 = id_to_1k[1:20]
    footprintsubset20 = userfootprints[1:20]

    fig, ax = plt.subplots(3)
    ax[0].plot(idsubset, footprintsubset)
    # plt.plot(footprintsubset, label="active user count")
    fig.suptitle("Amount of posts + comments of a user")
    # ax[0].xlabel("Amount of posts + comments of a user")
    ax[0].set_title("Y axis: Users that have post N comments + posts")

    ax[1].bar(idsubset50, footprintsubset50)
    # plt.plot(footprintsubset, label="active user count")
    # ax[2].xlabel("Amount of posts + comments of a user")
    # ax[1].set_title("Users that have post N comments + posts")
    # plt.yscale('log')
    #
    # plt.xlabel(
    #    "Footprint = posts + comments")
    # plt.ylabel(" Amount of users that have N posts + comments")
    # plt.set_yscale('log')
    # plt.show()
    ax[2].bar(idsubset20, footprintsubset20)

    fig.savefig(subreddit_short + "_footprint.pdf")


(sub, short) = constants.subreddits[0]
total_users = find_user_count(sub, short)

last_active_month()
footprint()

culled = []

s = "(Total Users) User amount of " + short + ": ["
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

# plt.clf()
fig = plt.figure()
plt.plot(culled, label="user count")
plt.plot(active_users, label="active user count")
plt.plot(left, label="users posted last month but not this month")
plt.plot(joined, label="users posted this month but didnt post last month")
plt.plot(remained, label="user posted both last and this month")

plt.xlabel("month, as a distance from creation of subreddit")
# plt.ylabel("count")
# splt.yscale("log")
plt.legend(loc='best')
# plt.show()

fig.savefig(short + "_user_count.pdf")

# plt.clf()
fig = plt.figure()
plt.plot(active_users, label="active user count")
plt.plot(left, label="users posted last month but not this month")
plt.plot(joined, label="users posted this month but didnt post last month")
plt.plot(remained, label="user posted both last and this month")

plt.xlabel("month, as a distance from creation of subreddit")
plt.legend(loc='best')
# plt.show()

fig.savefig(short + "_user_activity_change.pdf")
