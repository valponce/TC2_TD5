from tkinter import *
from random import randint
from formes import*
from tkinter import colorchooser
import sqlite3

# Création d'une base de données stockant le pseudo des joueurs ainsi que le nombre de parties gagnée et perdue
class BaseDonnees():
    def __init__(self,typ,fichier):        
        self.__con = typ.connect(fichier)
        self.cur = self.__con.cursor()
        
        #Création des différentes colonnes du tableau si elles n'existent pas déjà
        res=self.cur.execute("SELECT name FROM sqlite_master WHERE name='scores'")
        if res.fetchone() is None:
              self.cur.execute("CREATE TABLE scores(pseudo TEXT, echecs INTEGER, victoires INTEGER)")
    
    # ajout du pseudo d'un nouveau joueur dans le tableau scores
    def ajout_joueur(self,pseudo):
        res=self.cur.execute("SELECT pseudo FROM scores WHERE pseudo=:nom",{"nom":pseudo})
        if res.fetchone() is None:
            self.cur.execute("""INSERT INTO scores VALUES (:pseudo,0,0)""",{"pseudo":pseudo})
            self.__con.commit()

    #augmente d'un le nombre de victoires dans le tableau scores du joueur dont le nom est passé en argument
    def set_victoire(self,nom):
        self.cur.execute("UPDATE scores SET victoires=victoires+1 WHERE pseudo=:nom",{"nom":nom})
        self.__con.commit()
    
    #augmente d'un le nombre d'échecs dans le tableau scores du joueur dont le nom est passé en argument
    def set_echec(self,nom):       
        self.cur.execute("UPDATE scores SET echecs=echecs+1 WHERE pseudo=:nom",{"nom":nom})
        self.__con.commit()
    
    # Renvoie le nombre d'échecs et de victoires d'un joueur
    def score(self,nom):
        res=self.cur.execute("SELECT echecs,victoires FROM scores WHERE pseudo=:nom",{"nom":nom})
        return(res.fetchone())
    
class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur,background="white")
        
        # Liste des formes composant le pendu: Base, Poteau, Traverse, Corde,Tete, Tronc,Bras gauche et droit, Jambes gauche et droite
        self.formes=[Rectangle(self, 50,  270, 200,  26, "dark blue"),Rectangle(self, 87,   83,  26, 200, "dark blue")
                ,Rectangle(self, 87,   70, 150,  26, "dark blue"),Rectangle(self, 183,  67,  10,  40, "dark blue")
                ,Ellipse(self, 187, 123,  15,  15, "black"),Rectangle(self, 185.5, 133, 5,  60, "black")
                ,Rectangle(self, 145, 150,  40, 5, "black"),Rectangle(self, 188, 150,  40,  5, "black")
                ,Rectangle(self, 181, 187,  5,  50, "black"),Rectangle(self, 191, 187,  5,  50, "black")]
    
    def setCouleurEchafaudage(self):
       couleur=colorchooser.askcolor()[1]
       for i in range(4):
           self.formes[i].set_couleur(couleur)
    
    def setCouleurPendu(self):
       couleur=colorchooser.askcolor()[1]
       for i in range(4,10):
           self.formes[i].set_couleur(couleur)
   
class MonBoutonLettre(Button):
    def __init__(self,parent,i,fenetre):
        # Enregistre la lettre
        lettre=chr(ord('A')+i)
        self.__lettre=lettre
        
        #initialisation de la classe parente
        Button.__init__(self,parent,text=lettre,width=6)
        
        # Enregistre la fenêtre parentale
        self.__fen=fenetre
        
        #Bouton initialement désactivé et associé à la fonction cliquer
        self.config(bg='white',state='disabled',command=self.cliquer)
    
    def cliquer(self):
        # Désactive la touche
        self.config(state='disabled')
        # Fait appel à la methode de la fenêtre principale en passant la lettre
        self.__fen.traitement(self.__lettre)

