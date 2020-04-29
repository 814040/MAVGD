import csv 
from dataset_to_db import *
import sqlite3
import time

#read data from IMDbData
pathNameBasics = './IMDbData/name.basics.tsv'
# pathTitleAkas = './IMDbData/title.akas.tsv'
pathTitleBasics = './IMDbData/title.basics.tsv'
# pathTitleCrew = './IMDbData/title.crew.tsv'
# pathTitleEpisode = './IMDbData/title.episode.tsv'
pathTitlePrincipals = './IMDbData/title.principals.tsv'
pathTitleRatings = './IMDbData/title.ratings.tsv'
           

def extractionTitleBasics(cur, conn):
    """"This function :
        - creates date_list
        - creates genres_list
        - fills PELICULA table """
    fh = open(pathTitleBasics)
    reader = csv.reader(fh, delimiter = '\t')
    firstLine = True
    genres_list = []
    date_list = []
    idGenero = 0
    idAno = 0

    for row in reader:
        if firstLine : firstLine = False # Read header
        else :
            idTitulo = int(row[0][2:])
            duracion = row[1] # short, movie or episode
            titulo = row[2]

            # YEAR PROCESSING -- Creation of date_list
            ano = row[5]
            if row[6] == '\\N': 
                fechaEstreno = ano
            else : fechaEstreno = row[6]

            if len(date_list) == 0 :  date_list.append([0, [ano, fechaEstreno]]) # Initialize
            j=0
            while j<len(date_list):
                if date_list[j][1] == [ano, fechaEstreno] : # Verify if this value already exists
                    idAno = j
                    break
                else : j+=1
            if j == len(date_list) : 
                idAno = j
                date_list.append([idAno, [ano, fechaEstreno]]) # If this value does not exist, create new item

            # GENRE PROCESSING -- Creation of genres_list
            genre = row[-1].split(',')[0] # Choose only 1st genre
            k=0
            if len(genres_list) == 0 :  genres_list.append([k, genre]) # Initialize
            while k<len(genres_list):
                if genres_list[k][1] == genre : # Verify if this value already exists
                    idGenero = k
                    break
                else : k+=1
            if k == len(genres_list) : 
                idGenero = k
                genres_list.append([idGenero, genre]) # If this value does not exist, create new item


            # print(peliculaInsert.format(idTitulo, idAno, idGenero, duracion, titulo))  
            # # REGISTER DATA IN PELICULA TABLE  
            cur.execute(peliculaInsert.format(idTitulo, idAno, idGenero, duracion, titulo))
            conn.commit()
    return genres_list, date_list

        

def insertionGenero (cur, conn, genre_list):
    """This function fills GENERO table 
        by values recorded in genre_list (extractionTitleBasics function)"""
    for genre in genre_list :
        idGenero = genre[0]
        genero=genre[1]
        # print(generoInsert.format(idTitulo,genero))
        # REGISTER DATA IN GENERO TABLE
        cur.execute(generoInsert.format(idGenero,genero))
        conn.commit()


def insertionAno(cur, conn, date_list):
    """This function fills ACTOR table 
        by values recorded in date_list (extractionTitleBasics function)"""
    for date in date_list:
        idAno = date[0]
        ano=date[1][0]
        fechaEstreno=date[1][1]
        # print(anoInsert.format(idAno,ano,fechaEstreno))
        # REGISTER ANO IN ACTOR TABLE
        cur.execute(anoInsert.format(idAno,ano,fechaEstreno))
        conn.commit()


def extractionTitlePrincipals(cur, conn):
    """This function fills JUGAR table"""
    fh = open(pathTitlePrincipals)
    reader = csv.reader(fh, delimiter = '\t')
    firstLine = True
    idActor_list = []
    idJugar = 1
    for row in reader:
        if firstLine : firstLine = False # Read header
        else :
            if (row[3]=='actor' or row[3]=='actress'): #only record actors
                idTitulo = int(row[0][2:])
                idActor = int(row[2][2:])
                idActor_list.append(idActor)
                idJugar +=1
                # print(jugarInsert.format(idJugar, idTitulo, idActor))
                # REGISTER DATA IN JUGAR TABLE
                cur.execute(jugarInsert.format(idJugar, idTitulo, idActor))
                conn.commit()
    return idActor_list


def extractionNameBasics(cur, conn, idActor_list):
    """This function fills ACTOR table"""
    fh = open(pathNameBasics)
    reader = csv.reader(fh, delimiter = '\t')
    firstLine = True
    for row in reader:
        if firstLine : firstLine = False # Read header
        else :        
            if(int(row[0][2:]) in idActor_list): #only record actors
                idActor = int(row[0][2:])
                name = row[1].split()
                nombreActor , apellidoActor = name[0], name[1]
                # print(actorInsert.format(idActor, nombreActor, apellidoActor))
                # REGISTER DATA IN ACTOR TABLE
                cur.execute(actorInsert.format(idActor, nombreActor, apellidoActor))
                conn.commit()


def extractionTitleRatings(cur, conn):
    """This function fills CLASIFICACION table"""
    fh = open(pathTitleRatings)
    reader = csv.reader(fh, delimiter = '\t')
    firstLine = True
    for row in reader:
        if firstLine : firstLine = False # Read header
        else :
            idTitulo = int(row[0][2:])
            valuacionMedia = float(row[1])
            nombreVoto = int(row[2])
            # print(clasificacionInsert.format(idTitulo, valuacionMedia, nombreVoto))
            # REGISTER DATA IN CLASIFICACION TABLE
            cur.execute(clasificacionInsert.format(idTitulo, valuacionMedia, nombreVoto))
            conn.commit()




if __name__ == "__main__":
    # Create date_list and genres_list and fill PELICULA table
    genres_list, date_list = extractionTitleBasics(0,0)
    # Fill GENERO table
    insertionGenero(0,0,genres_list)
    # Fill ANO table
    insertionAno(0,0,date_list)
    
    # Create actor_list and fill JUGAR table
    actor_list = extractionTitlePrincipals(0,0)
    # Fill ACTOR table
    extractionNameBasics(0,0,actor_list)

    # Fill CLASIFICACION table
    extractionTitleRatings(0,0)


    