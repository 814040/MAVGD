# Create the tables

create_pelicula = ("""
CREATE TABLE pelicula
(	idTitulo SERIAL PRIMARY KEY,
	idAno FLOAT NOT NULL,
	idGenero FLOAT	NOT NULL,
	duracion CHAR,
	titulo CHAR);
""")

create_actor = ("""
	CREATE TABLE actor
(	idActor	BIGINT,
	nombreActor	CHAR,
	apellido CHAR);
""")

create_genero = ("""
CREATE TABLE genero
(	idGenero FLOAT,
	Genero CHAR NOT NULL);
""")

create_ano = ("""
CREATE TABLE ano
(
	idAno INT,
	Ano	FLOAT NOT NULL,
	fechaEstreno DATE NOT NULL);
""")

create_empresa = ("""
CREATE TABLE empresa
(
	idEmpresa INT,
	nombreEmpresa CHAR NOT NULL,
	paisEmpresa CHAR);
""")

create_jugar = ("""
CREATE TABLE jugar
(
	idJugar	BIGINT,
	idTitulo FLOAT,
	idActor	FLOAT
);
""")

create_clasificacion = ("""
CREATE TABLE clasificacion
(
	idTitulo INT,
	valuacionMedia FLOAT, 
	nombreVoto INT
);
""")

create_all_tables=[create_pelicula, create_clasificacion, create_jugar, create_empresa, create_ano, create_genero, create_actor]

# Drop all the tables from db

actor_table_drop = "DROP TABLE IF EXISTS actor;"
genero_table_drop = "DROP TABLE IF EXISTS genero;"
ano_table_drop = "DROP TABLE IF EXISTS ano;"
empresa_table_drop = "DROP TABLE IF EXISTS empresa;"
pelicula_table_drop = "DROP TABLE IF EXISTS pelicula;"
jugar_table_drop = "DROP TABLE IF EXISTS jugar;"
clasificacion_table_drop = "DROP TABLE IF EXISTS clasificacion;"

drop_all_tables = [pelicula_table_drop, jugar_table_drop, clasificacion_table_drop, actor_table_drop, genero_table_drop, ano_table_drop, empresa_table_drop]

# Insert queries to db 

peliculaInsert = ("""INSERT INTO pelicula ( idTitulo, idAno, idGenero, duracion, titulo) Values ( {}, {}, {}, {}, {})""")

actorInsert = ("""INSERT INTO actor (idActor, nombreActor, apellido) Values ({}, {}, {})""")

generoInsert = ("""INSERT INTO genero (idGenero, genero) Values ({}, {})""")

anoInsert = ("""INSERT INTO ano (idAno, ano, fechaEstreno) Values ({}, {}, {})""")

empresaInsert = ("""INSERT INTO empresa (idEmpresa, nombreEmpresa, paisEmpresa) Values ({},{},{})""")

jugarInsert = ("""INSERT INTO jugar (idJugar, idTitulo, idActor) Values ({},{},{})""")

clasificacionInsert = ("""INSERT INTO espectador (idTitulo, valuacionMedia, nombreVoto) Values ({},{},{})""")