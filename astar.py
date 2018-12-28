import math as m

#################################################
####################DEFINITION###################
#################################################


#######NOEUD#######
class Noeud:
    def  __init__(self,x,y,cout=0,heuristique=0):
       #coordonnées du noeud, cout et heuristique
       self.x=x
       self.y=y
       self.cout=cout
       self.heuristique=heuristique
       self.px=0#coordonnées du parent pour reconstituer le chemin
       self.py=0
       
    def printN(self):
        #affichage d'un noeud (pour debug)
        print("x={0}, y={1}, cout={2}, heuristique={3}, parent({4},{5})"\
              .format(self.x,self.y,self.cout,self.heuristique,self.px,self.py))

    def distance(self,n):
        #renvoie la distance entre le point n et lui
        return m.sqrt( (n.x-self.x)**2 + (n.y-self.y)**2 )

    def copie(self):
        #copie un noeud
        res=Noeud(self.x,self.y,self.cout,self.heuristique)
        res.px=self.px
        res.py=self.py
        return res

    def compNoeud(self,n2):
        #si n1 est meilleur que n2 renvoie 1, 0 sinon 
        if (self.heuristique < n2.heuristique):
            return 1
        else:
            return 0
        
######GRAPH######
class Graph:
    def __init__(self,h,w):
        #un graph est une liste de noeuds
        self.graph=[Noeud(x,y) for x in range(h) for y in range(w)]
        self.h=h
        self.w=w

    #method static
    def creation(m):
        #m:List[List[int]] si 1 il y a un mur on le retire donc du graph
        h=len(m)
        w=len(m[0])
        g=Graph(h,w)
        for i in range(h):
            for j in range(w):
                if m[i][j]==1:
                    g.remove(i,j)
        return g

    def printG(self):
        #affichage d'un graph cad la liste des noeuds qui le compose (pour debug)
        for n in self.graph:
            n.printN()

    def listeVoisins(self,n):
        #renvoie la liste de tous les voisins du n dans le graph(n n'est pas son propre voisin)
        #hypothese: n est dans le graph
        res=[]
        for e in self.graph:
            if (abs(e.x-n.x)<=1 and abs(e.y-n.y)<=1 and (e.x!=n.x or e.y!=n.y)):
                res.append(e)
        return res

    def remove(self,x,y):
        #retire un noeud du graph
        for e in self.graph:
            if e.x==x and e.y==y:
                self.graph.remove(e)
                break;

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

    def remove(self,x,y):
        i=indexfind(self.l,x,y)
        self.l.pop(i)

######FONCTION LIST########
def estDansList(l,x,y):
    #l est une liste de noeuds on verifie que n est dans l avec un coup inf
    for e in l:
        if(e.x==x and e.y==y):
            return True
    return False

def indexfind(l,x,y):
    for i in range(len(l)):
        if(l[i].x==x and l[i].y==y):
            return i


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
        
def resolve(g,nDepart,nArrivee):
    #algo a*
    closedList=[]
    openList=FilePrioritaire([nDepart])
    while( not(openList.isEmpty()) ):
        u = openList.depiler()

        if(u.x==nArrivee.x and u.y==nArrivee.y):
            #on a trouver on reconstitu le chemin
            closedList.append(u)
            affichage(g,restituerChemin(closedList))
            return

        for v in g.listeVoisins(u):
            if ( not(estDansList(closedList,v.x,v.y))):
                cout=u.cout+u.distance(v)
                heuristique=cout+v.distance(nArrivee)
                if (estDansList(openList.l,v.x,v.y)):
                    i=indexfind(openList.l,v.x,v.y)
                    if(heuristique < openList.l[i].heuristique):
                        #remove puis insert
                        v.cout=cout
                        v.heuristique=heuristique
                        v.px=u.x
                        v.py=u.y
                        openList.remove(v.x,v.y)
                        openList.insert(v)
                        
                else:
                    #insert
                    v.cout=cout
                    v.heuristique=heuristique
                    v.px=u.x
                    v.py=u.y
                    openList.insert(v)
        closedList.append(u.copie())
    print("erreur")

########AFFICHAGE###########
def affichage(g,chemin):
    #affichage console du graph avec le chemin:List[Noeud]
    str=""
    for x in range(g.h):
        for y in range(g.w):
            if( not(estDansList(g.graph,x,y))):
                str+="1 "
            else:
                if (estDansList(chemin,x,y)):
                    str+="* "
                else:
                    str+="0 "
        str+="\n"
    print(str)

##################################################
#######################MAIN#######################
##################################################

"""
     [[0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0]]
"""
carte1=\
     [[0,1,0,0,0,0,0,0,0,0],
      [0,1,0,0,0,0,0,0,0,0],
      [0,1,0,1,0,0,0,0,0,0],
      [0,1,0,1,0,1,1,1,1,1],
      [0,1,0,1,0,0,0,0,0,0],
      [0,1,0,1,0,0,0,0,0,0],
      [0,1,0,1,1,1,1,0,1,1],
      [0,0,0,1,0,0,0,0,0,0],
      [0,0,0,1,0,0,1,1,1,1],
      [0,0,0,1,0,0,0,0,0,0]]

carte2=\
     [[0,1,0,0,0,1,0,0,0,1],
      [0,1,0,1,0,1,0,1,0,1],
      [0,0,0,1,0,1,0,1,0,0],
      [1,1,1,1,0,1,0,1,1,0],
      [0,0,0,0,0,1,0,1,0,0],
      [0,1,1,1,1,1,0,1,0,1],
      [0,0,0,0,0,0,0,1,1,0],
      [1,1,1,1,1,1,1,1,0,0],
      [0,0,0,0,0,0,0,0,0,1],
      [0,0,0,0,0,0,0,0,0,0]]
    
if(__name__=="__main__"):
   carte=\
     [[0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,1,0,0,0,0],
      [0,0,0,0,0,1,0,0,0,0],
      [1,1,1,1,1,1,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,1,0,0,0,0,0,0],
      [0,0,0,1,0,0,0,0,0,0],
      [0,0,0,1,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0]]

   g=Graph.creation(carte2)
   resolve(g,g.graph[0],g.graph[-1])
