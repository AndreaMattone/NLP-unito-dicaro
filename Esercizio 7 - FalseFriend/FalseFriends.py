import difflib
import nltk
import scipy
from nltk.corpus import wordnet as wn

# due parole simili ma semanticamente differenti
# da un ddsmall nasari prendiamo n coppie di parole simili ma con un punteggio di similarità semantica molto diverso

ddsmallnasari = []


def initialize_ddsmallnasari():
    with open('dd-small-nasari-15.txt', 'r', encoding="utf8") as f:
        lines = f.readlines()
    for line in lines:
        parts = line.split(";")
        key = parts[1].lower()
        ddsmallnasari.append(key)


def clean_string(s):
    s = s.replace('Synset(', '')
    s = s.replace(')', '')
    s = s.replace("'", '')
    return s


def shortest_path_nltk(synset1, synset2):
    sim_path_max = [0, [], []]
    for s1 in synset1:
        s1 = clean_string(s1)
        s1 = wn.synset(s1)
        for s2 in synset2:
            s2 = clean_string(s2)
            s2 = wn.synset(s2)
            sim_path = wn.path_similarity(s1, s2)
            if (sim_path > sim_path_max[0]):
                sim_path_max = [sim_path, s1, s2]
    sim_path_max = [sim_path_max[0], s1, s2]
    return sim_path_max


dict_false_friends = {}


def get_similar_words():
    for i in range(0, 100):
        # print(ddsmallnasari[i])
        word = ddsmallnasari[i]
        list = difflib.get_close_matches(
            ddsmallnasari[i], ddsmallnasari, 3, 0.8)
        list.remove(ddsmallnasari[i])
        # print(list)
        for l in list:
            try:
                synset1 = []
                for ss in wn.synsets(word):
                    synset1.append(str(ss))
                synset2 = []
                for ss in wn.synsets(l):
                    synset2.append(str(ss))
                value = shortest_path_nltk(synset1, synset2)
                # print(value[0])
                if (value[0] < 0.15):
                    dict_false_friends[word] = l
            except:
                pass


if __name__ == '__main__':
    initialize_ddsmallnasari()
    get_similar_words()
    print("False friends: ")
    # for el in dict_false_friends:
    #    print(el)
    #    print(dict_false_friends[el])
    #    print("-----")

    print(dict_false_friends)
