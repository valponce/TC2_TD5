from tkinter import *
from random import randint
from formes import*
from tkinter import colorchooser

class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur,background="white")
        self.__couleur=["black","black"]
        self.formes=[Rectangle(self, 50,  270, 200,  26, "dark blue"),Rectangle(self, 87,   83,  26, 200, "dark blue")
                ,Rectangle(self, 87,   70, 150,  26, "dark blue"),Rectangle(self, 183,  67,  10,  40, "dark blue")
                ,Ellipse(self, 187, 123,  15,  15, self.__couleur[0]),Rectangle(self, 185.5, 133, 5,  60, self.__couleur[0])
                ,Rectangle(self, 145, 150,  40, 5, self.__couleur[1]),Rectangle(self, 188, 150,  40,  5, self.__couleur[1])
                ,Rectangle(self, 181, 187,  5,  50, self.__couleur[1]),Rectangle(self, 191, 187,  5,  50, self.__couleur[1])]
        # Base, Poteau, Traverse, Corde,Tete, Tronc,Bras gauche et droit, Jambes gauche et droite
        
    #def changer_couleur
    
    def selection_couleur(self):
        self.__couleur=[colorchooser.askcolor()[1],colorchooser.askcolor()[2]]

class MonBoutonLettre(Button):
    def __init__(self,parent,i):
        lettre=chr(ord('A')+i)
        Button.__init__(self,parent,text=lettre,width=6)
        self.__lettre=lettre
        self.config(bg='white',state='disabled',command=self.cliquer)
    def cliquer(self):
        self.config(state='disabled')
        fen.traitement(self.__lettre)
        
class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)

        # paramètres de la fenêtre
        self.title('Jeu du pendu')
        self.configure(bg="light blue")
        #self.__lettres=[chr(ord('A')+i) for i in range(26)]
        self.__boutons=[]
        self.__listeMots=None
        self.__mot_affiche=None
        self.__mot=""
        self.__trouve=[]
        self.__essais=[]
        self.__nb_manques=0
        self.chargeMots()
        
        
        #Création barre outils
        barreOutils= Frame(self,bg="light blue")
        barreOutils.pack(side=TOP, padx=30,pady=10)
        
        boutonNouvellePartie=Button(barreOutils, text='Nouvelle partie',bg="white")
        boutonNouvellePartie.pack(side=LEFT, padx=10, pady=5)
        
        boutonUndo = Button(barreOutils, text='Undo',bg="white")
        boutonUndo.pack(side=LEFT, padx=15, pady=5)
        
        boutonCouleur = Button(barreOutils, text='Couleur',bg="white")
        boutonCouleur.pack(side=LEFT, padx=15, pady=5)
        
        boutonQuitter = Button(barreOutils, text='Quitter',bg="white")
        boutonQuitter.pack(side=LEFT, padx=15, pady=5)
        
       
        
        #Création du clavier
        clavier= Frame(self,bg="ivory")
        clavier.pack(side=BOTTOM,padx=30,pady=15)
        for i in range(26):
           Lettre=MonBoutonLettre(clavier,i)
           self.__boutons.append(Lettre)
           if i<7:
               Lettre.grid(row=1, column=i,padx=5, pady=5)
           elif 7<=i<14:
               Lettre.grid(row=2, column=i-7,padx=5, pady=5)
           elif 14<= i <21:
               Lettre.grid(row=3, column=i-14,padx=5, pady=5)
           else:
               Lettre.grid(row=4, column=i-20,padx=5, pady=5)
        
        #Emplacement du mot
        Mot=Label(self,text="Mot:")
        self.__mot_afficher=Mot
        Mot.pack(side=BOTTOM,padx=30,pady=10)
        
        #Création de la zone de dessin 
        self.canvas=ZoneAffichage(self, 300,300)
        self.canvas.pack(side=TOP, padx=30, pady=5)
        
        
        
        boutonQuitter.config(command=self.destroy)
        boutonNouvellePartie.config(command=self.nouvelle_partie)
        boutonCouleur.config(command=self.canvas.selection_couleur)
        boutonUndo.config(command=self.retour_en_arriere)
    
    def retour_en_arriere(self):
        if self.__essais:
            lettre,valeur=self.__essais.pop()
            self.__boutons[ord(lettre)-65].config(state='normal')
            if not(valeur):
                self.__nb_manques-=1
                self.canvas.formes[self.__nb_manques].set_state('hidden')
            else:
                for i in range(len(self.__trouve)):
                    if lettre==self.__trouve[i]:
                        self.__trouve[i]="*"
                separateur=""
                texte="Mot :"+str(separateur.join(self.__trouve))
                self.__mot_afficher.config(text=texte) 
            
    def traitement(self,lettre):
        valeur=False
        for i in range(len(self.__mot)):
            if self.__mot[i]==lettre:
                self.__trouve[i]=lettre
                valeur=True
        separateur=""
        texte="Mot :"+str(separateur.join(self.__trouve))
        self.__mot_afficher.config(text=texte) 
        if not(valeur):
            self.canvas.formes[self.__nb_manques].set_state('normal')
            self.__nb_manques+=1
        self.__essais.append((lettre,valeur))
        self.fin_partie(texte)


    def fin_partie(self,texte):
        self.__essais=[]
        if texte[5:]==self.__mot:
            for b in self.__boutons:
                b.config(state="disabled")
            self.__mot_afficher.config(text="Vous avez gagné. Le mot était:"+self.__mot)
        if self.__nb_manques==10:
            for b in self.__boutons:
                b.config(state="disabled")
            self.__mot_afficher.config(text="PERDU")
        
    def chargeMots(self):
        f = open('mots.txt', 'r')
        s=f.read()
        self.__mots = s.split('\n')
        f.close()

    def nouvelle_partie(self):
        self.__nb_manques=0
        self.__essais=[]
        self.nouveau_mot()
        for b in self.__boutons:
            b.config(state="normal")
        
            
    def nouveau_mot(self):
        for f in self.canvas.formes:
            f.set_state('hidden')
        self.__mot=self.__mots[randint(0,len(self.__mots)-1)]#on tire un eniter au hasard entre 0 et la longueur de la liste mot 
        self.__trouve=["*" for i in range (len(self.__mot))]
        self.__mot_afficher.config(text="Mot :"+"*"*len(self.__mot))
            
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
