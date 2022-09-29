import os
from os import stat

functions_names_fileA = []
functions_names_fileB = []


def get_functions_names(doc):
    if(doc == "codeA.py"):
        with open('valuation/codeA.py') as f:
            lines = f.readlines()
            for line in lines:
                if("def " in line):
                    parts1 = line[4:]
                    parts2 = parts1.split(":")
                    functions_names_fileA.append(parts2[0])
    else:
        with open('valuation/codeB.py') as f:
            lines = f.readlines()
            for line in lines:
                if("def " in line):
                    parts1 = line[4:]
                    parts2 = parts1.split(":")
                    functions_names_fileB.append(parts2[0])


variables_names_fileA = []
variables_names_fileB = []


def get_variables_names(doc):
    if(doc == "codeA.py"):
        with open('valuation/codeA.py') as f:
            lines = f.readlines()
            for line in lines:
                if("=" in line and "==" not in line and "!=" not in line and "#" not in line):
                    parts = line.split("=")
                    if("," in parts[0]):
                        parts = parts[0].split(",")
                        for n in parts:
                            if(n not in variables_names_fileA):
                                add = n.replace(" ", "")
                                variables_names_fileA.append(add)
                    else:
                        if(parts[0] not in variables_names_fileA):
                            add = parts[0].replace(" ", "")
                            variables_names_fileA.append(add)
    else:
        with open('valuation/codeB.py') as f:
            lines = f.readlines()
            for line in lines:
                if("=" in line and "==" not in line and "!=" not in line and "#" not in line):
                    parts = line.split("=")
                    if("," in parts[0]):
                        parts = parts[0].split(",")
                        for n in parts:
                            if(n not in variables_names_fileB):
                                add = n.replace(" ", "")
                                variables_names_fileB.append(add)
                    else:
                        if(parts[0] not in variables_names_fileB):
                            add = parts[0].replace(" ", "")
                            variables_names_fileB.append(add)


# nomi variabili
# nomi funzioni
# lunghezza file
# owner
def check_plagiarism(Icopied):
    plagiarism_score = 0

    if(Icopied == "codeB.py"):
        # variables
        max_val_var = len(variables_names_fileA)  # variabili totali nel file A
        copied_vars = 0  # variabili copiate (uguali)
        for var in variables_names_fileB:
            if(var in variables_names_fileA):
                copied_vars = copied_vars + 1

        if((copied_vars/max_val_var) > 0.7):
            plagiarism_score = plagiarism_score + 1

        # functions
        max_val_fun = len(functions_names_fileA)  # variabili totali nel file A
        copied_fun = 0  # variabili copiate (uguali)
        for fun in functions_names_fileB:
            if(fun in functions_names_fileA):
                copied_fun = copied_fun + 1
        if((copied_fun/max_val_fun) > 0.7):
            plagiarism_score = plagiarism_score + 1

        # check_size
        sizeA = os.path.getsize("valuation/codeA.py")
        sizeB = os.path.getsize("valuation/codeB.py")
        min = sizeA-500
        max = sizeA+500
        if(sizeB < max and sizeB > min):
            plagiarism_score = plagiarism_score+1

        # check_owner
        #ownerA = getpwuid(stat("valuation/codeA.py").st_uid).pw_name
        #ownerB = getpwuid(stat("valuation/codeB.py").st_uid).pw_name
        ownerB = stat("valuation/codeB.py").st_uid
        ownerA = stat("valuation/codeA.py").st_uid
        if(ownerA == ownerB):
            plagiarism_score = plagiarism_score+1
        if(plagiarism_score >= 2):
            return True
        else:
            return False
    else:
        # variables
        max_val_var = len(variables_names_fileB)  # variabili totali nel file A
        copied_vars = 0  # variabili copiate (uguali)
        for var in variables_names_fileA:
            if(var in variables_names_fileB):
                copied_vars = copied_vars + 1
        print(copied_vars/max_val_var)
        if((copied_vars/max_val_var) > 0.7):

            plagiarism_score = plagiarism_score + 1

        # functions
        max_val_fun = len(functions_names_fileB)  # variabili totali nel file A
        copied_fun = 0  # variabili copiate (uguali)
        for fun in functions_names_fileA:
            if(fun in functions_names_fileB):
                copied_fun = copied_fun + 1
        if((copied_fun/max_val_fun) > 0.7):
            plagiarism_score = plagiarism_score + 1

        # check_size
        sizeA = os.path.getsize("valuation/codeA.py")
        sizeB = os.path.getsize("valuation/codeB.py")
        min = sizeB-500
        max = sizeB+500
        if(sizeA < max and sizeA > min):
            plagiarism_score = plagiarism_score+1

        # check_owner
        ownerB = stat("valuation/codeB.py").st_uid
        ownerA = stat("valuation/codeA.py").st_uid
        if(ownerA == ownerB):
            plagiarism_score = plagiarism_score+1
        if(plagiarism_score >= 2):
            return True
        else:
            return False


if __name__ == "__main__":

    get_functions_names("codeA.py")
    get_functions_names("codeB.py")
    get_variables_names("codeA.py")
    get_variables_names("codeB.py")

    # chi ha creato il file dopo è quello che ha copiato
    timeA = os.path.getctime("valuation/codeA.py")
    timeB = os.path.getctime("valuation/codeB.py")
    Icopied = ""
    if(timeA > timeB):
        Icopied = "codeA.py"
    else:
        Icopied = "codeB.py"

    print("L'accusato di plagio è il file "+Icopied)
    res = check_plagiarism(Icopied)
    print("Possibilità di plagio: "+str(res))
