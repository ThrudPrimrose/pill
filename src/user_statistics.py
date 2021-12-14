from csv import DictReader
import constants
import os.path


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
    for y in constants.years:
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
                      str(m) + " " + str(len(find_unique_active_users)) + " unique users")

                sets.append(unique_active_users)
            else:
                sets.append(set())
