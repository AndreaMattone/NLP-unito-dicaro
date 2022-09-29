from nltk.corpus import wordnet as wn
import re
import operator
import nltk

# Facciamo la ricerca onomasiologica
# Usando wordnet e le parole contenute nelle definizioni devo cercare di trovare il termine di partenza
# Usiamo le definizioni come input per andare su wordnet e trovare il synset giusto
# Si ragiona per score, avremo un rank dei synset candidati, dare un top 5 synset trovati
#
# per descrivere casa dico "edificio", quindi la def è piu generica, devo prendere gli iponimi delle parole della def
# se le parole della definizione dell'iponimo compaiono anche nella nostra def allora diamo uno score

# { Person: ["a human being", "somthing else", ...] , Emotion: [...], ...}
dataset = {}
stopwords = []


def analize_csv():
    with open('Definizioni.csv', 'r', encoding="utf8") as f:
        lines = f.readlines()
        firstLine = True
        for line in lines:
            if(firstLine == True):
                firstLine = False
            else:
                parts = line.split(",")
                vect = []
                for elem in parts:
                    vect.append(elem)
                vect.pop(0)
                dataset[parts[0]] = vect
    with open('stop_words_FULL.txt', 'r', encoding="utf8") as f:
        lines = f.readlines()
        firstLine = True
        for line in lines:
            s = line.replace("\n", "")
            stopwords.append(s)
    # print(stopwords)
    # print(dataset["Person"])


person_definitions = {}  # { human: 4 , word2: 6 , ...}
emotion_definitions = {}
brick_definitions = {}
revenge_definitions = {}


def process_words():
    for key in dataset:
        if(key == "Emotion"):
            for elem in dataset[key]:
                new_string = re.sub(r'[^\w\s]', '', elem)
                parts = new_string.split(" ")
                for ele in parts:
                    el = ele.lower()
                    if((el != '') and (el not in stopwords)):
                        if(el in emotion_definitions):
                            emotion_definitions[el] = emotion_definitions[el] + 1
                        else:
                            emotion_definitions[el] = 1
        if(key == "Person"):
            for elem in dataset[key]:
                new_string = re.sub(r'[^\w\s]', '', elem)
                parts = new_string.split(" ")
                for ele in parts:
                    el = ele.lower()
                    if((el != '') and (el not in stopwords)):
                        if(el in person_definitions):
                            person_definitions[el] = person_definitions[el] + 1
                        else:
                            person_definitions[el] = 1
        if(key == "Revenge"):
            for elem in dataset[key]:
                new_string = re.sub(r'[^\w\s]', '', elem)
                parts = new_string.split(" ")
                for ele in parts:
                    el = ele.lower()
                    if((el != '') and (el not in stopwords)):
                        if(el in revenge_definitions):
                            revenge_definitions[el] = revenge_definitions[el] + 1
                        else:
                            revenge_definitions[el] = 1
        if(key == "Brick"):
            for elem in dataset[key]:
                new_string = re.sub(r'[^\w\s]', '', elem)
                parts = new_string.split(" ")
                for ele in parts:
                    el = ele.lower()
                    if((el != '') and (el not in stopwords)):
                        if(el in brick_definitions):
                            brick_definitions[el] = brick_definitions[el] + 1
                        else:
                            brick_definitions[el] = 1


def find_overlap_score_emotion(parts):
    score = 0
    for el in parts:
        if(el in emotion_definitions):
            score = score + emotion_definitions[el]

    return score


