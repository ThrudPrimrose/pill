from csv import DictReader
import constants


def find_unique_posters(filepath):
    unique_users = set()

    with open(filepath, "r") as csv_file:
        csv_reader = DictReader(csv_file)
        for row in csv_reader:
            unique_users.add(row["author"])

    return len(unique_users)


for subreddit_short in constants.subreddit_shorts:
    for y in constants.years:
        for m in constants.months:
            for p_or_c in constants.query_types:
                filepath = "data/" + \
                    str(subreddit_short) + "_" + p_or_c + \
                    "-" + str(y) + "-" + str(m) + ".csv"
                unique_user_count = find_unique_posters(filepath)

                print(subreddit_short + " had during: " + str(y) + "." +
                      str(m) + " " + str(unique_user_count) + " unique " + p_or_c)
