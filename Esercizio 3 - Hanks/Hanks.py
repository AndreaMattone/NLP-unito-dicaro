from traceback import print_list
import spacy
from nltk.corpus import wordnet as wn
from spacy import displacy
from nltk.stem import WordNetLemmatizer
from nltk.wsd import lesk

lemmatizer = WordNetLemmatizer()
nlp = spacy.load('en_core_web_sm')

# Verbo scelto: won
dataset = []


def load_dataset_FULL():
    count = 0
    exit = False
    file_uno = open("dataset.txt", "a")
    with open('wikisent2.txt', 'r', encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split(" ")
            found = False
            for p in parts:
                if (p == "won"):
                    found = True
            if (found == True and exit == False):
                file_uno.write(line)
                count = count + 1


def load_dataset():
    count = 0
    with open('dataset.txt', 'r', encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split("\n")
            dataset.append(parts[0])
            count = count + 1


dict_nsubj = {}
dict_dobj = {}
dict_tot = {}


def dependency_finder():
    count = 0
    dict_text = {}
    dict_pos = {}
    dict_dep = {}
    for d in dataset:
        if (count < 200):
            doc = nlp(d)
            num_arg = 0
            list_text = []
            list_pos = []
            list_dep = []
            for token in doc:
                if (str(token.head) == "won" and (str(token.dep_) == "nsubj" or str(token.dep_) == "dobj")):
                    #print(token.text, token.pos_, token.dep_)
                    num_arg = num_arg + 1
                    list_text.append(token.text)
                    list_pos.append(token.pos_)
                    list_dep.append(token.dep_)
            if (num_arg == 2):
                count = count + 1
                # print(list_text)
                # print(list_pos)
                # print(list_dep)
                lemma1 = lemmatizer.lemmatize((list_text[0]).lower())
                syn1 = lesk(d, lemma1, 'n')
                lemma2 = lemmatizer.lemmatize((list_text[1]).lower())
                syn2 = lesk(d, lemma2, 'n')

                # print(syn1)
                try:
                    if(syn1.lexname() == 'noun.location' and syn2.lexname() == 'noun.event'):
                        print(d)
                    if (syn1.lexname() in dict_nsubj):
                        dict_nsubj[syn1.lexname(
                        )] = dict_nsubj[syn1.lexname()] + 1
                    else:
                        dict_nsubj[syn1.lexname()] = 1
                    if (syn2.lexname() in dict_dobj):
                        dict_dobj[syn2.lexname()] = dict_dobj[syn2.lexname()] + 1
                    else:
                        dict_dobj[syn2.lexname()] = 1
                    comb = syn1.lexname() + "-" + syn2.lexname()
                    if (comb in dict_tot):
                        dict_tot[comb] = dict_tot[comb] + 1
                    else:
                        dict_tot[comb] = 1
                except:
                    pass
                    #print("Supersense non disponibile")
                # print("************")
                list_dep.clear()
                list_pos.clear()
                list_dep.clear()
            num_arg = 0


def print_aggregation():
    dict1 = dict(sorted(dict_nsubj.items(),
                 key=lambda item: item[1], reverse=True))
    print("Frequenza nsbuj:")
    for el in dict1:
        print(el, " "+str(dict1[el]))
    print("*************")
    dict2 = dict(sorted(dict_dobj.items(),
                 key=lambda item: item[1], reverse=True))
    print("Frequenza dobj:")
    for el in dict2:
        print(el, " "+str(dict2[el]))

    dict3 = dict(
        sorted(dict_tot.items(), key=lambda item: item[1], reverse=True))
    print("Frequenza coppie:")
    for el in dict3:
        print(el, " "+str(dict3[el]))


if __name__ == '__main__':
    # crea un file dataset.txt con tutte le frasi con play
    # load_dataset_FULL()
    # carica il contenuto di dataset.txt in dataset
    load_dataset()
    # print(dataset)
    dependency_finder()
    print_aggregation()
