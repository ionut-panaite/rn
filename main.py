import pathlib


def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A=[]
    B=[]

    with open(path,"r",encoding="utf-8") as file:
        for line in file:
            linie=line.strip()
            print(linie)
            stanga, dreapta=linie.split("=")
            B.append(float(dreapta))
            termeni=stanga.split()
            print(termeni)
            semne=[]
            coef=[]
            for termen in termeni:
                if '-' in termen:
                    semne.append('-')
                if '+' in termen:
                    semne.append('+')
                if termen[-1] in "xyz":
                    if semne and semne.pop()=='-':
                        coef.append(-1.0)
                    else:
                        coef.append(1.0)
                    cifre=termen.strip("+-xyz")
                    if cifre:
                        nr=float(cifre)
                    else:
                        nr=1.0
                    coef[-1]*=nr
            A.append(coef)
    return A, B


A, B = load_system(pathlib.Path("file.txt"))
print(f"{A=} {B=}")

def determinant(matrix: list[list[float]]) -> float:
    det=0
    sz=len(matrix)
    if sz==2:
        return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    for i in range(sz):
        d=1
        for j in range(0,sz):
                d*=matrix[(i+j)%sz][j]
        det+=d
    for i in range(sz):
        d=1
        for j in range(0,sz):
                d*=matrix[(i+j)%sz][sz-1-j]
        det-=d
    return det

print(f"{determinant(A)=}")

def trace(matrix: list[list[float]]) -> float:
    sum=0
    for i in range(len(matrix)):
        sum+=matrix[i][i]
    return sum

print(f"{trace(A)=}")

def norm(vector: list[float]) -> float:
    sum=0
    for i in range(len(vector)):
        sum+=vector[i]**2
    sum=sum**(1/2)
    return sum

print(f"{norm(B)=}")

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    matrix=[lin[:] for lin in matrix]
    for i in range(len(matrix)):
        for j in range(i):
            matrix[i][j], matrix[j][i]=matrix[j][i], matrix[i][j]
    return matrix

print(f"{transpose(A)=}")

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    solve=[0,0,0]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            solve[i]+=matrix[i][j]*vector[j]
    return solve

print(f"{multiply(A, B)=}")

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    ans=[]
    for i in range(len(matrix)):
        cop=[row[:] for row in matrix]
        for j in range(len(matrix)):
            cop[j][i]=vector[j]
        ans.append(determinant(cop)/determinant(matrix))
    return ans

print(f"{solve_cramer(A, B)=}")

def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    #devine 2*2
    new_m=[row[:j]+row[j+1:] for row in (matrix[:i]+matrix[i+1:])]
    return new_m

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    #devine cu -1 si 1
    new_m=[]
    for i in range(len(matrix)):
        new_line=[]
        for j in range(len(matrix)):
            new_line.append((-1)**(i+j)*determinant(minor(matrix,i,j)))
        new_m.append(new_line)
    return new_m

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    #trasnpusa de cofactor
    return transpose(cofactor(matrix))

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    inverse=adjoint(matrix)
    det=determinant(matrix)
    for i in range(len(matrix)):
            for j in range(len(matrix)):
                inverse[i][j]/=det
    return multiply(inverse, vector)

print(f"{solve(A, B)=}")
print(minor(A,0,0))