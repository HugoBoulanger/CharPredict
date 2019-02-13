##Projet OPT7 -- Transformation des raw en liste
import pickle
from copy import copy
from time import time

chemin = "C:/Users/Kardas/Pictures/temp AIC/OPT7/wikitext-2-raw/"
cheminSave = "C:/Users/Kardas/Pictures/temp AIC/OPT7/wikitext-2-raw/"

##Fonctions
def savedata(data,path,name):
    """
    INPUT : 
        - object quelconque
        - path : chemin vers lequel sauver les fichiers
        - name : nom du fichier
    OUPUT:
        - [name].data contenant data sous forme binaire
    """
    pickle.dump(data, open(path+f"/{name}.data","wb"))
    
def casseLign(path,listeIni = None,wordlevel = True):
    """
    INPUT:
        - path : chemin d'accès du fichier "raw"
        - listeIni : liste de phrases de départ (remplace le path)
    OUTPUT:
        - dicoChar : dictionnaire caractère->occurence / mot->occurence
        - listLign : liste de str. Chaque item correspond à une phrase du corpus (sans le " . " final)
    """
    dicoChar = {}
    listLign = []
    if(listeIni is None):
        F = open(path,"r", encoding="utf8")
        content = F.readlines()
        ligns = [x.strip().lower() for x in content]
        F.close()
    else:
        ligns = listeIni
    nbl = 0
    nbp = 0
    for lign in ligns:
        nbl += 1
        if((len(lign) > 0) and (lign != "<formula>") and (lign[0] != '=') and (lign[0] != ' ')):
            #on exclu les lignes vides et les titres
            nbp += 1
            if(wordlevel):
                iterator = lign.split(" ")
            else:
                iterator = lign
            for c in iterator:
                if(c in dicoChar):
                    dicoChar[c] += 1
                else:
                    dicoChar[c] = 1
            listLign.extend(lign.split(" . "))
    print(f"{nbl} lignes de fichier\n{nbp} lignes de phrases\n")#{nbf} formules (retirées)\n")
    return dicoChar, listLign

def statDict(dicoChar,lim=50, wordlevel = True):
    """
    INPUT:
        - dicoChar : dictionnaire caractère->occurence
    OUTPUT:
        - dicoReplace : dictionnaire caractère->caractère
    """
    if(wordlevel):
        unk = '__'
    else:
        unk = '♦'
    nbu = 0
    dicoReplace = copy(dicoChar)
    for k in dicoReplace.keys():
        if(dicoChar[k] < lim):
            dicoReplace[k] = unk #caractère / mot inconnu
            nbu += 1
        else:
            dicoReplace[k] = k #caractère / mot connu
    #dicoReplace[unk] = unk
    print(f"statDict : \t{len(dicoReplace.keys())} clés ({len(dicoChar.keys())} originellement)\nToken '<unk>' = '{unk}' (ajouté {nbu} fois)")
    return dicoReplace
    
def mapDico(obj,dico,wordlevel = True):
    """
    INPUTS:
        - obj : liste de str
        - dico : mappeur -> les clés sont présentes dans obj et sont remplacés par les valeurs
    OUTPUT:
        - objMap : itérateur transformé par le dico
    """
    objMap = []
    i = 0
    for elt in obj:
        newElt = []
        if(wordlevel):
            iterator = elt.split(" ")
        else:
            iterator = elt
        for word in iterator:
            if(word in dico):
                newElt.append(dico[word])
            else:
                i+=1
                newElt.append(word)
        if(wordlevel):
            objMap.append(" ".join(newElt))
        else:
            objMap.append("".join(newElt))
    print(f"mapDico : \t{i} clés non-retrouvé")
    return objMap

def deleteSentence(liste,lim = 5, wordlevel = False):
    """
    INPUTS:
        - liste : liste de str
    OUTPUT:
        - newListe : liste de str dont tous les items possèdent au moins 5 éléments
    """
    newListe = []
    i = 0
    for elt in liste:
        if(wordlevel):
            item = elt.split(" ")
        else:
            item = elt
        if(len(item) > lim):
            newListe.append(elt)
        else:
            i+=1
    print(f"deleteSentence : \t{i} item supprimés (taille inférieure à {lim})")
    return newListe

##Preprocess
def printDicoOccur(dico):
    print(f"longeur dico : {len(dico)}")
    for k,v in dico.items():
        print(f"{k} : \t{v}")
    print("voilà, voilà")

def preprocess(loadpath,savepath,name):
    #Preprocess Wordlevel
    dicoMot,listeMot = casseLign(loadpath) #chargement des lignes et des occurences de mots
    print(f"Alphabet Initial : {len(dicoMot.keys())} mots ")
    dicoMotReplace = statDict(dicoMot,lim=100)  #Recherche des mots à tokeniser <unk>
    newlisteMot = deleteSentence(mapDico(listeMot,dicoMotReplace), lim = 1, wordlevel = True) #mapping et suppression des phrases trop courtes (FIN)
    uniqueToken = list(set(dicoMotReplace.values()))
    uniqueToken.sort()
    print(f"Alphabet Final : {len(uniqueToken)} mots \n")
    #Preprocess Characterlevel
    dicoCar,listeCar = casseLign(loadpath, wordlevel = False, listeIni = newlisteMot) #chargement des lignes et des occurences de caractères
    print(f"\nAlphabet Initial : {len(dicoCar.keys())} caractères \n")
    print(sorted(dicoCar.keys()))
    dicoReplace = statDict(dicoCar,lim=100, wordlevel = False) #Recherche des caractères à tokeniser <unk>
    listeFinal = deleteSentence(mapDico(listeCar,dicoReplace,wordlevel = False)) #mapping et suppression des phrases trop courtes (FIN)
    uniqueToken2 = list(set(dicoReplace.values()))
    uniqueToken2.sort()
    print(f"\nAlphabet Final : {len(uniqueToken2)} caractères \n")
    print(uniqueToken2)
    #Saving preprocess
    savedata(listeFinal,savepath,f"listSentence_{name}") #Sauvegarde de la liste des phrases préprocessées
    savedata(dicoReplace,savepath,f"dicoReplace_{name}") #Sauvegarde de l'alphabet de travail
    # print("\n")
    # printDicoOccur(dicoCar)

##Application
top = time()
preprocess(chemin+"wiki.train.raw",cheminSave,"Train")
print(f"Train preprocess : {round(time()-top)}s\n#################################")

top = time()
preprocess(chemin+"wiki.test.raw",cheminSave,"Test")
print(f"Test preprocess : {round(time()-top)}s\n#################################")

top = time()
preprocess(chemin+"wiki.valid.raw",cheminSave,"Valid")
print(f"Valid preprocess : {round(time()-top)}s\n#################################")