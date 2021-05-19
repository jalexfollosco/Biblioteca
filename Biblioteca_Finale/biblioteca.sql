
/* Creazione della tabella libro*/
create table libro(
	isbn int(13) primary key,
	titolo varchar(255) not null,
	lingua varchar(255) not null,
	editore varchar(255),
	anno int(4),
	copie int(2) not null
);

/* Creazione della tabella categoria*/
create table categoria(
	id int(5) primary key,
	nome varchar(255) not null unique
);

/* Creazione della tabella bridge_categoria*/
create table bridge_categoria(
	isbn_libro int (13) not null references libro(isbn),
	id_categoria int(5) not null references categoria(id)
);

/* Creazione della tabella autore*/
create table autore(
	id int(5) primary key,
	nome varchar(255) not null,
	cognome varchar(255) not null,
	data_nascita date,
	luogo_nascita varchar(255),
	note varchar(255),
	unique(nome, cognome, data_nascita, luogo_nascita)
);

/* Creazione della tabella bridge_autore*/
create table bridge_autore(
	isbn_libro int (13) not null references libro(isbn),
	id_autore int(5) not null references autore(id)
);

/* Creazione della tabella utente*/
create table utente(
	id_tessera int(5) primary key,
	data_registrazione date not null,
	nome varchar(255) not null,
	cognome varchar(255) not null,
	telefono char(10) not null unique,
	indirizzo varchar(255),
	email varchar(255) 
);

/* Creazione della tabella prestito*/
create table prestito(
	isbn_libro int(13) not null references libro(isbn),
	tessera_id int(5) not null references utente(id_tessera),
	data_prestito date not null,
	data_restituzione date
);