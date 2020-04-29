#import pandas as pd
import psycopg2
from dataset_to_db import *
from data_extraction import *


def create_database():
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=insertdbname user=insertuser password=insertpassword")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS insertdbname ")
    cur.execute("CREATE DATABASE insertdbname WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to the database
    conn = psycopg2.connect("host=127.0.0.1 dbname=insertdbname user=insertuser password=insertpassword")
    cur = conn.cursor()
    
    return cur, conn

def drop_tables(cur, conn):
    for query in drop_all_tables:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_all_tables:
        cur.execute(query)
        conn.commit()


def fill_tables(cur,conn):
      # Create date_list and genres_list and fill PELICULA table
    genres_list, date_list = extractionTitleBasics(cur,conn)
    # Fill GENERO table
    insertionGenero(cur,conn,genres_list)
    # Fill ANO table
    insertionAno(cur,conn,date_list)
    
    # Create actor_list and fill JUGAR table
    actor_list = extractionTitlePrincipals(cur,conn)
    # Fill ACTOR table
    extractionNameBasics(cur,conn,actor_list)

    # Fill CLASIFICACION table
    extractionTitleRatings(cur,conn)



def main():
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)
    fill_tables(cur,conn)

    conn.close()


if __name__ == "__main__":
    main()