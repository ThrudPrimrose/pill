import constants
from csv import DictReader

import matplotlib.pyplot as plt
import numpy as np
import os

from numpy import random, exp
import scipy
import utility
# residuals with gompertz function


def first_n_0(arr):
    a = 0
    for i in arr:
        if i == 0:
            a += 1
        else:
            return a

    return a


def cull_zeros(arr):
    n = first_n_0(arr)
    l = arr[n:]
    npl = np.array(l)
    return npl


def residual_gompertz(params, x, data):
    # gompertz function
    # https://en.wikipedia.org/wiki/Gompertz_function
    model = params[0] * exp(-exp(params[1] - params[2]*x))

    return data-model


def residual_decay_exp(params, x, data):
    # gompertz function
    # https://en.wikipedia.org/wiki/Gompertz_function
    model = params[0] * exp(params[1]*x)

    return data-model


def resi(fun, xs, ys):
    acc = 0.0
    for (x, y) in (xs, ys):
        acc += abs(fun(x) - y)
    return acc


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

            filepath_posts = utility.get_post_path(subreddit_short, y, m)

            filepath_comments = utility.get_comment_path(subreddit_short, y, m)

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

    yavg = [0] * len(constants.years_asc) * len(constants.months)
    user_at = [0] * len(constants.years_asc) * len(constants.months)

    vector = []

    # plot every user as a separate line, if they are not active at that month write 0
    for usr in unique_users:
        usr_activity_vector = []

        for i in range(0, len(constants.years_asc) * len(constants.months)):
            if usr in footprint_dicts[i]:
                yavg[i] += float(footprint_dicts[i][usr])
                usr_activity_vector.append(float(footprint_dicts[i][usr]))
            else:
                usr_activity_vector.append(0)

            user_at[i] = float(len(footprint_dicts[i]))

        # dont plot for every user
        # ax[N].plot(usr_activity_vector)
        vector.append((usr, max(usr_activity_vector)))

    # calculate average foorprint of all active users over months
    for i in range(0, len(constants.years_asc) * len(constants.months)):
        if user_at[i] == 0:
            yavg[i] = 0
        else:
            yavg[i] = float((float(yavg[i]) + 0.5) / float(user_at[i]))

    utility.unzero_fields(yavg)

    # print(yavg)
    # (u, v) = max(vector, key=lambda item: item[1])
    # print(u, " ", v)

    n = first_n_0(yavg)
    # print(n)
    # print(len(yavg))
    yavg = cull_zeros(yavg)
    # print(len(yavg_culled))
    add_month = n % 12
    add_year = n // 12
    starting_date = [constants.years[0] + add_year, 0 + add_month]

    x = list(range(len(constants.years_asc) * len(constants.months) - n))

    params = np.array([1.0, 1.0, 1.0])

    npx = np.array(x)
    npyavg = np.array(yavg)

    # generate experimental uncertainties
    uncertainty = abs(0.16 + random.normal(size=len(x), scale=0.05))

    # print(np.array(x))
    # print(np.shape(np.array(x)))
    # print(np.array(yavg))
    # print(np.shape(np.array(yavg)))
    fig = plt.figure()
    fig, ax = plt.subplots(4, figsize=(10, 10))

    # polynomial plots
    ax[0].plot(npx, npyavg, label="avg")

    # OLS fitting for polynomials degree 1 to 5
    # https://www.kite.com/python/answers/how-to-plot-a-polynomial-fit-from-an-array-of-points-using-numpy-and-matplotlib-in-python
    for i in [2, 3, 4, 5]:
        fit_linear_ols = np.polyfit(npx, npyavg, i)
        poly = np.poly1d(fit_linear_ols)
        poly_y = poly(npx)
        resi = poly_y - npyavg
        s = np.sum(np.absolute(resi))
        ax[0].plot(npx, poly_y, label="OLS "+str(i) + " " + "{:.2f}".format(s))

    ax[0].legend()
    ax[0].set_title('OLS with polynomials of various degrees')
    ax[0].set_xlabel('month, starting from ' +
                     str(starting_date[0]) + "." + str(starting_date[1]) + " + offset")
    ax[0].set_ylabel('avg number of post + comment per user')
    # gompertz plots
    out = scipy.optimize.least_squares(
        residual_gompertz, x0=params, loss='soft_l1', args=(npx, npyavg))

    out_ch = scipy.optimize.least_squares(
        residual_gompertz, x0=params, loss='cauchy', args=(npx, npyavg))

    out_lin = scipy.optimize.least_squares(
        residual_gompertz, x0=params, args=(npx, npyavg))
    # print(out)
    # print(out.x)

    def gompertz_fit(
        a, params): return params.x[0] * exp(- exp(params.x[1] - params.x[2]*a))

    ax[1].plot(npx, npyavg, label="avg")
    resi = gompertz_fit(npx, out_lin) - npyavg
    s = np.sum(np.absolute(resi))
    ax[1].plot(npx, gompertz_fit(npx, out_lin),
               label="gompertz lin " + "{:.2f}".format(s))
    resi = gompertz_fit(npx, out) - npyavg
    s = np.sum(np.absolute(resi))
    ax[1].plot(npx, gompertz_fit(npx, out),
               label="gompertz soft_l1 " + "{:.2f}".format(s))
    resi = gompertz_fit(npx, out_ch) - npyavg
    s = np.sum(np.absolute(resi))
    ax[1].plot(npx, gompertz_fit(npx, out_ch),
               label="gompertz cauchy " + "{:.2f}".format(s))
    ax[1].legend()
    ax[1].set_title('OLS with gompertz function and various loss functions')
    ax[1].set_xlabel('month, starting from ' +
                     str(starting_date[0]) + "." + str(starting_date[1]) + " + offset")
    ax[1].set_ylabel('avg number of post + comment per user')

    out_log = np.polyfit(np.log(npx + 1), npyavg, 1)

    def log_output(x, param): return param[0] * np.log(x) + param[1]

    ax[2].plot(npx + 1, npyavg, label="avg")
    resi = log_output(npx + 1, out_log) - npyavg
    s = np.sum(np.absolute(resi))
    ax[2].plot(npx + 1, log_output(npx + 1, out_log),
               label="log " + "{:.2f}".format(s))
    ax[2].set_xlabel('month, starting from ' +
                     str(starting_date[0]) + "." + str(starting_date[1]) + " + offset")
    ax[2].set_ylabel('avg number of post + comment per user')
    ax[2].set_title('OLS with log transformation on x')
    ax[2].legend()
    # print(out_log)

    # max_el_y = max(npyavg)
    max_el_y = np.argmax(npyavg)
    # print(max_el_y)

    x_left = npx[:max_el_y+1]
    # print(x_left)
    x_right = npx[max_el_y:]
    # print(x_right)
    y_left = npyavg[:max_el_y+1]
    # print(y_left)
    y_right = npyavg[max_el_y:]
    # print(y_right)

    exp_params = [y_left[0], -1.0]

    growth = scipy.optimize.least_squares(
        residual_gompertz, x0=params, loss='soft_l1', args=(x_left, y_left))

    decay_exp = scipy.optimize.least_squares(
        residual_decay_exp, x0=exp_params, loss='soft_l1', args=(x_right, y_right))

    def decay_exp_fit(
        a, params): return params.x[0] * exp(params.x[1]*a)

    ax[3].plot(npx, npyavg, label="avg")
    resi = gompertz_fit(x_left, growth) - y_left
    s = np.sum(np.absolute(resi))
    ax[3].plot(x_left, gompertz_fit(x_left, growth),
               label="growth(gompertz) " + "{:.2f}".format(s))
    resi = decay_exp_fit(x_right, decay_exp) - y_right
    s = np.sum(np.absolute(resi))
    ax[3].plot(x_right, decay_exp_fit(x_right, decay_exp),
               label="decay(exp) " + "{:.2f}".format(s))

    decay_lin = np.polyfit(x_right, y_right, 1)
    poly = np.poly1d(decay_lin)
    poly_y = poly(x_right)
    resi = poly_y - y_right
    s = np.sum(np.absolute(resi))
    ax[3].plot(x_right, poly_y, label="OLS 1 " + "{:.2f}".format(s))

    ax[3].legend()
    ax[3].set_xlabel('month, starting from ' +
                     str(starting_date[0]) + "." + str(starting_date[1]) + " + offset")
    ax[3].set_ylabel('avg number of post + comment per user')
    ax[3].set_title('OLS with living and dying phases')

    fig.tight_layout(pad=3.0)
    # ax[3].plot(npx, out_log, label="avg")
    fig.savefig(subreddit_short + "_user_activity_over_months.pdf")


for (_, sub) in constants.subreddits:
    activity_over_months(sub)
