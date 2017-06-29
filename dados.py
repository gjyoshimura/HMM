import csv
import numpy as np

def viterbi(obs, states, start_p, trans_p, emit_p):

    V = [{}]

    for st in states:

        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}

    # Run Viterbi when t > 0

    for t in range(1, len(obs)):

        V.append({})

        for st in states:

            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)

            for prev_st in states:

                if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:

                    max_prob = max_tr_prob * emit_p[st][obs[t]]

                    V[t][st] = {"prob": max_prob, "prev": prev_st}

                    break

    for line in dptable(V):

        print (line)

    opt = []

    # The highest probability

    max_prob = max(value["prob"] for value in V[-1].values())

    previous = None

    # Get most probable state and its backtrack

    for st, data in V[-1].items():

        if data["prob"] == max_prob:

            opt.append(st)

            previous = st

            break

    # Follow the backtrack till the first observation

    for t in range(len(V) - 2, -1, -1):

        opt.insert(0, V[t + 1][previous]["prev"])

        previous = V[t + 1][previous]["prev"]


    print ('The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob)


def dptable(V):

    # Print a table of steps from dictionary

    yield " ".join(("%12d" % i) for i in range(len(V)))

    for state in V[0]:

        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)



def main ():
    with open('dados_trabalhados_v2.csv', newline='') as f:
        reader = csv.reader(f)

        
        matrix = list(reader)
        
        #print (matrix[0][10])
        
        size = len(matrix)
        #print(size)
        matrix_float = np.zeros((size,11))

        
        #print (matrix[0])

    #transforma os campos da matrix em float
        for i in range(size):
            for j in range(11):
                matrix_float[i][j] = float(matrix[i][j])

        #print (matrix_float[0][10])


    #Calcula as probabilidades de chuva e sol 
        count_chuva = 0
        count_sol = 0
        count_chuva_sol = 0
        count_sol_chuva = 0
        count_sol_sol = 0
        count_chuva_chuva = 0
        for i in range(1, size):
            if matrix_float[i-1][10] > 0.00:
                count_chuva += 1
                if matrix_float[i][10] == 0.0:
                    count_chuva_sol += 1
                else:
                    count_chuva_chuva += 1
            if matrix_float[i-1][10] == 0.00:       
                count_sol += 1  
                if matrix_float[i][10] > 0.00:
                    count_sol_chuva += 1 
                else:
                    count_sol_sol += 1
        prob_sol = count_sol/size
        prob_chuva = count_chuva/size
        prob_chuva_sol = count_chuva_sol/size
        prob_sol_chuva = count_sol_chuva/size
        prob_sol_sol = count_sol_sol/size
        prob_chuva_chuva = count_chuva_chuva/size
        

        print("CHUVA: %f"% (prob_chuva))
        print("SOL: %f"% (prob_sol))
        print("CHUVA_SOL: %f"% prob_chuva_sol)
        print("SOL_CHUVA: %f"% prob_sol_chuva)
        print("SOL_SOL: %f"% prob_sol_sol)
        print("CHUVA_CHUVA: %f"% prob_chuva_chuva)

        umid_min_chuva = 10000
        umid_med_chuva = 0
        umid_max_chuva = 0
        umid_min_sol = 10000
        umid_med_sol = 0
        umid_max_sol = 0

        count_chuva = 0
        count_sol = 0
        for i in range(size):
            if matrix_float[i][10] > 0.00:
                if umid_min_chuva > matrix_float[i][4]:
                    umid_min_chuva = matrix_float[i][4]
                if umid_max_chuva < matrix_float[i][4]:
                    umid_max_chuva = matrix_float[i][4]
                umid_med_chuva += matrix_float[i][4]
                count_chuva += 1
            else:
                if umid_min_sol > matrix_float[i][4]:
                    umid_min_sol = matrix_float[i][4]
                if umid_max_sol < matrix_float[i][4]:
                    umid_max_sol = matrix_float[i][4]
                umid_med_sol += matrix_float[i][4]
                count_sol += 1
        
        umid_med_chuva = umid_med_chuva/count_chuva
        umid_med_sol = umid_med_sol/count_sol  
        
        #print("CHUVA: umidade_min = %f\numidade_med = %f\numidade_max = %f  " % (umid_min_chuva, umid_med_chuva, umid_max_chuva))
        #print("SOL: umidade_min = %f\numidade_med = %f\numidade_max = %f  " % (umid_min_sol, umid_med_sol, umid_max_sol))
        
        prob_umid_maior_med_chuva = 0
        prob_umid_menor_med_chuva = 0
        prob_umid_maior_med_sol = 0
        prob_umid_menor_med_sol = 0
        for i in range(size):
            if matrix_float[i][10] > 0.00:        
                if matrix_float[i][4] > umid_med_chuva:
                    prob_umid_maior_med_chuva += 1
                else: 
                    prob_umid_menor_med_chuva += 1
            else:
                if matrix_float[i][4] > umid_med_sol:
                    prob_umid_maior_med_sol += 1
                else:
                    prob_umid_menor_med_sol += 1

        prob_umid_maior_med_chuva = prob_umid_maior_med_chuva/count_chuva
        prob_umid_menor_med_chuva = prob_umid_menor_med_chuva/count_chuva
        prob_umid_maior_med_sol = prob_umid_maior_med_sol/count_sol
        prob_umid_menor_med_sol = prob_umid_menor_med_sol/count_sol
        
        print("CHUVA: \nprob_umid_maior_med_chuva = %f\nprob_umid_menor_med_chuva = %f\nSOL: \nprob_umid_maior_med_sol = %f\nprob_umid_menor_med_sol = %f "% (prob_umid_maior_med_chuva, prob_umid_menor_med_chuva, prob_umid_maior_med_sol, prob_umid_menor_med_sol))

    #observations
        obs = ('ALTA UMIDADE',	'ALTA UMIDADE',	'ALTA UMIDADE',	'ALTA UMIDADE',	'ALTA UMIDADE',	'ALTA UMIDADE',	'ALTA UMIDADE',	'ALTA UMIDADE',	'ALTA UMIDADE',	'ALTA UMIDADE',	'ALTA UMIDADE',	'ALTA UMIDADE') #media de umidade 
    #states
        states = ('SOL','CHUVA')
            
    #start_probability
        pi = {'SOL': prob_sol, 'CHUVA': prob_chuva}
    #transition_probability
        prob_sol_chuva = 1 - prob_sol_sol
        prob_chuva_sol = 1 - prob_chuva_chuva
        A = {
                'SOL': {'SOL': prob_sol_sol, 'CHUVA': prob_sol_chuva},      
                'CHUVA': {'SOL': prob_chuva_sol, 'CHUVA': prob_chuva_chuva}
            }
    #emission_probability
        B = {
                'SOL': {'ALTA UMIDADE': prob_umid_maior_med_sol, 'BAIXA UMIDADE': prob_umid_menor_med_sol},       
                'CHUVA': {'ALTA UMIDADE': prob_umid_maior_med_chuva, 'BAIXA UMIDADE': prob_umid_menor_med_chuva}
            }     

        viterbi(obs, states, pi, A, B)

if __name__ == "__main__":
    main()
