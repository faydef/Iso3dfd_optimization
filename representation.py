import numpy as np

def initiate(problem):
    liste = dict()
    liste['liste1'] = ['O2', 'O3', 'Ofast']
    liste['liste2'] = ['avx', 'avx2', 'avx512']
    liste['liste3'] = [k for k in range(1,33)]
    liste['liste4'] = [16*k for k in range(1,problem[0]//16)]
    liste['liste5'] = [k for k in range(1, problem[1]+1)]
    liste['liste6'] = [k for k in range(1, problem[2]+1)]
    
    dico = dict()
    dico['mat1'] = np.array([1/len(liste['liste1']) for el in liste['liste1']])
    for k in range(2,7):
        dico[f'mat{k}'] = np.array([[1/len(liste[f'liste{k}']) for el in liste[f'liste{k}']]for el in liste[f'liste{k-1}']])
    return liste, dico
    # mat2 = np.array([[1/len(liste2) for el in liste2]for el in liste1])
    # mat3 = np.array([[1/len(liste3) for el in liste3]for el in liste2])
    # mat4 = np.array([[1/len(liste4) for el in liste2]for el in liste3])
    # mat5 = np.array([[1/len(liste5) for el in liste2]for el in liste4])
    # mat6 = np.array([[1/len(liste6) for el in liste2]for el in liste5])





