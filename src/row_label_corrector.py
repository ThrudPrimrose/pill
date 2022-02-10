import os
import sys
import fileinput
import constants


def replaceAll(file, searchExp, replaceExp):
    if os.path.isfile(file):

        for line in fileinput.input(file, inplace=1):
            if searchExp in line:
                line = line.replace(searchExp, replaceExp)
            sys.stdout.write(line)


for y in constants.years_asc:
    for m in constants.months:
        for (_, s) in constants.subreddits:
            infp = s + "_data/" + s + "_posts" + \
                "-" + str(y) + "-" + str(m) + ".csv"
            infc = s + "_data/" + s + "_comments" + \
                "-" + str(y) + "-" + str(m) + ".csv"
            replaceAll(infp, "post_id,author,title,upvotes,body,image",
                       "post_id,author,title,body,image")
            replaceAll(infc, "comment_id,author,upvotes,body",
                       "comment_id,author,body")