def try_to_find_emotion():
    sorted_emotion_definition = sorted(
        emotion_definitions.items(), key=operator.itemgetter(1), reverse=True)
    most_used = []
    for i in range(0, 5):
        most_used.append(sorted_emotion_definition[i])

    # print(sorted_emotion_definition)
    My_sysn1 = wn.synsets(most_used[0][0])
    My_sysn2 = wn.synsets(most_used[1][0])
    My_sysn3 = wn.synsets(most_used[2][0])
    My_sysn4 = wn.synsets(most_used[3][0])
    My_sysn5 = wn.synsets(most_used[4][0])

    # print("\n\nThe Hyponyms for the word",
    #     My_sysn1[0], "is:", My_sysn1[0].hyponyms(), "\n\n")

    hyponyms_syn1 = My_sysn1[1].hyponyms()
    hyponyms_syn2 = My_sysn2[1].hyponyms()
    hyponyms_syn3 = My_sysn3[1].hyponyms()
    hyponyms_syn4 = My_sysn4[1].hyponyms()
    hyponyms_syn5 = My_sysn5[1].hyponyms()
    # trovo il syn candidato per la prima lista di iponimi
    max_score1 = 0
    found_sys1 = ""
    for el in hyponyms_syn1:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_emotion(parts)
        if(score > max_score1):
            max_score1 = score
            found_sys1 = el

    max_score2 = 0
    found_sys2 = ""
    for el in hyponyms_syn2:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_emotion(parts)
        if(score > max_score2):
            max_score2 = score
            found_sys2 = el

    max_score3 = 0
    found_sys3 = ""
    for el in hyponyms_syn3:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_emotion(parts)
        if(score > max_score3):
            max_score3 = score
            found_sys3 = el

    max_score4 = 0
    found_sys4 = ""
    for el in hyponyms_syn4:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_emotion(parts)
        if(score > max_score4):
            max_score4 = score
            found_sys4 = el

    max_score5 = 0
    found_sys5 = ""
    for el in hyponyms_syn5:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_emotion(parts)
        if(score > max_score5):
            max_score5 = score
            found_sys5 = el

    return found_sys1, found_sys2, found_sys3, found_sys4, found_sys5


def find_overlap_score_person(parts):
    score = 0
    for el in parts:
        if(el in person_definitions):
            score = score + person_definitions[el]

    return score


def try_to_find_person():
    sorted_person_definition = sorted(
        person_definitions.items(), key=operator.itemgetter(1), reverse=True)
    most_used = []
    for i in range(0, 5):
        most_used.append(sorted_person_definition[i])
    My_sysn1 = wn.synsets(most_used[0][0])
    My_sysn2 = wn.synsets(most_used[1][0])
    My_sysn3 = wn.synsets(most_used[2][0])
    My_sysn4 = wn.synsets(most_used[3][0])
    My_sysn5 = wn.synsets(most_used[4][0])
    hyponyms_syn1 = My_sysn1[0].hyponyms()
    hyponyms_syn2 = My_sysn2[0].hyponyms()
    hyponyms_syn3 = My_sysn3[0].hyponyms()
    hyponyms_syn4 = My_sysn4[0].hyponyms()
    hyponyms_syn5 = My_sysn5[0].hyponyms()
    # trovo il syn candidato per la prima lista di iponimi
    max_score1 = 0
    found_sys1 = ""
    for el in hyponyms_syn1:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_person(parts)
        if(score > max_score1):
            max_score1 = score
            found_sys1 = el

    max_score2 = 0
    found_sys2 = ""
    for el in hyponyms_syn2:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_person(parts)
        if(score > max_score2):
            max_score2 = score
            found_sys2 = el

    max_score3 = 0
    found_sys3 = ""
    for el in hyponyms_syn3:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_person(parts)
        if(score > max_score3):
            max_score3 = score
            found_sys3 = el

    max_score4 = 0
    found_sys4 = ""
    for el in hyponyms_syn4:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_person(parts)
        if(score > max_score4):
            max_score4 = score
            found_sys4 = el

    max_score5 = 0
    found_sys5 = ""
    for el in hyponyms_syn5:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_person(parts)
        if(score > max_score5):
            max_score5 = score
            found_sys5 = el

    return found_sys1, found_sys2, found_sys3, found_sys4, found_sys5


def find_overlap_score_revenge(parts):
    score = 0
    for el in parts:
        if(el in revenge_definitions):
            score = score + revenge_definitions[el]

    return score


