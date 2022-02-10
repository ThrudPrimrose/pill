import constants
import os.path
import matplotlib.pyplot as plt
import numpy as np
from csv import reader
import utility

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
        csv_reader = reader(csv_file)
        for row in csv_reader:
            if "[removed]" in row:
                p_deleted += 1
            p_total += 1

    with open(filepath_comments, "r") as csv_file:
        csv_reader = reader(csv_file)
        for row in csv_reader:
            if "[removed]" in row:
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


p_dels = []
c_dels = []

for (sub, subreddit_short) in constants.subreddits:
    # reset global variables before continuing with new subreddits

    p_dels = []
    c_dels = []
    p_del_acc = 0
    p_tot_acc = 0
    c_del_acc = 0
    c_tot_acc = 0

    for y in constants.years_asc:
        for m in constants.months:
            filepath_posts = subreddit_short + "_data/" + \
                str(subreddit_short) + "_" + "posts" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            filepath_comments = subreddit_short + "_data/" + \
                str(subreddit_short) + "_" + "comments" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            if os.path.isfile(filepath_comments) and os.path.isfile(filepath_posts):
                (p, c) = percentage_deleted(
                    filepath_comments, filepath_posts)

                p_dels.append(p)
                c_dels.append(c)

                print("{:.4f}".format(100 * p) + "% of posts and " + "{:.4f}".format(100 * c) + "% of comments were deleted in: " + str(y) + "." +
                      str(m) + " in " + subreddit_short)
            else:
                print("At least one of: " + filepath_comments +
                      " " + filepath_posts + " don't exist")

                p_dels.append(0.0)
                c_dels.append(0.0)

    print("In total: " + "{:.4f}".format(100 * p_del_acc / p_tot_acc) + "% of posts and " + "{:.4f}".format(100 * c_del_acc / c_tot_acc) + "% of comments were deleted in "
          + subreddit_short)

    ids = list(range(0, len(constants.months) * len(constants.years)))

    fig, ax = plt.subplots(2)

    npx = np.array(ids)
    # print(npx)
    npcomments = np.array(p_dels)
    # print(npcomments)
    npposts = np.array(c_dels)
    # print(npposts)

    # for months that pmaw fails we just set it to the average of left and right
    def clean(c_dels):
        for i in range(len(c_dels)-1):
            if i != 0 and i != len(c_dels)-1 and c_dels[i-1] != 0.0 and c_dels[i] == 0.0 and c_dels[i+1] != 0.0:
                c_dels[i] = (c_dels[i-1] + c_dels[i+1])/2.0

    clean(p_dels)
    clean(c_dels)

    npposts, npx_p = utility.cull_zeros(p_dels, ids)
    npcomments, npx_c = utility.cull_zeros(c_dels, ids)
    ax[0].plot(ids, p_dels)
    fig.suptitle("Amount of posts + comments of a user")
    ax[0].set_title("Deleted posts")
    ax[1].plot(ids, c_dels)
    ax[1].set_title("Deleted comments")

    # OLS fitting for polynomials degree 1 to 5
    # https://www.kite.com/python/answers/how-to-plot-a-polynomial-fit-from-an-array-of-points-using-numpy-and-matplotlib-in-python
    for i in [1, 3, 5]:
        fit_linear_ols = np.polyfit(npx_c, npcomments, i)
        poly = np.poly1d(fit_linear_ols)
        poly_y = poly(npx_c)
        resi = poly_y - npcomments
        s = np.sum(np.absolute(resi))
        ax[1].plot(npx_c, poly_y, label="OLS " +
                   str(i) + " " + "{:.2f}".format(s))

    for i in [1, 3, 5]:
        fit_linear_ols = np.polyfit(npx_p, npposts, i)
        poly = np.poly1d(fit_linear_ols)
        poly_y = poly(npx_p)
        resi = poly_y - npposts
        s = np.sum(np.absolute(resi))
        ax[0].plot(npx_p, poly_y, label="OLS " +
                   str(i) + " " + "{:.2f}".format(s))

    ax[0].legend()
    ax[1].legend()
    # ax[0].set_title('OLS with polynomials of various degrees')
    # ax[0].set_xlabel('month, starting from ' +
    #                 str(starting_date[0]) + "." + str(starting_date[1]) + " + offset")
    # ax[0].set_ylabel('avg number of post + comment per user')
    fig.tight_layout(pad=3.0)

    fig.savefig(subreddit_short + "_deleted.pdf")
