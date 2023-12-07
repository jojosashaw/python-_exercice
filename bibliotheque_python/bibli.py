import sqlite3
import os

'''
Au début j'avais essayé de mettre plussieurs exemplaire d'un même livre mais je n'ai pas réussi
Voici le code que j'avais fait pour cela:
dans la classe livre j'avais rajouté un attribut nb_exemplaires et nb_exemplaires_disponibles, une liste d'emprunteurs et une liste de date d'emprunt et de retour
ces trois dernier champs étais remplis au moment d'emprunter un livre en utilisant unne fonction emprunt_retour de Livre qui mettait a jour la liste d'emprunteurs et la liste de date d'emprunt et de retour
au moment de l'emprunt ou du retour je vérifiais que le nombre d'exemplaires disponibles était supérieur à 0
et je mettais a jour le nombre d'exemplaires disponibles
'''

'''
je voulais aussi ajouter pour chaque utilisateur une liste des livres qu'il a emprunté
mais j'ai eu un problem de type ducoup jai une autre solution masi je n'ai pas le temps de la faire : 
rajouter un champs liste_emprunt TEXT et l'implémenter sous la forme : titre_livre + ', ' quand je l'ajoute
comme ca quand je le suprime je suprime la fomre titre_livre + ', ' 
et je peux faire une fonction qui affiche la liste des livres emprunté
'''

'''
Pour l'héritage je pensais faire plussieurs genre de livre : jeunesse, ado, adulte.
on aurait choisi le genre du livre au moment de l'ajout et on aurait pu faire une fonction qui affiche les livres d'un genre donné
j'aurais utilisé factory pour créer les livres de chaque genre 
exemple non représentatif :
class LivreFactory:
    def creer_livre(self, type_livre, titre, auteur):
        if type_livre == "Fiction":
            return LivreFiction(titre, auteur)
        elif type_livre == "NonFiction":
            return LivreNonFiction(titre, auteur)
        else:
            raise ValueError("Type de livre non pris en charge")
'''

# création de la base de données bibliotheque

def creation_base():
    if not os.path.exists('bibliotheque.db'):
        conn = sqlite3.connect('bibliotheque.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS livres
                    (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    titre TEXT NOT NULL,
                    auteur TEXT NOT NULL,
                    annee INTEGER NOT NULL,
                    editeur TEXT NOT NULL,
                    categorie TEXT NOT NULL,
                    disponible TINYINT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS utilisateurs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    adresse TEXT NOT NULL,
                    telephone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    date_inscription TEXT NOT NULL)''')
        conn.commit()
        conn.close()


class Livre:
    def __init__(self, titre, auteur, annee, editeur, categorie, disponible):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.editeur = editeur
        self.categorie = categorie
        self.disponible = disponible

    def ajouter_livre(self):
        conn = sqlite3.connect('bibliotheque.db')
        c = conn.cursor()
        c.execute('''INSERT INTO livres(titre, auteur, annee, editeur, categorie, disponible) VALUES (?, ?, ?, ?, ?, ?)''', (self.titre, self.auteur, self.annee, self.editeur, self.categorie, self.disponible))
        conn.commit()
        conn.close()

    def creer_livre(titre, auteur, annee, editeur, categorie, disponible = 1):
        livre = Livre(titre, auteur, annee, editeur, categorie, disponible)
        livre.ajouter_livre()

    def afficher_livres():
        conn = sqlite3.connect('bibliotheque.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM livres''')
        print(c.fetchall())
        conn.close()

    def rechercher_livre(search_type, search_value):
        conn = sqlite3.connect('bibliotheque.db')
        c = conn.cursor()

        if search_type == 'titre':
            c.execute('''SELECT * FROM livres WHERE titre=?''', (search_value,))
        elif search_type == 'auteur':
            c.execute('''SELECT * FROM livres WHERE auteur=?''', (search_value,))
        elif search_type == 'categorie':
            c.execute('''SELECT * FROM livres WHERE categorie=?''', (search_value,))
        
        resultat = c.fetchall()
        conn.close()
        return resultat



