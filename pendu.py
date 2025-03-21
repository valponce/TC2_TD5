from tkinter import *
from random import randint


class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur,background="white")

class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)

        # paramètres de la fenêtre
        self.title('Jeu du pendu')
        self.configure(bg="blue")
        self.__lettres=[chr(ord('A')+i) for i in range(26)]
        self.__boutons=[]
        self.__listeMots=None
        self.__mot=None
        self.__nb_manques=0
        self.chargeMots()
        
        
        #Création barre outils
        barreOutils= Frame(self,bg="grey")
        barreOutils.pack(side=TOP, padx=30,pady=10)
        
        boutonNouvellePartie=Button(barreOutils, text='Nouvelle partie',bg="white")
        boutonNouvellePartie.pack(side=LEFT, padx=15, pady=5)
        
        boutonQuitter = Button(barreOutils, text='Quitter',bg="white")
        boutonQuitter.pack(side=LEFT, padx=15, pady=5)
        
        #Création du clavier
        clavier= Frame(self,bg="grey")
        clavier.pack(side=BOTTOM,padx=30,pady=10)
        for i in range(26):
           Lettre=Button(clavier,text=self.__lettres[i],bg="white",width=8,state='disabled')
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
        Mot=Label(self,text="Mot")
        Mot.pack(side=BOTTOM,padx=30,pady=10)
        
        #Création de la zone de dessin 
        self.canvas=ZoneAffichage(self, 300,300)
        self.canvas.pack(side=TOP, padx=30, pady=30)
        
        #Configuration des boutons
        for i in range(26):
            b[i].config(command=self.traitement(i))
        
        boutonQuitter.config(command=self.destroy)
        boutonNouvellePartie.config(command=self.nouvelle_partie)
    
    def chercher_lettre
    def traitement(self,i):
        
    def chargeMots(self):
        f = open('mots.txt', 'r')
        s=f.read()
        self.__mots = s.split('\n')
        f.close()

    def nouvelle_partie(self):
        self.nouveau_mot()
        for b in self.__boutons:
            b.config(state="normal")
        
            
    def nouveau_mot(self):
        self.__mot=self.__mots[randint(0,len(self.__mots)-1)]#on tire un eniter au hasard entre 0 et la longueur de la liste mot 
        self.__nb_manques=len(self.__mot)
            
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
