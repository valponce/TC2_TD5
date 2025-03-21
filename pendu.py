from tkinter import *

class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur,background="white")

class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)

        # paramètres de la fenêtre
        self.title('Jeu du pendu')
        self.configure(bg="blue")
        self.__boutons=[chr(ord('A')+i) for i in range(26)]
        
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
           Lettre=Button(clavier,text=self.__boutons[i],bg="white",width=8)
           if i<7:
               Lettre.grid(row=1, column=i,padx=5, pady=5)
           elif 7<=i<14:
               Lettre.grid(row=2, column=i-7,padx=5, pady=5)
           elif 14<= i <21:
               Lettre.grid(row=3, column=i-14,padx=5, pady=5)
           else:
               Lettre.grid(row=4, column=i-20,padx=5, pady=5)
        
        
        Mot=Label(self,text="Mot")
        Mot.pack(side=BOTTOM,padx=30,pady=10)
        
        #Création de la zone de dessin 
        self.canvas=ZoneAffichage(self, 300,300)
        self.canvas.pack(side=TOP, padx=30, pady=30)
        
        boutonQuitter.config(command=self.destroy)
        
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
