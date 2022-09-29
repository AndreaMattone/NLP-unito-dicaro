import math
import nltk
import scipy
from nltk.corpus import wordnet as wn
from nltk.corpus import semcor
from nltk.stem import WordNetLemmatizer
import random
Lemmatizer = WordNetLemmatizer()


# Lesk
def lesk_algorithm(word, sentence):
    max_overlap = 0
    best_sense = ""
    # context corrisponde all'inseme delle parole in sentence
    context = sentence
    # print(context)
    synset1 = []
    synset = ""
    for ss in wn.synsets(word):
        signature = ss.definition()
        overlap = overlap(signature.split(), context)
        if (overlap > max_overlap):
            max_overlap = overlap
            best_sense = signature
            synset = ss
    return synset, best_sense


def computeOverlap(signature, context):

    intersec = list(set(signature).intersection(context))
    return len(intersec)


def lem_list(sent):
    return [l.label() if isinstance(l, nltk.tree.Tree) else None for l in sent]


dataset = []
dataset_tag = []


def load_dataset():

    # Prendiamo 50 frasi da semcor
    d = semcor.sents()
    for i in range(0, 50):
        dataset.append(d[i])

    print("50 items selected")
    lesk_correct = 0

    for i in range(0, 50):  # per ogni frase
        print("-------------")
        # associa il senso di wordnet ad ogni parola della frase i
        lem = lem_list(semcor.tagged_sents(tag="sem")[i])
        # print(lem)
        index = len(lem)
        found = False  # quando trovo un nome mi fermo
        for j in range(0, index):
            if (found == False):
                if (str(lem[j]) != 'None'):
                    string = str(lem[j])  # prendo la parola e la pulisco
                    string = string.replace("lem('", "")
                    string = string.replace("')", "")
                    parts = string.split('.')
                    # lem('recommend.v.01.recommend') --> "synset".paroladeltesto
                    # parts[0] = reccommend
                    # parts[1] = v
                    # parts[2] = 01
                    # parts[3] = reccommend # parola del testo che ha "taggato"

                    if (parts[1] == 'n' and parts[3] in dataset[i] and len(parts) > 3):
                        found = True
                        # passo la parola del testo e la frase e lesk mi restituisce
                        res, definition = lesk_algorithm(parts[3], dataset[i])
                        # il synset e la definizione associata
                        print(dataset[i])
                        print("Word: "+parts[3])
                        print("Lesk algorithm: " + str(res))
                        print(parts[0], parts[1], parts[2])
                        syn = str(res)
                        if (syn != ""):
                            syn = syn.replace("Synset('", "")
                            syn = syn.replace("')", "")
                            syn_parts = syn.split('.')
                            # controllo se il synset che ha trovato lesk sia quello corretto
                            if (syn_parts[0] == parts[0] and syn_parts[1] == parts[1] and syn_parts[2] == parts[2]):
                                lesk_correct = lesk_correct+1

        lem.clear()
    print(lesk_correct)


if __name__ == "__main__":
    load_dataset()