def try_to_find_revenge():
    sorted_revenge_definition = sorted(
        revenge_definitions.items(), key=operator.itemgetter(1), reverse=True)
    most_used = []
    for i in range(0, 5):
        most_used.append(sorted_revenge_definition[i])
    My_sysn1 = wn.synsets(most_used[0][0])
    My_sysn2 = wn.synsets(most_used[1][0])
    My_sysn3 = wn.synsets(most_used[2][0])
    My_sysn4 = wn.synsets(most_used[3][0])
    My_sysn5 = wn.synsets(most_used[4][0])
    hyponyms_syn1 = My_sysn1[0].hyponyms()
    hyponyms_syn2 = My_sysn2[0].hyponyms()
    hyponyms_syn3 = My_sysn3[0].hyponyms()
    hyponyms_syn4 = My_sysn4[0].hyponyms()
    hyponyms_syn5 = My_sysn5[0].hyponyms()
    # trovo il syn candidato per la prima lista di iponimi
    max_score1 = 0
    found_sys1 = ""
    for el in hyponyms_syn1:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_revenge(parts)
        if(score > max_score1):
            max_score1 = score
            found_sys1 = el

    max_score2 = 0
    found_sys2 = ""
    for el in hyponyms_syn2:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_revenge(parts)
        if(score > max_score2):
            max_score2 = score
            found_sys2 = el

    max_score3 = 0
    found_sys3 = ""
    for el in hyponyms_syn3:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_revenge(parts)
        if(score > max_score3):
            max_score3 = score
            found_sys3 = el

    max_score4 = 0
    found_sys4 = ""
    for el in hyponyms_syn4:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_revenge(parts)
        if(score > max_score4):
            max_score4 = score
            found_sys4 = el

    max_score5 = 0
    found_sys5 = ""
    for el in hyponyms_syn5:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_revenge(parts)
        if(score > max_score5):
            max_score5 = score
            found_sys5 = el

    return found_sys1, found_sys2, found_sys3, found_sys4, found_sys5


def find_overlap_score_brick(parts):
    score = 0
    for el in parts:
        if(el in brick_definitions):
            score = score + brick_definitions[el]
    return score


def try_to_find_brick():
    sorted_brick_definition = sorted(
        brick_definitions.items(), key=operator.itemgetter(1), reverse=True)
    most_used = []
    for i in range(0, 5):
        most_used.append(sorted_brick_definition[i])
    My_sysn1 = wn.synsets(most_used[0][0])
    My_sysn2 = wn.synsets(most_used[1][0])
    My_sysn3 = wn.synsets(most_used[2][0])
    My_sysn4 = wn.synsets(most_used[3][0])
    My_sysn5 = wn.synsets(most_used[4][0])
    hyponyms_syn1 = My_sysn1[0].hyponyms()
    hyponyms_syn2 = My_sysn2[0].hyponyms()
    hyponyms_syn3 = My_sysn3[0].hyponyms()
    hyponyms_syn4 = My_sysn4[0].hyponyms()
    hyponyms_syn5 = My_sysn5[0].hyponyms()

    # trovo il syn candidato per la prima lista di iponimi
    max_score1 = 0
    found_sys1 = ""
    for el in hyponyms_syn1:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_brick(parts)
        if(score > max_score1):
            max_score1 = score
            found_sys1 = el

    max_score2 = 0
    found_sys2 = ""
    for el in hyponyms_syn2:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_brick(parts)
        if(score > max_score2):
            max_score2 = score
            found_sys2 = el

    max_score3 = 0
    found_sys3 = ""
    for el in hyponyms_syn3:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_brick(parts)
        if(score > max_score3):
            max_score3 = score
            found_sys3 = el

    max_score4 = 0
    found_sys4 = ""
    for el in hyponyms_syn4:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_brick(parts)
        if(score > max_score4):
            max_score4 = score
            found_sys4 = el

    max_score5 = 0
    found_sys5 = ""
    for el in hyponyms_syn5:
        definition = el.definition()
        parts = definition.split(" ")
        score = find_overlap_score_brick(parts)
        if(score > max_score5):
            max_score5 = score
            found_sys5 = el

    return found_sys1, found_sys2, found_sys3, found_sys4, found_sys5


if __name__ == '__main__':
    analize_csv()
    process_words()

    print("Emotion:")
    print(try_to_find_emotion())
    print("*******")
    print("Brick:")
    print(try_to_find_brick())
    print("*******")
    print("Person:")
    print(try_to_find_person())
    print("*******")
    print("Revenge:")
    print(try_to_find_revenge())
