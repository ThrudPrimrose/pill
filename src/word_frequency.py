import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import constants
import nltk
import csv
import os
import vocab
import numpy as np


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
        x = i_str.split("; ")
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


full_vocab = [set(vocab.fds_gatekeeping),
              set(vocab.fds_misandry),
              set(vocab.fds_advanced_date_theory),
              set(vocab.blackpill_racism),
              set(vocab.blackpill_cope),
              set(vocab.blackpill_rant),
              set(vocab.blackpill_gatekeeping),
              set(vocab.blackpill_misogyny),
              set(vocab.blackpill_advanced_date_theory),
              set(vocab.trp_gatekeeping),
              set(vocab.trp_advanced_date_theory),
              set(vocab.trp_misagony)]

full_vocab = set.union(*full_vocab)


# matplotlib.interactive(False)
# this script has a bad runtime due to all the operations with words
# so it is a good idea to run 3 isntances of this script for every subreddit at the same time

# for (_, sub) in constants.subreddits:
#    ("TheRedPill", "trp")
#    ("FemaleDatingStrategy", "fds")("BlackPillScience", "bps")
for (_, sub) in [("BlackPillScience", "bps"), ("TheRedPill", "trp"), ("FemaleDatingStrategy", "fds")]:
    print("Calculating word frequence for ", sub)

    glob_tokens = []

    sub_advanced_date_theory = []
    sub_gatekeeping = []
    sub_full = []
    sub_signature = []
    sub_cope = []
    #sw_bps = "chad"
    #sw_fds = "lvm"

    for y in constants.years_asc:
        for m in constants.months:
            tokens = []
            for c in ["comments", "posts"]:
                inf = sub + "_data/" + sub + "_" + c + "-" + \
                    str(y) + "-" + str(m) + "-lemmetized.csv"

                print("Generating word frequency output for ", inf)

                if os.path.exists(inf):
                    file = open(inf)
                    csv_reader = csv.DictReader(file)

                    for row in csv_reader:
                        # print(row)
                        s = row["body"]

                        if c == "posts":
                            l = row["title"]
                            s = s + "; " + l

                        # print("1:")
                        # print(s)
                        v = string_to_arr(s)
                        # print("2:")
                        # print(v)

                        _tokens = purge_bot_words(v)
                        # print("3:")

                        tokens = tokens + _tokens
                        # print(row["body"] + " -> ", v, " -> ", tokens)
                # else:
                    # print(inf + " does not exist")

                    # print(tokens)
                    # tokens = freq_dist(tokens)

            glob_tokens = tokens + glob_tokens
            # print(tokens)
            fdist = nltk.FreqDist(tokens)
            wcount = len(tokens)

            # Percentage of keywords this month, at to a vector to plot it later
            advanced_date_theory_percentage = 0.0
            gatekeeping_percentage = 0.0
            full_percentage = 0.0
            signature_percentage = 0.0
            cope_percentage = 0.0

            for (word, frequency) in fdist.items():
                freq = float(frequency)/float(wcount)
                if sub == "fds" and word in vocab.fds_gatekeeping:
                    gatekeeping_percentage += freq
                if sub == "bps" and word in vocab.blackpill_gatekeeping:
                    gatekeeping_percentage += freq
                if sub == "fds" and word in vocab.fds_advanced_date_theory:
                    advanced_date_theory_percentage += freq
                if sub == "bps" and word in vocab.blackpill_advanced_date_theory:
                    advanced_date_theory_percentage += freq
                if sub == "trp" and word in vocab.trp_gatekeeping:
                    gatekeeping_percentage += freq
                if sub == "trp" and word in vocab.trp_advanced_date_theory:
                    advanced_date_theory_percentage += freq
                if word in full_vocab:
                    full_percentage += freq
                if word == "lvm" and sub == "fds":
                    signature_percentage += freq
                if word == "chad" and sub == "bps":
                    signature_percentage += freq
                if sub == "bps" and (word in vocab.blackpill_cope or word in vocab.blackpill_rant):
                    cope_percentage += freq

            sub_gatekeeping.append(gatekeeping_percentage)
            sub_advanced_date_theory.append(advanced_date_theory_percentage)
            sub_full.append(full_percentage)
            sub_signature.append(signature_percentage)

            if sub == "bps":
                sub_cope.append(cope_percentage)

            # print(u'{};{}'.format(word, float(frequency)/float(wcount)))
            # print(fdist['lvm'])

            matplotlib.interactive(False)
            # plt.ion()
            fig = plt.figure()
            tit = "Most common words of " + sub + \
                " on: " + str(y) + "." + str(m)
            fdist.plot(30, title=tit, cumulative=False,
                       show=False, percents=True)
            inf = sub + "_data/" + sub + "-" + \
                str(y) + "-" + str(m)
            plt.savefig(inf + ".pdf")
            # pdf.savefig(fig)
            # plt.ioff()
            plt.close()

    matplotlib.interactive(False)

    fig = plt.figure()
    tit = "Most common words of " + sub
    glob_fdist = nltk.FreqDist(glob_tokens)
    glob_fdist.plot(40, title=tit, cumulative=False,
                    show=False, percents=True)
    inf = sub + "_data/" + sub
    plt.savefig(inf + ".pdf")

    fig = plt.figure()

    ids = np.array(
        list(range(0, len(constants.months) * len(constants.years))))

    adt_percentage = np.array(sub_advanced_date_theory)
    g_percentage = np.array(sub_gatekeeping)
    f_percentage = np.array(sub_full)
    sig_percentage = np.array(sub_signature)

    plt.plot(ids, adt_percentage, label="advanced date theory vocab percentage")
    plt.plot(ids, g_percentage, label="gatekeeping vocab percentage")
    plt.plot(ids, f_percentage, label="hateful vocab percentage")
    plt.plot(ids, sig_percentage, label="signature word percentage")
    if sub == "bps":
        cpp = np.array(sub_cope)
        plt.plot(ids, cpp, label="cope")
    plt.legend()
    tit = "Terminology percentage of " + sub
    inf = sub + "_data/terminology-" + sub
    plt.savefig(inf + ".pdf")
    # pdf.savefig(fig)
    plt.close()
