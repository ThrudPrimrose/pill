from csv import DictReader
import constants
import os.path

p_del_acc = 0
p_tot_acc = 0
c_del_acc = 0
c_tot_acc = 0


def percentage_deleted(filepath_comments, filepath_posts):

    p_deleted = 0
    p_total = 0
    c_deleted = 0
    c_total = 0

    with open(filepath_posts, "r") as csv_file:
        csv_reader = DictReader(csv_file)
        for row in csv_reader:
            if row["body"] == "[removed]":
                p_deleted += 1
            p_total += 1

    with open(filepath_comments, "r") as csv_file:
        csv_reader = DictReader(csv_file)
        for row in csv_reader:
            if row["body"] == "[removed]":
                c_deleted += 1
            c_total += 1

    p_per = 0.0
    c_per = 0.0
    if p_total != 0:
        p_per = p_deleted / p_total
    if c_total != 0:
        c_per = c_deleted / c_total

    global p_del_acc
    global p_tot_acc
    global c_del_acc
    global c_tot_acc

    p_del_acc += p_deleted
    p_tot_acc += p_total
    c_del_acc += c_deleted
    c_tot_acc += c_total

    return (p_per, c_per)


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
                (p, c) = percentage_deleted(
                    filepath_comments, filepath_posts)

                print("{:.4f}".format(p) + "% of posts and " + "{:.4f}".format(c) + "% of comments were deleted in: " + str(y) + "." +
                      str(m) + " in " + subreddit_short)


print("In total: " + "{:.4f}".format(p_del_acc / p_tot_acc) + "% of posts and " + "{:.4f}".format(c_del_acc / c_tot_acc) + "% of comments were deleted in "
      + subreddit_short)
