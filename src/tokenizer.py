import io
import sys
import csv
import nltk
import re
import vocab
nltk.download('punkt')


def arr_to_string(arr):
    s = str()
    #s += "["
    if len(arr) > 1:
        for i in range(len(arr)-1):
            s += arr[i]
            s += ", "
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
    if not "," in str:
        print(str)
    else:
        x = str.split(", ")
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
            e = "found a: "
            e += check_str
            e += "\n"
            sys.stderr.write(e)
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
    t = abbreviation_mapper(vocab.aliases_31, 3, vec)
    t = abbreviation_mapper(vocab.aliases_41, 4, t)
    return t


def tokenize(filepath, body_offset):
    file = open(filepath)
    csv_reader = csv.reader(file)

    first = True
    for row in csv_reader:
        if first:
            first = False
            continue
        else:
            raw_text = row[body_offset]
            # print(raw_text)
            letters_only = re.sub("[^a-zA-Z]", " ", raw_text)
            # print(letters_only)
            raw_tokens = nltk.word_tokenize(letters_only)
            # print(raw_tokens)
            for i in range(len(raw_tokens)):
                raw_tokens[i] = raw_tokens[i].lower()
            # print(raw_tokens)
            # print(arr_to_string(raw_tokens))
            # string_to_arr(arr_to_string(raw_tokens))
            tt = alias_mapper(raw_tokens)
            print(tt)


tokenize("fds_data/fds_comments-2019-12.csv", 2)
