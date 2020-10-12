import random
from random import choice
import time
import psutil 

def generateBoard(nQueens):
    stateBoard = list(random.randrange(N) for i in range(N))
    return stateBoard

##############################################################

def conflicted(state, row, col):
    '''coloca rainha na (linha/coluna) se conflito ocorrer'''
    return any(conflict(row, col, state[c], c)for c in range(col))
  
##############################################################
    
def conflict(row1, col1, row2, col2):
    '''coloca duas rainhas na (linha1/coluna1) e (linha2/coluna2)
       retorna True caso exista conflito entre duas colunas'''
    return ( (row1 == row2 or 
              col1 == col2 or  
              row1 - col1 == row2 - col2 or  
              row1 + col1 == row2 + col2 ) ) 
    
##############################################################

def goalTest(state):
    '''Checa se todas as colunas estao preenchidas sem conflitos'''
    if state[-1] == -1:
        return False
    return not any(conflicted(state, state[col], col)
                  for col in range(len(state)))

##############################################################

def nearStates(nQueens,state):
    nearStates = []
    '''Verfica se as colunas vizinhas estão vazias'''
    for row in range(nQueens):
        for col in range(nQueens):
            if col != state[row]:
                aux = list(state)
                aux[row] = col  # Troca a coluna p/ a vazia
                nearStates.append(list( aux )) 
    return nearStates
  
##############################################################

def loss(state):
    conflictsAmount = 0
    for (r1, c1) in enumerate(state):
        for (r2, c2) in enumerate(state):
            if (r1, c1) != (r2, c2):
                conflictsAmount += conflict(r1, c1, r2, c2)
    return -conflictsAmount/2
  
##############################################################
  
def randomNearStates(nQueens, state):
  return choice(nearStates(nQueens, state))

##############################################################

def searchBestsNeighs(neighbours, state):
    bestNeighbor = []
    
    neighbor = max(neighbours, key=lambda state: loss(state))
    bestNeighbor.append(neighbor)
    
    for n in neighbours:
    	if( loss(neighbor) == loss(n) ):
    		bestNeighbor.append(n)
      
    #recebe Numero entre 0 e o tamanho da lista 
    pos = random.randint(0,len(bestNeighbor)-1)
    return bestNeighbor[pos]

##############################################################

def hillClimbing(nQueens,state):
	current = state
	count = 0
 
	while True:
    #recebe estados proximos para mover rainhas
		neighbours = nearStates(nQueens, current)

		if not neighbours:
		    break	
    
		neighbour = searchBestsNeighs(neighbours, state)
		print("Neighbours State: ",neighbour)
  
    #verifica se a quantidade de conflitos é menor que em estado atual 
		if loss(neighbour) < loss(current):
		  break
  
		count += 1 
		current = neighbour
  
	print("Amount of changes: ", count,
        "\nLoss Function: ",loss(neighbour))
 
	return current

##############################################################

def printBoard(stateBoard):
    
    for i in range( len(stateBoard) ):
        for j in range( len(stateBoard) ):
            if (stateBoard[j] == i):
                print("Q ", end=" ")
            else:
                print("x ", end=" ")
        print("")

##############################################################
#Chamadas de execução

N = int(input("How many queens do you want Sr ? \nNumb of Queens: "))
print("Alright, lets test with ", N, "then")

stateBoard = generateBoard(N)
start = time.time()
stateBoard = hillClimbing(N, stateBoard)  
end = time.time()

#tratamento de tempo
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)

printBoard(stateBoard)
print(goalTest(stateBoard))
print("{:0>2}hrs {:0>2}min {:.2f}sec".format(int(hours),int(minutes),seconds))
print("Memory During the process:",psutil.virtual_memory().used ,"bytes") 
