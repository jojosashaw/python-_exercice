import sqlite3 # pour la base de donnée
import sys # pour quitter le programme
import datetime # pour la date et l'heure
import os

conn = sqlite3.connect('premiercourspython2023.db') # créez la base de donnée
cursor = conn.cursor() # créez un curseur pour la base de donnée

cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        titre TEXT,
        notetype TEXT,
        note BLOB,
        date TEXT
    )
    """)
conn.commit()

# refait ce code mais en utilisant les classes et les fonctions

class Blocnote:
    def __init__(self, nom):
        self.nom = nom
        self.notes = []

    def ajouter(self, note):
        self.notes.append(note)
        cursor.execute("""INSERT INTO notes(titre, notetype, note, date) VALUES(?, ?, ?, ?)""", (note.titre, note.notetype, note.note, note.date)) # ajoute la note dans la base de donnée
        conn.commit() # sauvegarde les modifications

    def modifier(self, titre, note):
        cursor.execute("""UPDATE notes SET note = ? WHERE titre = ?""", (note, titre))
        conn.commit() # modifier une note

    def rechercher(self, mot):
        cursor.execute("""SELECT * FROM notes WHERE titre LIKE ? OR note LIKE ?""", ("%"+mot+"%", "%"+mot+"%"))
        notes = cursor.fetchall()
        print("Voici la liste des notes : ")
        print("/-----------------------------------------/")
        for note in notes:
            print(note)
        print("/-----------------------------------------/") # rechercher une note

    def suppimer(self, titre):
        cursor.execute("""DELETE FROM notes WHERE titre = ?""", (titre,))
        conn.commit() # suprimer une note

    def vider_blocnote(self):
        confirmation = input("Êtes-vous sûr de vouloir vider le blocnote ? (O/N) : ")
        if confirmation.lower() == "o":
            cursor.execute("""DELETE FROM notes""")
            conn.commit() # vider le blocnote

    def afficher(self):
        cursor.execute("""SELECT * FROM notes""") # récupère toutes les notes
        notes = cursor.fetchall() # récupère toutes les notes
        print("Voici la liste des notes : ") # affiche un message
        print("/-----------------------------------------/") # affiche un message
        for note in notes: # parcour toutes les notes
            print(note) # affiche les (1par1) note
        print("/-----------------------------------------/") # affiche un message

"""
class note héritage si il y avait un choix restaraint de type de note

class Note:
    def __init__(self, date):
        self.date = date

class NoteTexte(Note):
    def __init__(self, titre, notetexte, date, notetype):
        super().__init__(date)
        self.titre = titre
        self.note = note
        self.notetype = "texte"

class NoteImage(Note):
    def __init__(self, titre, noteimage, date, notetype):
        super().__init__(date)
        self.titre = titre
        self.note = note
        self.notetype = "image"

class NoteVideo(Note):
    def __init__(self, titre, notevideo, date, notetype):
        super().__init__(date)
        self.titre = titre
        self.note = note
        self.notetype = "video"

"""

class Note:
    def __init__(self, titre, notetype, note, date):
        self.titre = titre
        self.notetype = notetype
        self.note = note
        self.date = date
    
    def __str__(self): # convertie la note en string
        return "Titre: %s\nType de note: %s\nNote: %s\nDate: %s" % (self.titre, self.notetype, self.note, self.date) # affiche la note avec le titre, la note et la date de la note une fois convertie en string

blocnoteTest = Blocnote("blocnoteTest")

if __name__ == '__main__':

    while True:

        print("Que voulez-vous faire ?")
        print("1. Ajouter une note")
        print("2. Afficher les notes")
        print("3. modifier une note")
        print("4. Rechercher une note")
        print("5. Supprimer une note")
        print("6. Vider le blocnote")
        print("7. Quitter")
        choix = input("Votre choix : ")

        match choix:

            case "1":
                os.system("cls")
                titre = input("Titre de la note : ")
                type_de_note = input("Type de note : ")
                note = input("Note : ")
                date = datetime.datetime.now()
                note = Note(titre, type_de_note, note, date)
                blocnoteTest.ajouter(note)

                """
                affichage si jamais il y avait un choix restreint de type de note

                case "1":
                    os.system("cls")
                    print("quel type de note voulez-vous ajouter ?")
                    print("1. Note texte")
                    print("2. Note image")
                    print("3. Note vidéo")

                    match input("Votre choix : "):
                        case "1":
                            os.system("cls")
                            titre = input("Titre de la note : ")
                            note = input("Note : ")
                            date = datetime.datetime.now()
                            note = NoteTexte(titre, notetext, date)
                            blocnoteTest.ajouter(note)
                        case "2":
                            os.system("cls")
                            titre = input("Titre de la note : ")
                            image = input("Votre image : ")
                            date = datetime.datetime.now()
                            note = NoteImage(titre, noteimage, date)
                            blocnoteTest.ajouter(note)  

                        case "3":
                            os.system("cls")
                            titre = input("Titre de la note : ")
                            video = input("Votre vidéo : ")
                            date = datetime.datetime.now()
                            note = NoteVideo(titre, notevideo, date)
                            blocnoteTest.ajouter(note)
                
                """
    
            case "2":
                os.system("cls")
                blocnoteTest.afficher()

            case "3":
                os.system("cls")
                titre = input("Titre de la note à modifier : ")
                os.system("cls")
                blocnoteTest.rechercher(titre)
                note = input("Modification de la note : ")
                blocnoteTest.modifier(titre, note)
    
            case "4":
                os.system("cls")
                mot = input("Mot à rechercher : ")
                blocnoteTest.rechercher(mot)
    
            case "5":
                os.system("cls")
                title = input("Titre de la note à supprimer : ")
                blocnoteTest.suppimer(title)
    
            case "6":
                os.system("cls")
                blocnoteTest.vider_blocnote()
    
            case "7":
                os.system("cls")
                sys.exit()
    
