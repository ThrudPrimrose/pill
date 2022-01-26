import os
import sys
import csv
import nltk
import re

from numpy import short
import vocab
import constants
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')


keys = [set(vocab.aliases_11.values()), set(vocab.aliases_21.values()), set(vocab.aliases_31.values()),
        set(vocab.aliases_41.values())]

short_words_not_to_remove = set.union(*keys)


def arr_to_string(arr):
    s = str()
    # s += "["
    if len(arr) > 1:
        for i in range(len(arr)-1):
            s += arr[i]
            s += "; "
        s += arr[len(arr)-1]
        # s += "]"
    elif len(arr) == 1:
        s += arr[0]
        # s += "]"
    # else:
        # s += "[]"
    return s


def string_to_arr(str):
    # "[ ..., a..., "
    # read until first ,
    # skip one offeset, repeat
    if not ";" in str:
        print(str)
    else:
        x = str.split("; ")
        print(x)


# WARNING: possibly inefficient
def abbreviation_mapper(i_map, abbrv_len, vec):
    if len(vec) == 0:
        return vec
    if len(vec) < abbrv_len:
        return vec

    cpy = []

    # i |
    # i, i+1 |
    # a, b, c |
    # i, i+1, i+.., i+abbrv_len-1 -> matches entry in map ->
    for i in range(len(vec) - abbrv_len + 1):
        check_str = str()
        if abbrv_len == 1:
            check_str = vec[i]
        else:
            for j in range(abbrv_len - 1):
                check_str += vec[i + j] + " "
            check_str += vec[i + abbrv_len - 1]

        outp = str()
        if check_str in i_map.keys():
            # e = "found a: "
            # e += check_str
            # e += "\n"
            # sys.stderr.write(e)
            outp = i_map[check_str]
        else:
            outp = vec[i]

        cpy.append(outp)

    # TODO: check for duplication at the last offsets
    for i in range(len(vec) - abbrv_len + 1, len(vec)):
        cpy.append(vec[i])

    return cpy


def alias_mapper(vec):
    t = abbreviation_mapper(vocab.aliases_11, 1, vec)
    t = abbreviation_mapper(vocab.aliases_21, 2, t)
    t = abbreviation_mapper(vocab.aliases_31, 3, t)
    t = abbreviation_mapper(vocab.aliases_41, 4, t)
    return t


def negate(vec):
    for i in range(len(vec)-1):
        if vec[i] == "no" or vec[i] == "not":
            vec[i] = "n"
            vec[i+1] = "-" + vec[i+1]


def clear_len_1(vec):
    res = [i for i in vec if len(i) > 1 and i not in short_words_not_to_remove]
    return res


def clear_len_3(vec):
    res = [i for i in vec if len(i) > 3 and i not in short_words_not_to_remove]
    return res


stop_words = set(stopwords.words('english'))


def tokenize(filepath, body_offsets, outputfile):
    if os.path.exists(filepath):
        file = open(filepath)

        csv_reader = csv.reader(file)

        if os.path.exists(outputfile):
            os.remove(outputfile)

        outf = open(outputfile, "w")
        writer = csv.writer(outf)

        first = True
        for row in csv_reader:
            if first:
                first = False
                writer.writerow(row)
                continue
            else:
                for body_offset in body_offsets:
                    if body_offset >= len(row):
                        continue

                    raw_text = row[body_offset]
                    raw_text = raw_text.strip('"')
                    raw_text = raw_text.strip("'")

                    letters_only = re.sub("[^a-zA-Z]", " ", raw_text)
                    raw_tokens = nltk.word_tokenize(letters_only)

                    for i in range(len(raw_tokens)):
                        raw_tokens[i] = raw_tokens[i].lower()

                    tt = alias_mapper(raw_tokens)
                    tt = clear_len_1(tt)

                    no_stop_words = [w for w in tt if not w in stop_words]
                    negate(no_stop_words)
                    tt = clear_len_3(tt)

                    row[body_offset] = arr_to_string(tt)

                writer.writerow(row)


subs = ["fds", "bps"]

for sub in subs:
    for y in constants.years_asc:
        for m in constants.months:
            for (c, offset) in [("comments", (2, )), ("posts", (2, 3))]:
                inf = sub + "_data_old/" + sub + "_" + c + \
                    "-" + str(y) + "-" + str(m) + ".csv"

                outf = sub + "_data_old/" + sub + "_" + c + "-" + \
                    str(y) + "-" + str(m) + "-tokenized.csv"

                tokenize(inf, offset, outf)