class FenIntro(Tk):
    #Fenêtre d'introduction du jeu ou le joueur choisit un pseudo
    def __init__(self):
        
        # Initialise la fenêtre
        Tk.__init__(self)
        
        self.__Frame1=Frame(self,bg='light grey')
        self.__Frame1.pack()
        self.__base=BaseDonnees(sqlite3,"Joueurs")
        self.__pseudo=None
        
        label=Label(self.__Frame1,text="Entrez votre pseudo:",bg='light grey')
        label.pack(side=TOP,pady=10)
        
        self.__entry=Entry(self.__Frame1)
        self.__entry.pack(side=TOP,padx=20,pady=6)

        BouttonValider=Button(self.__Frame1, text='Valider',bg="white")
        BouttonValider.pack(side=TOP,pady=10)
        
        self.__BoutonClassement=Button(self.__Frame1,text='Classement',bg="white")
        self.__BoutonClassement.pack(side=BOTTOM,pady=10)
        
        self.__BoutonClassement.config(command=self.afficher_classement)
        BouttonValider.config(command=self.lancement_jeu)
    
    def afficher_classement(self):
        self.__BoutonClassement.destroy() #Disparition du bouton classement une fois pressé
        
        #Tri du tableau score par nombre devictoires décroissant puis d'échecs croissant
        res=self.__base.cur.execute("SELECT * FROM scores ORDER BY victoires DESC, echecs ASC")
        resultat=res.fetchall()
        
        # Affichage du score des 3 meilleurs joueurs
        for i in range(3):
            label=Label(self.__Frame1,text=f"({i+1}). {resultat[i][0]}, Echecs:{resultat[i][1]}, Victoires:{resultat[i][2]}",bg='light grey')
            label.pack(side=TOP,pady=10)
        
    def lancement_jeu(self):
        #Récupéraion du pseudo entré par le joueur
        self.__pseudo=self.__entry.get()    
        
        #Disparition/Suppression de la fenêtre d'introduction
        self.destroy()
        
        #Ajout du nouveau joueur à la base de donnée
        self.__base.ajout_joueur(self.__pseudo)
        
        #Lancement de la fenêtre de jeu
        fen= FenPrincipale(self.__base,self.__pseudo)
        fen.mainloop()
        
