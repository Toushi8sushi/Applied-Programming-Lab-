def print_mat(A):
    for i in range(len(A)):
        print(A[i])
def gausselim(A, B):
    #Forward elemenation
    variables=len(A[0]) #no of variables in this system of equations
    equations=len(A) # no of equations for this system

    for i in range(variables-1): # we do not touch the last variable
       
        for j in range(i+1,equations):#first equation is not touched 
          
            factor=A[j-1][i]/A[j][i]
            ''' print("------------normalized--------")
            print("factor",factor)'''
            for k in range(i,variables):#multiplying factor to all terms in the 'J'th equation
                A[j][k]*=factor
            B[j]*=factor # updating the constant matrix as well
            ''' print_mat(A)
            print()
            print(B)
            print()'''

        # Jth equation is normalized 
        for h in range(i+1,equations):
            for k in range(0,variables): #can put range(i,variables)
                A[h][k]-=A[i][k]
            B[h]-=B[i]
            '''print("-----------subtracted--------")
            print_mat(A)
            print()
            print(B)
            print()'''
    print_mat(A)
    print()
    print(B)
    print()
    
    #Back substituiton 
    for i in range(-1,-equations-1,-1):#using negative indexing in python
        for k in range(-1,i,-1):
            B[i]-=B[k]*A[i][k]
        B[i]=B[i]/A[i][i] #[i][i] is a coincidence 
    return B

#test to check for correctness 
A = [ [ 2,5,2 ] , [ 3,-2,4 ] , [ -6,1,-7 ] ]
B = [ -38,17,-12 ]
Bout = gausselim(A, B)
print_mat(B)
Bexp = [3,-8,-2]
s = 0
for i in range(len(Bout)):
    s += abs(Bout[i] - Bexp[i])
if s < 0.01:
  print("PASS")
else:
  print("FAIL")

A = [[0.26399197, 0.7078364 , 0.74605183, 0.52658905],
       [0.3187093 , 0.69157511, 0.55497212, 0.72189566],
       [0.96727446, 0.57382705, 0.74889902, 0.76056476],
       [0.58070383, 0.97389366, 0.26139946, 0.00913732]]
B = [0.0140597 , 0.46419182, 0.20868931, 0.65451389]
Bout = gausselim(A, B)
print_mat(B)
Bexp = [ 0.19335079,  0.96322792, -1.54304119,  0.82112907]
s = 0
for i in range(len(Bout)):
    s += abs(Bout[i] - Bexp[i])
if s < 0.01:
  print("PASS")
else:
  print("FAIL")