class Utilisateur:
    def __init__(self, nom, prenom, age, adresse, telephone, email, date_inscription):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.adresse = adresse
        self.telephone = telephone
        self.email = email
        self.date_inscription = date_inscription

    def ajouter_utilisateur(self):
        conn = sqlite3.connect('bibliotheque.db')
        c = conn.cursor()
        c.execute('''INSERT INTO utilisateurs(nom, prenom, age, adresse, telephone, email, date_inscription) VALUES (?, ?, ?, ?, ?, ?, ?)''', (self.nom, self.prenom, self.age, self.adresse, self.telephone, self.email, self.date_inscription))
        conn.commit()
        conn.close()

    def creer_utilisateur(nom, prenom, age, adresse, telephone, email, date_inscription):
        utilisateur = Utilisateur(nom, prenom, age, adresse, telephone, email, date_inscription)
        utilisateur.ajouter_utilisateur()

    def afficher_utilisateurs():
        conn = sqlite3.connect('bibliotheque.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM utilisateurs''')
        print(c.fetchall())
        conn.close()

    def rechercher_utilisateur(search_type, search_value):
        conn = sqlite3.connect('bibliotheque.db')
        c = conn.cursor()

        if search_type == 'nom':
            c.execute('''SELECT * FROM utilisateurs WHERE nom=?''', (search_value,))
        elif search_type == 'prenom':
            c.execute('''SELECT * FROM utilisateurs WHERE prenom=?''', (search_value,))
        elif search_type == 'email':
            c.execute('''SELECT * FROM utilisateurs WHERE email=?''', (search_value,))
        
        resultat = c.fetchall()
        conn.close()
        return resultat

    def emprunter(self, titre_livre):
        conn = sqlite3.connect('bibliotheque.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM livres WHERE titre=? AND disponible=1''', (titre_livre,))
        livre = c.fetchone()
        if livre: 
            c.execute('''UPDATE livres SET disponible=0 WHERE titre=?''', (titre_livre,))
            conn.commit()
            conn.close()
            print("Vous avez emprunté le livre: " + titre_livre)
        else:
            print("Ce livre n'est pas disponible")
        

    def retourner(self, titre_livre):
        conn = sqlite3.connect('bibliotheque.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM livres WHERE titre=? AND disponible=0''', (titre_livre,))
        livre = c.fetchone()
        if livre:
            c.execute('''UPDATE livres SET disponible=1 WHERE titre=?''', (titre_livre,))
            conn.commit()
            conn.close()
            print("Vous avez rendu le livre: " + titre_livre)
        else:
            print("Ce livre n'est pas emprunté par vous")

if __name__ == '__main__':
    creation_base()

    # creation de linterface utilisateur
    def interface_bibliotheque():
        print("Bienvenue dans la bibliothèque")
        print("Que voulez vous faire ?")
        print("1. Gestion des livres")
        print("2. Gestion des utilisateurs")
        print("3. Quitter")
        choix = input("Votre choix: ")
        if choix == '1':
            interface_livres()
        elif choix == '2':
            interface_utilisateurs()
        elif choix == '3':
            print("Au revoir")
            exit()
        else:
            print("Veuillez choisir une option valide")
            interface_bibliotheque()

    def interface_livres():
        print("1. Ajouter un livre")
        print("2. Rechercher un livre")
        print("3. Afficher tous les livres")
        print("4. Retour")
        choix = input("Votre choix: ")
        if choix == '1':
            titre = input("Titre: ")
            auteur = input("Auteur: ")
            annee = input("Année: ")
            editeur = input("Editeur: ")
            categorie = input("Catégorie: ")
            disponible = 1
            Livre.creer_livre(titre, auteur, annee, editeur, categorie, disponible)
            interface_livres()
        elif choix == '2':
            print("1. Par titre")
            print("2. Par auteur")
            print("3. Par catégorie")
            choix = input("Votre choix: ")
            if choix == '1':
                search_type = 'titre'
                search_value = input("Titre: ")
            elif choix == '2':
                search_type = 'auteur'
                search_value = input("Auteur: ")
            elif choix == '3':
                search_type = 'categorie'
                search_value = input("Catégorie: ")
            else:
                print("Veuillez choisir une option valide")
                interface_livres()    
            print(Livre.rechercher_livre(search_type, search_value))
            interface_livres()
        elif choix == '3':
            Livre.afficher_livres()
            interface_livres()
        elif choix == '4':
            interface_bibliotheque()
        else:
            print("Veuillez choisir une option valide")
            interface_livres()

    def interface_utilisateurs():
        print("1. Ajouter un utilisateur")
        print("2. Rechercher un utilisateur")
        print("3. Afficher tous les utilisateurs")
        print("4. Emprunter un livre")
        print("5. Retourner un livre")
        print("6. Retour")
        choix = input("Votre choix: ")
        if choix == '1':
            nom = input("Nom: ")
            prenom = input("Prénom: ")
            age = input("Age: ")
            adresse = input("Adresse: ")
            telephone = input("Téléphone: ")
            email = input("Email: ")
            date_inscription = input("Date d'inscription: ")
            Utilisateur.creer_utilisateur(nom, prenom, age, adresse, telephone, email, date_inscription)
        elif choix == '2':
            print("1. Par nom")
            print("2. Par prénom")
            print("3. Par email")
            choix = input("Votre choix: ")
            if choix == '1':
                search_type = 'nom'
                search_value = input("Nom: ")
            elif choix == '2':
                search_type = 'prenom'
                search_value = input("Prénom: ")
            elif choix == '3':
                search_type = 'email'
                search_value = input("Email: ")
            else:
                print("Veuillez choisir une option valide")
                interface_utilisateurs()
            print(Utilisateur.rechercher_utilisateur(search_type, search_value))
            interface_utilisateurs()
        elif choix == '3':
            Utilisateur.afficher_utilisateurs()
            interface_utilisateurs()
        elif choix == '4':
            email = input("Email de l'emprunteur: ")
            titre_livre = input("Titre du livre: ")
            Utilisateur.emprunter(Utilisateur.rechercher_utilisateur('email', email), titre_livre)
            interface_utilisateurs()
        elif choix == '5':
            email = input("Email de l'emprunteur: ")
            titre_livre = input("Titre du livre: ")
            Utilisateur.retourner(Utilisateur.rechercher_utilisateur('email', email), titre_livre)
            interface_utilisateurs()
        elif choix == '6':
            interface_bibliotheque()
        else:
            print("Veuillez choisir une option valide")
            interface_utilisateurs()

    interface_bibliotheque()  


