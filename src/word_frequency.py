import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import constants
import nltk
import csv
import os


subs = ["fds", "bps"]


def string_to_arr(i_str):
    # "[ ..., a..., "
    # read until first ,
    # skip one offeset, repeat
    if i_str is None:
        return []

    if not ";" in i_str:
        # print(str)
        return [i_str]
    else:
        x = str.split("; ")
        return x


def freq_dist(tokens):
    # Calculate frequency distribution
    fdist = nltk.FreqDist(tokens)

    fdist.plot(50)
    # Output top 50 words
    for word, frequency in fdist.most_common(50):
        print(u'{};{}'.format(word, frequency))


words_to_remove = [";", "", "removed", "deleted", "thanks"]


def purge_bot_words(tokens):
    res = [i for i in tokens if not i in words_to_remove]
    return res


# matplotlib.interactive(False)

for sub in subs:
    pdf = matplotlib.backends.backend_pdf.PdfPages(
        sub + "_frequence_output.pdf")
    glob_tokens = []

    for y in constants.years_asc:
        for m in constants.months:
            tokens = []
            for (c, offset) in [("comments", 2), ("posts", 3)]:
                inf = sub + "_data/" + sub + "_" + c + "-" + \
                    str(y) + "-" + str(m) + "-tokenized.csv"

                if os.path.exists(inf):
                    file = open(inf)
                    csv_reader = csv.DictReader(file)

                    for row in csv_reader:
                        # print(row)
                        s = row["body"]
                        # print("1:")
                        # print(s)
                        v = string_to_arr(s)
                        # print("2:")
                        # print(v)

                        _tokens = purge_bot_words(v)
                        # print("3:")
                        # print(_tokens)

                        tokens = tokens + _tokens
                # else:
                    # print(inf + " does not exist")

                    # print(tokens)
                    # tokens = freq_dist(tokens)

            globa_tokens = tokens + glob_tokens
            fdist = nltk.FreqDist(tokens)

            matplotlib.interactive(False)
            # plt.ion()
            fig = plt.figure()
            tit = "Most common words of " + sub + \
                " on: " + str(y) + "." + str(m)
            fdist.plot(30, title=tit, cumulative=False,
                       show=False, percents=True)
            inf = sub + "_data/" + sub + "-" + \
                str(y) + "-" + str(m)
            plt.savefig(inf + ".png")
            pdf.savefig(fig)
            # plt.ioff()
            plt.close()

    matplotlib.interactive(False)

    fig = plt.figure()
    tit = "Most common words of " + sub
    fdist.plot(40, title=tit, cumulative=False,
               show=False, percents=True)
    inf = sub + "_data/" + sub
    plt.savefig(inf + ".png")
    pdf.savefig(fig)
    plt.close()
