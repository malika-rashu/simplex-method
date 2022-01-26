
import math
import sys


'''implemented simplex tableau method in the following code 
first the input file was read to store the values appropriately,
a tableau was created by combining A B and appending C as well in the last row,
checkOptimality function checks if the optimal solution is reached, 
keyRow and keyCol finds the pivot element and entering and leaving variable,
operations functions performs the necessary matrix operations,
simplex function repeats the procedure until optimality is reached
'''

inputfile =open(sys.argv[1],"r")

count=0
A=[]
while True:

    count+=1
    line = inputfile.readline()
    if count==1:
        m,n = list(map(int,line.split(' ')))
    elif count>1 and count<=1+m:
        A.append(list(map(float,line.split(' '))))
    elif count==2+m:
        B=list(map(float,line.split(' ')))
    elif count==3+m:
        C = list(map(float,line.split(' ')))
    if not line:
        break
    
 
inputfile.close()

#step one creating tableau
AB=[]
for i,j in zip(A,B):
  AB.append( i +[j])
C= [-1*i for i in C]
tableau = AB + [ C + [0] ]

#last row of the tableau is Z-C


#is the sol optimum
def checkOptimality(tab):
    #if any of the element of Z-C is positive, then optimality not attained yet
    
    for i in tab[-1]:
      if i>0:
        return False
    return True

#finding key col
def keyCol(tab):
    return tab[-1].index(max(tab[-1]))


#finding key row
def keyRow(tab,col):
    minratio=[]
    for i in tab[:-1]:
      if i[col]>0: 
        minratio.append(i[-1]/i[col])
      else:
        minratio.append(math.inf)
    return minratio.index(min(minratio))


#to make identity matrix with the new basic variables
def operations(tab,r,c):
    pivot = tab[r][c]
    tab[r] = [tab[r][j]/pivot for j in range(len(tab[r])) ]
    for i in range(len(tab)):
      if i!=r:
        f = [tab[r][j]*tab[i][c] for j in range(len(tab[r]))]
        arr = [tab[i][j]-f[j] for j in range(len(tab[r]))]
        tab[i] =arr
    return tab


def simplex(tableau):
    while not checkOptimality(tableau):
        Col = keyCol(tableau)
        Row = keyRow(tableau, Col)
        tableau = operations(tableau, Row, Col)
    
    #optimality achieved

    #finding all coloumns that constitute identity matrix to find out basic variables to find solution
    solution=[]
    for i in range(n):
      sum=0
      count=0
      if tableau[0][i]==1 or tableau[0][i]==0:
        for j in range(m):
          sum+= tableau[j][i]
          if tableau[j][i]==0:
            count+=1
          if tableau[j][i]==1:
            idx = j
      #appending corresponding b values to solution
      if count==m-1 and sum==1:
        solution.append(round(tableau[idx][-1],6))
        
      else:
        solution.append(0)
         

    print( "The optimal objective function value is " + str(round(tableau[-1][-1],6)))
    print("The optimal solution is " + str(solution))
    multiplesol=False
    for i in solution[:m]:
      #if any of the basic variables have value zero then multiple solutions otherwise unique
      if i==0:
        multiplesol=True

    if multiplesol:
      print("This LP has multiple optimal solutions")
    else:
      print("This LP has a unique optimal solution")

simplex(tableau)