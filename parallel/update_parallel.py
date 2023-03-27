def update(routes, liste, dico, rho, alpha, Q, Me):
    #print("updating routes : "+str(routes))
    old_dico = [x for x in dico['mat1']]
    new_dico = dico.copy()
    compteur = [0,0,0]
    for route, number, scores in routes:
        if scores != -99 :
            for i in range(len(route)):
                compteur[route[0]] += 1
                if i==0:
                    #print("old dico['mat1'] : ")
                    #print(dico['mat1'])
                    new_dico['mat1'][liste['liste1'].index(route[i])] **= 1/alpha
                    new_dico['mat1'][liste['liste1'].index(route[i])] *= rho
                    new_dico['mat1'][liste['liste1'].index(route[i])] += (number * Q)
                    new_dico['mat1'][liste['liste1'].index(route[i])] **= alpha
                    #if Me == 0 :
                    #    print("nouveau = ancien^1/{} * {} + {} )^{}".format(alpha,rho,number*Q,alpha))
                    #print("new dico['mat1'] : ")
                    #print(dico['mat1'])
                else:
                    new_dico[f'mat{i+1}'][liste[f'liste{i}'].index(route[i-1])][liste[f'liste{i+1}'].index(route[i])] **= 1/alpha
                    new_dico[f'mat{i+1}'][liste[f'liste{i}'].index(route[i-1])][liste[f'liste{i+1}'].index(route[i])] *= rho
                    new_dico[f'mat{i+1}'][liste[f'liste{i}'].index(route[i-1])][liste[f'liste{i+1}'].index(route[i])] += (number * Q)
                    new_dico[f'mat{i+1}'][liste[f'liste{i}'].index(route[i-1])][liste[f'liste{i+1}'].index(route[i])] **= alpha
    print("old dico : {}; new dico : {}".format(old_dico,new_dico['mat1']))
    print("and compteur : {}".format(compteur))
    return new_dico
