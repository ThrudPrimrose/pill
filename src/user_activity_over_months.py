import constants
import matplotlib.pyplot as plt
from csv import DictReader

import matplotlib.pyplot as plt
import numpy as np
import os

from numpy import random, exp
import scipy
from scipy import optimize

# residuals with gompertz function


def residual(params, x, data):
    # gompertz function
    # https://en.wikipedia.org/wiki/Gompertz_function
    model = params[0] * exp(- exp(params[1] - params[2]*x))

    return data-model


def activity_over_months(subreddit_short):

    # vector of dictionaries
    # has the form (user_id, #comments + #posts at month i)
    footprint_dicts = []

    # has a set of unique users over subreddit history
    unique_users = set()

    # iterate over months and collect foorprint size
    for y in constants.years_asc:
        for m in constants.months:
            footprint_dict = dict()

            filepath_posts = subreddit_short + "_data_old/" + \
                str(subreddit_short) + "_" + "posts" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            filepath_comments = subreddit_short + "_data_old/" + \
                str(subreddit_short) + "_" + "comments" + \
                "-" + str(y) + "-" + str(m) + ".csv"

            if os.path.exists(filepath_posts):
                with open(filepath_posts, "r") as csv_file:
                    csv_reader = DictReader(csv_file)
                    for row in csv_reader:
                        unique_users.add(row["author"])
                        if row["author"] != "[removed]" and row["author"] != "[deleted]" and row["author"] != "AutoModerator":
                            if row["author"] in footprint_dict:
                                footprint_dict[row["author"]] += 1
                            else:
                                footprint_dict[row["author"]] = 1

            if os.path.exists(filepath_comments):
                with open(filepath_comments, "r") as csv_file:
                    csv_reader = DictReader(csv_file)
                    for row in csv_reader:
                        unique_users.add(row["author"])
                        if row["author"] != "[removed]" and row["author"] != "[deleted]" and row["author"] != "AutoModerator":
                            if row["author"] in footprint_dict:
                                footprint_dict[row["author"]] += 1
                            else:
                                footprint_dict[row["author"]] = 1

            footprint_dicts.append(footprint_dict)

    fig = plt.figure()
    fig, ax = plt.subplots(3)
    fig.suptitle("User activity over months:")

    yavg = [0] * len(constants.years_asc) * len(constants.months)
    user_at = [0] * len(constants.years_asc) * len(constants.months)

    vector = []

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
        vector.append((usr, max(usr_activity_vector)))

    # calculate average foorprint of all active users over months
    for i in range(0, len(constants.years_asc) * len(constants.months)):
        if user_at[i] == 0:
            yavg[i] = 0
        else:
            yavg[i] = int((float(yavg[i]) + 0.5) / float(user_at[i]))

    # print(yavg)
    #(u, v) = max(vector, key=lambda item: item[1])
    #print(u, " ", v)

    x = list(range(len(constants.years_asc) * len(constants.months)))

    params = np.array([1.0, 1.0, 1.0])

    npx = np.array(x)
    npyavg = np.array(yavg)

    # generate experimental uncertainties
    uncertainty = abs(0.16 + random.normal(size=len(x), scale=0.05))

    # print(np.array(x))
    # print(np.shape(np.array(x)))
    # print(np.array(yavg))
    # print(np.shape(np.array(yavg)))

    # polynomial plots
    ax[1].plot(npx, npyavg, label="avg")

    # OLS fitting for polynomials degree 1 to 5
    # https://www.kite.com/python/answers/how-to-plot-a-polynomial-fit-from-an-array-of-points-using-numpy-and-matplotlib-in-python
    for i in [2, 3, 4, 5]:
        fit_linear_ols = np.polyfit(npx, npyavg, i)
        poly = np.poly1d(fit_linear_ols)
        poly_y = poly(npx)
        ax[1].plot(npx, poly_y, label="OLS "+str(i))

    ax[1].legend()

    # gompertz plots
    out = scipy.optimize.least_squares(
        residual, x0=params, loss='soft_l1', args=(npx, npyavg))

    out_ch = scipy.optimize.least_squares(
        residual, x0=params, loss='cauchy', args=(npx, npyavg))

    out_lin = scipy.optimize.least_squares(
        residual, x0=params, args=(npx, npyavg))
    # print(out)
    # print(out.x)

    def gompertz_fit(
        a, params): return params.x[0] * exp(- exp(params.x[1] - params.x[2]*a))

    ax[2].plot(npx, npyavg, label="avg")
    ax[2].plot(npx, gompertz_fit(npx, out_lin), label="gompertz lin")
    ax[2].plot(npx, gompertz_fit(npx, out), label="gompertz soft_l1")
    ax[2].plot(npx, gompertz_fit(npx, out_ch), label="gompertz cauchy")
    ax[2].legend()
    fig.savefig(subreddit_short + "_user_activity_over_months.pdf")


activity_over_months("fds")
