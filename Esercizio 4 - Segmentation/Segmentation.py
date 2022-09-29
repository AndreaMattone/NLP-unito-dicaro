import nltk
from tracemalloc import stop
from nltk.tokenize.api import TokenizerI
from nltk.corpus import stopwords
import string
import math
from random import randint

from regex import E
dataset = []


def load_dataset():
    with open('dataset.txt', 'r', encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split("\n")
            dataset.append(parts[0])


matrix = {}
stop_words = stopwords.words('english')

list_sentences = []


def validate_matrix():
    for sentence in dataset:
        parts = sentence.split(" ")
        s = ""
        for words in parts:
            word = words.translate(str.maketrans('', '', string.punctuation))
            if(word not in stop_words and word != ""):
                if(word in matrix):
                    matrix[word] = []
                else:
                    matrix[word] = []
                s = s + " "+word
        list_sentences.append(s)

    for el in matrix:
        temp_vect = []
        for sentence in dataset:
            # scorro le frasi
            count_di_el_nella_prima_frase = 0
            parts = sentence.split(" ")
            for words in parts:
                word = words.translate(
                    str.maketrans('', '', string.punctuation))
                if(word == el):
                    count_di_el_nella_prima_frase = count_di_el_nella_prima_frase+1
            #count_di_el_nella_prima_frase = n
            temp_vect.append(count_di_el_nella_prima_frase)
        matrix[el] = temp_vect.copy()

    for elem in matrix:
        print(matrix[elem], elem)


vect_segm = []


def segmentate(num_seg):
    tot_sent = len(dataset)
    split = tot_sent/num_seg
    for i in range(0, num_seg):
        num = math.floor(split*(i+1))
        vect_segm.append(int(num))
    # print(vect_segm)

    # Stampo la divisione
    prec = 0
    for i in range(0, num_seg):
        index = vect_segm[i]
        for elem in matrix:
            array = []
            for j in range(prec, index):
                a = matrix[elem]
                array.append(a[j])
            #print(array, elem, i+1)
            array.clear()
        prec = index

    return 0


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


# calcolo l'overlap tra due frasi vicine all'interno di quel tile
def calculate_overlap(vect_segm_modif):
    list_score = []
    prec = 0
    for i in range(0, len(vect_segm_modif)):
        index = vect_segm_modif[i]
        score = 0
        for j in range(prec, index-1):
            overlap = intersection(list_sentences[j], list_sentences[j+1])
            score = len(overlap)
        list_score.append(score)
        prec = index

    return list_score


def calculate_segmentation():
    print("Segmentation iniziale: "+str(vect_segm))
    list_score_1 = calculate_overlap(vect_segm)
    score_max = 0
    vect_segm_max = vect_segm.copy()
    for i in range(0, len(vect_segm)):
        score_max = score_max + list_score_1[i]
    print("Score iniziale: "+str(score_max))

    for j in range(0, 1000):
        #print("Value random: "+str(dist))
        vect_segm_modif = vect_segm_max.copy()
        for i in range(0, len(vect_segm_modif)-1):
            dist = randint(1, 20)
            op = j % 2
            if (op == 0):
                if (vect_segm_modif[i] - dist > 0):
                    vect_segm_modif[i] = vect_segm_modif[i] - dist
                else:
                    vect_segm_modif[i] = 0
            else:
                if (vect_segm_modif[i] + dist < vect_segm_modif[i+1]):
                    vect_segm_modif[i] = vect_segm_modif[i] + dist
                else:
                    vect_segm_modif[i] = vect_segm_modif[i+1]-1
        list_score_2 = calculate_overlap(vect_segm_modif)
        score = 0
        for i in range(0, len(vect_segm_modif)):
            score = score + list_score_2[i]
        if (score > score_max):
            score_max = score
            vect_segm_max = vect_segm_modif.copy()

        # print(vect_segm_modif)
        # print(score)

    print("********************")
    print("Segmentation finale: "+str(vect_segm_max))
    print("Score finale: "+str(score_max))


if __name__ == '__main__':
    load_dataset()
    count_sentences = len(dataset)
    validate_matrix()
    segmentate(3)
    calculate_segmentation()
