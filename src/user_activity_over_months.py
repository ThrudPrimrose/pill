import constants
import matplotlib.pyplot as plt
from csv import DictReader


def activity_over_months():
    (_, subreddit_short) = constants.subreddits[0]

    # vector of dictionaries
    # has the form (user_id, #comments + #posts at month i)
    footprint_dicts = []

    # has a set of unique users over subreddit history
    unique_users = set()

    # iterate over months and collect foorprint size
    for y in constants.years_asc:
        for m in constants.months:
            footprint_dict = dict()

            filepath_posts = "data/" + \
                str(subreddit_short) + "_" + "posts" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            filepath_comments = "data/" + \
                str(subreddit_short) + "_" + "comments" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            with open(filepath_posts, "r") as csv_file:
                csv_reader = DictReader(csv_file)
                for row in csv_reader:
                    unique_users.add(row["author"])
                    if row["author"] != "[removed]" and row["author"] != "[deleted]":
                        if row["author"] in footprint_dict:
                            footprint_dict[row["author"]] += 1
                        else:
                            footprint_dict[row["author"]] = 1

            with open(filepath_comments, "r") as csv_file:
                csv_reader = DictReader(csv_file)
                for row in csv_reader:
                    unique_users.add(row["author"])
                    if row["author"] != "[removed]" and row["author"] != "[deleted]":
                        if row["author"] in footprint_dict:
                            footprint_dict[row["author"]] += 1
                        else:
                            footprint_dict[row["author"]] = 1

            footprint_dicts.append(footprint_dict)

    fig = plt.figure()
    fig, ax = plt.subplots(2)
    fig.suptitle("User activity over months:")

    yavg = [0] * len(constants.years_asc) * len(constants.months)
    user_at = [0] * len(constants.years_asc) * len(constants.months)

    # plot every user as a separate line, if they are not active at that month write 0
    for usr in unique_users:
        usr_activity_vector = []

        for i in range(0, len(constants.years_asc) * len(constants.months)):
            if usr in footprint_dicts[i]:
                yavg[i] += footprint_dicts[i][usr]
                usr_activity_vector.append(footprint_dicts[i][usr])
            else:
                usr_activity_vector.append(0)

            user_at[i] = len(footprint_dicts[i])

        ax[0].plot(usr_activity_vector)

    # calculate average foorprint of all active users over months
    for i in range(0, len(constants.years_asc) * len(constants.months)):
        if user_at[i] == 0:
            yavg[i] = 0
        else:
            yavg[i] = int((float(yavg[i]) + 0.5) / float(user_at[i]))

    print(yavg)

    ax[1].plot(yavg)
    fig.savefig(subreddit_short + "_user_activity_over_months.pdf")


activity_over_months()
