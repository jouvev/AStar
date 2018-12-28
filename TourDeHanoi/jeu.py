class Plateau:
    #creation d'un plateau de jeu en 2 dimensions avec quelques méthodes comme
    #la copie du plateau ou le test d'égalité
    def __init__(self,h,w):
        self.w=w
        self.h=h
        self.plat = [[0 for i in range(h)] for j in range(w)]

    def copie(self):
        #renvoie une copie du plateau
        w=self.w
        h=self.h
        res=Plateau(h,w)
        res.plat= [[self.plat[j][i] for i in range(h)] for j in range(w)]
        return res

    def egal(self,p):
        #renvoie true si les 2 plateaux sont égaux sinon false
        w=self.w
        h=self.h
        for i in range(h):
            for j in range(w):
                if(p.plat[j][i]!=self.plat[j][i]):
                    return False
        return True

    def affichage(self):
        res=""
        for i in range(self.h):
            for j in range(self.w):
              res+=str(self.plat[j][i])+" "
            res+="\n"
        print(res)

    def chercher(self,n):
        for c in range(self.w):
            for l in range(self.h):
                if(self.plat[c][l]==n):
                    return c,l

    def heuristique(self):
        s=0
        for poid in range(1,self.h+1):
            if(self.plat[2][poid-1]!=poid):
                #on le cherche
                c,i=self.chercher(poid)
                #puis on compte le nombre de palets au-dessus lui
                while (i>=0 and self.plat[c][i]!=0):
                    s+=1
                    i-=1
        return s
                

class TourHanoi:
    #represente le jeu tour de hanoi
    def __init__(self,d):
        #on initialise le jeu ou d represente la difficulte cad hauteur de la tour
        #lecture du plateau
        #|------>(x)
        #|
        #|
        #v
        #(y)
        self.jeu = Plateau(d,3)
        for i in range(d):
            self.jeu.plat[0][i]=i+1
        self.listeCoupsValides=None

    def joueCoup(self,coup):
        #joue le coup:[x,y,x',y'] donc on deplace la piece du 
        #en x,y vers x',y'
        #on fait l'hypothese que le coup est valide
        self.jeu.plat[coup[2]][coup[3]]=self.jeu.plat[coup[0]][coup[1]]
        self.jeu.plat[coup[0]][coup[1]]=0
        self.listeCoupsValides=None

    def indiceMax(self,c):
        #renvoie l'indice de la ligne de la piece la plus haute de la colone c
        for i in range(self.jeu.h):
            if(self.jeu.plat[c][i]!=0):
                return i
        return self.jeu.h

    def coupsValides(self):
        #renvoie la liste des coups valides
        #coup:[x,y,x',y']
        if(self.listeCoupsValides!=None):
            return self.listeCoupsValides

        res=[]
        for c in range(self.jeu.w):
            cMax=self.indiceMax(c)
            if(cMax==self.jeu.h):
                #pas de pièce à prendre dans cette colone
                continue
            for c2 in range(self.jeu.w):
                if(c2==c):
                    #on ne deplace pas une piece vers la même colone
                    continue
                c2Max=self.indiceMax(c2)
                if(c2Max==self.jeu.h \
                   or self.jeu.plat[c2][c2Max]>self.jeu.plat[c][cMax]):
                    #donc c'est un coup valide on l'ajoute
                    res.append([c,cMax,c2,c2Max-1])
        self.listeCoupsValides=res
        return res

    def terminer(self):
        #renvoie true si la partie est termine selon les regles du jeu
        #sinon false
        for i in range(self.jeu.h):
            if(self.jeu.plat[2][i]!=i+1):
                return False
        return True

    def copie(self):
        res=TourHanoi(0)
        res.jeu=self.jeu.copie()
        return res

