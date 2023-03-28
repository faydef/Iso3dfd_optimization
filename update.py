def update(routes, liste, dico, rho, alpha, Q):
    for route, number, scores in routes:
        if scores != -99 :
            for i in range(len(route)):
                if i==0:
                    dico['mat1'][liste['liste1'].index(route[i])] **= 1/alpha
                    dico['mat1'][liste['liste1'].index(route[i])] *= rho
                    dico['mat1'][liste['liste1'].index(route[i])] += (number * Q)
                    dico['mat1'][liste['liste1'].index(route[i])] **= alpha
                else:
                    dico[f'mat{i+1}'][liste[f'liste{i}'].index(route[i-1])][liste[f'liste{i+1}'].index(route[i])] **= 1/alpha
                    dico[f'mat{i+1}'][liste[f'liste{i}'].index(route[i-1])][liste[f'liste{i+1}'].index(route[i])] *= rho
                    dico[f'mat{i+1}'][liste[f'liste{i}'].index(route[i-1])][liste[f'liste{i+1}'].index(route[i])] += (number * Q)
                    dico[f'mat{i+1}'][liste[f'liste{i}'].index(route[i-1])][liste[f'liste{i+1}'].index(route[i])] **= alpha
