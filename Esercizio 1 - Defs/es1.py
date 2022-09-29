
# Brick
# Revenge
# Emotion
# Person
# Abbiamo annotato le definizioni a mano
# Per ogni parola creiamo un vettore con le parole più usate nelle definizioni da noi date
# dobbiamo vedere quanto le nostre definizioni sono simili, per capire quanto è facile dare definizioni
# assegnamo uno score alle parole
# vediamo le 5 parole + frequenti nella nostra definizione e vediamo quante delle nostre definizioni le contengono
# emotion  person
# revenge  brick

import re
import operator

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
    # HO TOLTO BEING DA STOP WORDS FULL
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
        elif(key == "Person"):
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
        elif(key == "Revenge"):
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
        elif(key == "Brick"):
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
    # print(person_definitions)


# Prendiamo le 5 parole più frequenti, e calcoliamo in ogni frase quante di queste compaiono per avere un punteggio
# di sovrapposizione da 1 a 5
score_person = 0
score_emotion = 0
score_brick = 0
score_revenge = 0


def calculate_overlap_person():
    # ordino il dizionario in base alle frequenze delle parole
    sorted_person_definition = sorted(
        person_definitions.items(), key=operator.itemgetter(1), reverse=True)
    most_used = []
    for i in range(0, 5):
        most_used.append(sorted_person_definition[i])

    global score_person
    for defin in dataset["Person"]:
        defin = defin.lower()
        if most_used[0][0] in defin:
            score_person = score_person + 1
        if most_used[1][0] in defin:
            score_person = score_person + 1
        if most_used[2][0] in defin:
            score_person = score_person + 1
        if most_used[3][0] in defin:
            score_person = score_person + 1
        if most_used[4][0] in defin:
            score_person = score_person + 1
    score_person = score_person/(35*5)
    # print(score_person)


def calculate_overlap_brick():
    # ordino il dizionario in base alle frequenze delle parole
    sorted_brick_definition = sorted(
        brick_definitions.items(), key=operator.itemgetter(1), reverse=True)
    most_used = []
    for i in range(0, 5):
        most_used.append(sorted_brick_definition[i])

    global score_brick
    for defin in dataset["Brick"]:
        defin = defin.lower()
        if most_used[0][0] in defin:
            score_brick = score_brick + 1
        if most_used[1][0] in defin:
            score_brick = score_brick + 1
        if most_used[2][0] in defin:
            score_brick = score_brick + 1
        if most_used[3][0] in defin:
            score_brick = score_brick + 1
        if most_used[4][0] in defin:
            score_brick = score_brick + 1
    score_brick = score_brick/(35*5)
    # print(score_brick)


def calculate_overlap_emotion():
    # ordino il dizionario in base alle frequenze delle parole
    sorted_emotion_definition = sorted(
        emotion_definitions.items(), key=operator.itemgetter(1), reverse=True)
    most_used = []
    for i in range(0, 5):
        most_used.append(sorted_emotion_definition[i])

    global score_emotion
    for defin in dataset["Emotion"]:
        defin = defin.lower()
        if most_used[0][0] in defin:
            score_emotion = score_emotion + 1
        if most_used[1][0] in defin:
            score_emotion = score_emotion + 1
        if most_used[2][0] in defin:
            score_emotion = score_emotion + 1
        if most_used[3][0] in defin:
            score_emotion = score_emotion + 1
        if most_used[4][0] in defin:
            score_emotion = score_emotion + 1
    score_emotion = score_emotion/(35*5)
    # print(score_emotion)


def calculate_overlap_revenge():
    # ordino il dizionario in base alle frequenze delle parole
    sorted_revenge_definition = sorted(
        revenge_definitions.items(), key=operator.itemgetter(1), reverse=True)
    most_used = []
    for i in range(0, 5):
        most_used.append(sorted_revenge_definition[i])
    global score_revenge
    for defin in dataset["Revenge"]:
        defin = defin.lower()
        if most_used[0][0] in defin:
            score_revenge = score_revenge + 1
        if most_used[1][0] in defin:
            score_revenge = score_revenge + 1
        if most_used[2][0] in defin:
            score_revenge = score_revenge + 1
        if most_used[3][0] in defin:
            score_revenge = score_revenge + 1
        if most_used[4][0] in defin:
            score_revenge = score_revenge + 1
    score_revenge = score_revenge/(35*5)
    # print(score_revenge)


if __name__ == '__main__':
    analize_csv()
    process_words()
    calculate_overlap_person()
    calculate_overlap_brick()
    calculate_overlap_emotion()
    calculate_overlap_revenge()
    print("            Astratto   Concreto")
    print("Generico    "+str(round(score_emotion, 2)) +
          "       "+str(round(score_person, 2)))
    print("Specifico   "+str(round(score_revenge, 2)) +
          "       "+str(round(score_brick, 2)))
    print("Valore medio per concreti: " +
          str(round((score_person+score_brick)/2, 2)))
    print("Valore medio per astratti: " +
          str(round((score_emotion+score_revenge)/2, 2)))
