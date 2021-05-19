# Definizione delle varie classi 

'''
In questo script definiamo le classi che andiamo a richiamare
poi negli alti script. 
Abbiamo la classe Persona che è la classe padre di classe Utente 
e di classe Autore che sono le figlie.
Come ultima classe definita c'è la classe Libro.
'''
# Classe persona che è la classe padre
class persona: 
    
  def __init__(self, nome = "", cognome = "", eta =""):
        self.nome = nome
        self.cognome = cognome
        
          
            
# Le classi utente e autore che sono le classi figlie della classe padre
# Definizione della classe utente 
class utente(persona): 
    profilo = "utente"

    def __init__(self, nome, cognome, registrazione, telefono, email, indirizzo, numero_tessera = ''):
        super().__init__(nome, cognome)
        self.numero_tessera = numero_tessera
        self.registrazione = registrazione
        self.telefono = telefono
        self.email = email
        self.indirizzo = indirizzo

# Definizioe della classe autore        
class autore(persona):
    profilo = "autore"     

    def __init__(self, nome, cognome, data_nascita, luogo_nascita, note= ''): 
        super().__init__(nome, cognome)
        self.data_nascita = data_nascita 
        self.luogo_nascita = luogo_nascita 
        self.note = note
        
# Classe Libro
class Libro:
    
    def __init__ (self,ISBN = "", titolo = "", lingua = "", autore = "", editore = "", anno = "",  copie = "", categoria = ""):
        
        self.ISBN = ISBN
        self.titolo = titolo
        self.lingua = lingua
        self.editore = editore
        self.anno = anno
        self.categoria = categoria
        self.copie = copie
        self.autore = autore

# Funzione che mi permette di visualizzare i dati del Libro.
#  Quali: ISBN, titolo, lingua, editore, anno, categoria,
# copie disponibili, autore.        
    def view(self):
        print('\n\nISBN: ', self.ISBN)
        print('Titolo: ', self.titolo)
        print('Lingua: ', self.lingua)
        print('Editore: ', self.editore)
        print('Anno: ', self.anno)
        print('Categoria: ', self.categoria)
        print('Copie: ', self.copie)
        print('Autore: ',self.autore)
        
     