class FenPrincipale(Tk):
    #fenêtre principale
    def __init__(self,base,joueur):
        Tk.__init__(self)

        # paramètres de la fenêtre
        self.title('Jeu du pendu') # le titre de la fenêtre
        self.configure(bg="light blue") # impose la couleur du fond
        self.__boutons=[]
        
        #Création de la liste des mots du fichier
        self.__listeMots=None 
        self.chargeMots()
        
        self.__mot_affiche=None
        self.__mot=""
        
        #Liste des lettres trouvées
        self.__trouve=[]
        
        #Liste des lettres essayées par le joueur
        self.__essais=[]
        
        #Nombre de fausses lettres proposées
        self.__nb_manques=0
        
        #Pseudo du joueur actuellement entrain de jouer
        self.__pseudo=joueur
        
        #Base de données contenant les scores des joueurs
        self.__base_donnees=base
        
        #Création barre outils
        self.__barreOutils= Frame(self,bg="light blue")
        self.__barreOutils.pack(side=TOP, padx=30,pady=10)
        
        boutonNouvellePartie=Button(self.__barreOutils, text='Nouvelle partie',bg="white")
        boutonNouvellePartie.pack(side=LEFT, padx=10, pady=5)
        
        boutonUndo = Button(self.__barreOutils, text='Undo',bg="white")
        boutonUndo.pack(side=LEFT, padx=15, pady=5)
        
        
        boutonCouleur = Menubutton(self.__barreOutils, text='Couleur',bg="white")
        boutonCouleur.pack(side=LEFT, padx=15, pady=5)
        
        #Création de la zone de dessin 
        self.canvas=ZoneAffichage(self, 300,300)
        self.canvas.pack(side=TOP, padx=30, pady=5)
        
        #Menu déroulant du Bouton Couleur
        menuCouleur = Menu(boutonCouleur)
        menuCouleur.add_command(label = "Couleur de l'échafaudage", command = self.canvas.setCouleurEchafaudage)
        menuCouleur.add_command(label = 'Couleur du pendu', command = self.canvas.setCouleurPendu)
        menuCouleur.add_command(label = "Couleur du background", command = self.setCouleurBg)
        
        #Le Menu apparait lorsque le bouton Couleur est pressé
        boutonCouleur.config(menu=menuCouleur)
      
        
        boutonQuitter = Button(self.__barreOutils, text='Quitter',bg="white")
        boutonQuitter.pack(side=LEFT, padx=15, pady=5)
        
       
        
        #Création du clavier
        clavier= Frame(self,bg="ivory")
        clavier.pack(side=BOTTOM,padx=30,pady=15)
        
        #Création des 26 boutons lettres, objets de la classe MonBoutonLettre
        for i in range(26):
           Lettre=MonBoutonLettre(clavier,i,self)
           
           #Stocke l'ensemble des boutons
           self.__boutons.append(Lettre)
           
           #Disposition des lettres sur le clavier
           if i<7:
               Lettre.grid(row=1, column=i,padx=5, pady=5)
           elif 7<=i<14:
               Lettre.grid(row=2, column=i-7,padx=5, pady=5)
           elif 14<= i <21:
               Lettre.grid(row=3, column=i-14,padx=5, pady=5)
           else:
               Lettre.grid(row=4, column=i-20,padx=5, pady=5)
        
        #Emplacement du mot
        self.__Mot=Label(self,text="Mot:")
        self.__Mot.pack(side=BOTTOM,padx=30,pady=10)
        
        #COnfiguration de l'action des boutons
        boutonQuitter.config(command=self.destroy)
        boutonNouvellePartie.config(command=self.nouvelle_partie)
        boutonUndo.config(command=self.retour_en_arriere)

    #Change la couleur de l'arrière plan 
    def setCouleurBg(self):
        couleur=couleur=colorchooser.askcolor()[1] #demande une couleur à l'utilisateur
        self.configure(bg=couleur)
        self.__barreOutils.config(bg=couleur)
        
    def retour_en_arriere(self):
        if self.__essais: #Vérification qu'il existe une action à annuler, pas début de la partie
            lettre,valeur=self.__essais.pop() #valeur: False si la lettre n'appartient pas au mot sinon True
            self.__boutons[ord(lettre)-65].config(state='normal')
            if not(valeur): # si la lettre n'appartient pas au mot
                #une erreur annulée/en moins
                self.__nb_manques-=1
                
                #supprime la dernière forme du pendu tracée
                self.canvas.formes[self.__nb_manques].set_state('hidden')
            
            else: #si la lettre appartient au mot
            
                #On cherche les différents emplacement de la lettre et on la remplace par * dans le mot à afficher
                for i in range(len(self.__trouve)):
                    if lettre==self.__trouve[i]:
                        self.__trouve[i]="*"
                separateur=""
                texte="Mot :"+str(separateur.join(self.__trouve))
                self.__Mot.config(text=texte) 
           
            
           
    def traitement(self,lettre):
        """ valeur indique si la lettre appartient(True) ou non(False) au mot """
        valeur=False 
        for i in range(len(self.__mot)):
            if self.__mot[i]==lettre: # si on trouve la lettre dans le mot
                self.__trouve[i]=lettre
                valeur=True 
        #Affichage des lettres trouvées au bonne endroit dans le mot
        separateur=""
        texte="Mot :"+str(separateur.join(self.__trouve))
        self.__Mot.config(text=texte) 
        
        if not(valeur): # si la lettre n'est pas dans le mot
            #Dessin de la prochaine forme du pendu
            self.canvas.formes[self.__nb_manques].set_state('normal')
            
            #Ajout d'un coup manqué
            self.__nb_manques+=1
        
        #Enregistrement de la tentative et si elle est bonne ou pas(valeur)
        self.__essais.append((lettre,valeur))
        
        #Vérification si la partie est finie ou non
        self.fin_partie(texte)



    def fin_partie(self,texte):
        if texte[5:]==self.__mot: # si toutes les lettres sont trouvées
            
            #Désactivation du clavier
            for b in self.__boutons:
                b.config(state="disabled")
                
            #Ajoute une victoire au score du joueur
            self.__base_donnees.set_victoire(self.__pseudo)
            
            #Affichage de fin de jeu lors d'une victoire
            e,v=self.__base_donnees.score(self.__pseudo)
            self.__Mot.config(text=f"Vous avez gagné. Le mot était:{self.__mot}. Echecs: {e} Victoires:{v}")
            
        if self.__nb_manques==10: #si le joueur perd = il s'est trompé 10 fois
            
            #Désactiation du clavier
            for b in self.__boutons:
                b.config(state="disabled")
                
            #Ajoute un échec au score du joueur
            self.__base_donnees.set_echec(self.__pseudo)
            
            #Affichage de fin de jeu lorsqu'on perd
            e,v=self.__base_donnees.score(self.__pseudo)
            self.__Mot.config(text=f"PERDU. Echecs: {e} Victoires:{v}")
        
        #empêche le joueur de revenir en arrière quand la partie est finie
        self.__essais=[] 
       
        
    #Charge les mots à faire deviner de la liste fournie
    def chargeMots(self):
        f = open('mots.txt', 'r')
        s=f.read()
        self.__mots = s.split('\n')
        f.close()



    def nouvelle_partie(self):
        #Réinitialise le nombre de coup manqué
        self.__nb_manques=0
        #Et l'historique des lettres essayées
        self.__essais=[]
        
        #Efface le dessin du pendu
        for f in self.canvas.formes:
            f.set_state('hidden')
        
        #Tire un nouveau mot
        self.nouveau_mot()
        
        #Activation du clavier
        for b in self.__boutons:
            b.config(state="normal")
        
        
    # Tirage au hasard d'un nouveau mot à deviner
    def nouveau_mot(self):
        self.__mot=self.__mots[randint(0,len(self.__mots)-1)]#on tire un eniter au hasard entre 0 et la longueur de la liste mot 
        #Aucune lettre trouvée
        self.__trouve=["*" for i in range (len(self.__mot))]
        self.__Mot.config(text="Mot :"+"*"*len(self.__mot))
            
if __name__ == "__main__":
    intro=FenIntro()
    intro.mainloop()
    
