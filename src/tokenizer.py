import os
import sys
import csv
import nltk
import re
import vocab
import constants
nltk.download('punkt')


def arr_to_string(arr):
    s = str()
    #s += "["
    if len(arr) > 1:
        for i in range(len(arr)-1):
            s += arr[i]
            s += "; "
        s += arr[len(arr)-1]
        #s += "]"
    elif len(arr) == 1:
        s += arr[0]
        #s += "]"
    # else:
        #s += "[]"
    return s


def string_to_arr(str):
    #"[ ..., a..., "
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
    res = [i for i in vec if len(i) > 1]
    return res


def clear_len_3(vec):
    res = [i for i in vec if len(i) > 3]
    return res


def tokenize(filepath, body_offset, outputfile):
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
                raw_text = row[body_offset]
                letters_only = re.sub("[^a-zA-Z]", " ", raw_text)
                raw_tokens = nltk.word_tokenize(letters_only)

                for i in range(len(raw_tokens)):
                    raw_tokens[i] = raw_tokens[i].lower()

                tt = alias_mapper(raw_tokens)
                tt = clear_len_1(tt)
                negate(tt)
                tt = clear_len_3(tt)

                row[body_offset] = arr_to_string(tt)
                writer.writerow(row)


subs = ["fds", "bps"]

for sub in subs:
    for (c, offset) in [("comments", 2), ("posts", 3)]:
        for y in constants.years_asc:
            for m in constants.months:
                inf = sub + "_data/" + sub + "_" + c + \
                    "-" + str(y) + "-" + str(m) + ".csv"

                outf = sub + "_data/" + sub + "_" + c + "-" + \
                    str(y) + "-" + str(m) + "-tokenized.csv"

                tokenize(inf, offset, outf)