#######Noeud#######
class Noeud:
    def __init__(self,j):
        #plateau de jeu et un plateau parent
        self.jeu=j
        self.cout=0
        self.heuristique=0
        self.parent=0#numero du parent

    def compNoeud(self,n2):
        #si n1 est meilleur que n2 renvoie 1, 0 sinon 
        if (self.heuristique < n2.heuristique):
            return 1
        else:
            return 0

    def copie(self):
        res=Noeud(self.jeu.copie())
        res.cout=self.cout
        res.heuristique=self.heuristique
        res.parent=self.parent
        return res

    def listeVoisins(self):
        coupsValides=self.jeu.coupsValides()
        res=[]
        for c in coupsValides:
            copie=self.jeu.copie()
            copie.joueCoup(c)
            res.append(Noeud(copie))
        return res

######FILE#######
class FilePrioritaire:
    def __init__(self,l=[]):
        #création d'une liste prioritaire
        self.l=l

    def insert(self,e):
        #insert l'element e par rapport a une fonction de comparaison comp
        i=0
        while (i < len(self.l) and e.compNoeud(self.l[i])==0):
            i+=1
        self.l.insert(i,e.copie())

    def depiler(self):
        #retire et renvoie l'élèment en tête
        return self.l.pop(0)

    def isEmpty(self):
        return len(self.l)==0

    def remove(self,jeu):
        for i in range(len(self.l)):
            if(self.l[i].jeu.jeu.egal(jeu)):
                self.l.pop(i)
                return 


########ALGO A*#########
def restituerChemin(l):
    #renvoie une liste de noeuds qui reprensent le chemin trouvé par l'algo a*
    #affichage closedlist
    #for e in l:
     #   e.printN()
        
    tmp=l[-1]
    res=[tmp]
    while( tmp.x!=l[0].x or tmp.y!=l[0].y):
        res.insert(0,tmp)
        i=indexfind(l,tmp.px,tmp.py)
        tmp=l[i]
    res.insert(0,l[0])
    return res

def estDansList(l,n):
    for n2 in l:
        if(n.jeu.jeu.egal(n2.jeu.jeu)):
            return True
    return False

def indexfind(l,n):
    for i in range(len(l)):
            if(l[i].jeu.jeu.egal(n.jeu.jeu)):
                return i

def restituerChemin(l,depart):
    #renvoie une liste de noeuds qui reprensent le chemin trouvé par l'algo a*
    #affichage closedlist
    #for e in l:
     #   e.printN()
        
    tmp=l[-1]
    res=[]
    while( tmp.jeu.jeu.egal(depart.jeu.jeu)==False):
        res.insert(0,tmp.jeu.jeu)
        tmp=l[tmp.parent]
    res.insert(0,depart.jeu.jeu)
    return res

def affichage(chemin):
    #for p in chemin:
        #p.affichage()
    print("gg en {0}".format(len(chemin)-1))

def resolve(depart):
    #algo a*
    closedList=[]
    openList=FilePrioritaire([depart])
    while( not(openList.isEmpty()) ):
        u = openList.depiler()

        if(u.jeu.terminer()):
            #on a trouver on reconstitu le chemin
            closedList.append(u)
            affichage(restituerChemin(closedList,depart))
            return

        for v in u.listeVoisins():
            if ( not(estDansList(closedList,v))):
                cout=u.cout+1
                heuristique=cout+v.jeu.jeu.heuristique()
                if (estDansList(openList.l,v)):
                    i=indexfind(openList.l,v)
                    if(heuristique < openList.l[i].heuristique):
                        #remove puis insert
                        v.cout=cout
                        v.heuristique=heuristique
                        v.parent=len(closedList)
                        openList.remove(v.jeu.jeu)
                        openList.insert(v)
                        
                else:
                    #insert
                    v.cout=cout
                    v.heuristique=heuristique
                    v.parent=len(closedList)
                    openList.insert(v)
        closedList.append(u.copie())
    print("erreur")

if (__name__=="__main__"):
    j=TourHanoi(7)
    n=Noeud(j)
    resolve(n)
