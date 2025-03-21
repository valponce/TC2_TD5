from tkinter import *
from random import randint


class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur,background="white")


class MonBoutonLettre(Button):
    def __init__(self,parent,i):
        lettre=chr(ord('A')+i)
        Button.__init__(self,parent,text=lettre,width=6)
        self.__lettre=lettre
        self.config(state='disabled',command=self.cliquer)
    def cliquer(self):
        self.config(state='disabled')
        fen.traitement(self.__lettre)
        
class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)

        # paramètres de la fenêtre
        self.title('Jeu du pendu')
        self.configure(bg="blue")
        #self.__lettres=[chr(ord('A')+i) for i in range(26)]
        self.__boutons=[]
        self.__listeMots=None
        self.__mot_affiche=None
        self.__mot=""
        self.__trouve=[]
        self.__nb_manque=0
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
        self.canvas.pack(side=TOP, padx=30, pady=30)
        
        #Configuration des boutons
        #self.__boutons[0].config(command= lambda :self.traitement(0))
        #self.__boutons[1].config(command= lambda :self.traitement(1))
        
        boutonQuitter.config(command=self.destroy)
        boutonNouvellePartie.config(command=self.nouvelle_partie)
    
    def chercher_lettre(self,lettre,mot):
        position=[]
        for i in range(len(mot)):
            if mot[i]==lettre:
                position.append(i)
        return position
    
    def afficher_lettre(self,position,lettre):
        for k in position:
            self.__trouve[k]=lettre
        
        self.__mot_afficher.config(text="Mot :"+separateur.join(self.__trouve))
        
    def traitement(self,lettre):
        for i in range(len(self.__mot)):
            if self.__mot[i]==lettre:
                self.__trouve[i]=lettre
        separateur=""
        self.__mot_afficher.config(text="Mot :"+str(separateur.join(self.__trouve))) 
        #position=self.chercher_lettre(lettre,self.__mot)
        #self.afficher_lettre(position,lettre)
        
        
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
        self.__trouve=["*" for i in range (len(self.__mot))]
        self.__mot_afficher.config(text="Mot :"+"*"*len(self.__mot))
            
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
