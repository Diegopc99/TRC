from subprocess import Popen, PIPE
import os

def minimum(a,b): 

    if a <= b: 
        return a 
    else: 
        return b 


print("Introduce rango de valores de i (ej -> 0/50):")
rango_i = input()
min_i = rango_i.split("/")[0]
max_i = rango_i.split("/")[1]

if (int(min_i) == 0):
    num_iteraciones = int(max_i) - int(min_i) +1
elif (int(min_i) < 0):
    num_iteraciones = int(max_i) + abs(int(min_i))
elif (int(min_i) > 0):
    num_iteraciones = int(max_i) - int(min_i) 
    

print("Introduce valor de m:")
m = input()

print("Introduce valor de S (tiempo de servicio):")
S = input()

print("Introduce valor de q (intervalo de confianza):")
q = input()

print("Introduce valor de seed:")
seed = input()

iteracion = 0
PBlockAnt = 0

if os.path.exists('gnuplot/trafico_simple.plot'):
    os.remove("gnuplot/trafico_simple.plot")

if os.path.exists('gnuplot/trafico_doble.plot'):
    os.remove("gnuplot/trafico_doble.plot")

if os.path.exists('gnuplot/trafico_total.plot'):
    os.remove("gnuplot/trafico_total.plot")


for i in range(int(min_i),int(max_i)+1):

    ######################################
    ########### Calculamos r #############
    ######################################

    r = (1-(0.04*i))

    ######################################
    ######### Calculamos landa ###########
    ######################################

    landa_simple = (25*r)/int(S)
    landa_dual = (25*r)/(int(S)*2)

    ######################################
    #### Generamos fichero config.cfg ####
    ######################################

    with open('config/config'+str(i)+'.cfg', 'w') as fw:
        fw.write(""+m+" "+m+" "+m+" "+m+"\n")
        fw.write("8\n")

        # Trafico simple
        for p in range(4):
            fw.write("M "+str(1/landa_simple)+"\n")
            fw.write("M "+S+"\n")
            #fw.write(str(i)+" a\n")
            if(p == 0):
                fw.write("0 3,2,1 a\n")
            if(p == 1):
                fw.write("1 0,3,2 a\n")
            if(p == 2):
                fw.write("2 1,0,3 a\n")
            if(p == 3):
                fw.write("3 2,1,0 a\n")
            

        # Trafico dual
        for j in range(4):
            fw.write("M "+str(1/landa_dual)+"\n")
            fw.write("M "+S+"\n")
            if(j == 0):
                fw.write("0,1 3,2 b\n")
            if(j == 1):
                fw.write("1,2 0,3 b\n")
            if(j == 2):
                fw.write("2,3 1,0 b\n")
            if(j == 3):
                fw.write("3,0 2,1 b\n")
            
    ################################
    ######## Calculo de t ##########
    ################################

    if iteracion == 0:
        t = 0.002
    else:
        t = minimum(1 , ((1-PBlockAnt)/PBlockAnt)*0.002)

    #####################################
    ###### Ejecutamos el simulador ######
    #####################################

    process = Popen(["./SimRedMMkk","-s",str(seed),"-q",str(q),"-t",str(t),"config/config"+str(i)+".cfg"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    os.rename("config/config"+str(i)+".cfg.out", "config_out/config"+str(i)+".cfg.out")

    ##################################################
    #### Guardamos los valores en el fichero plot ####
    ##################################################

    with open('gnuplot/sim.plot', 'a') as fw:

        fr = open('config_out/config'+str(i)+'.cfg.out', 'r')
        lines = fr.readlines()
        fr.close()
        count = 0
        for line in lines:
            if count == 4:
                res = line.split(" ")
                prob_block_a = res[4][:-1]
                print("probabilidad de bloqueo a: "+prob_block_a+"\n")
            if count == 5:
                first_interval_a = line.split("(")[1].split(",")[0]
                second_interval_a = line.split("(")[1].split(",")[1].split(")")[0]
                print("first interval_a: "+first_interval_a+"\n")
                print("second_interval_a: "+second_interval_a+"\n")
            if count == 14:
                res = line.split(" ")
                prob_block_b = res[4][:-1]
                print("probabilidad de bloqueo b: "+prob_block_b+"\n")
            if count == 15:
                first_interval_b = line.split("(")[1].split(",")[0]
                second_interval_b = line.split("(")[1].split(",")[1].split(")")[0]
                print("first interval_b: "+first_interval_b+"\n")
                print("second_interval_b: "+second_interval_b+"\n")
            count+=1

        A = (float(landa_simple)*int(S))
        AT = A + (A/2) + (A/2)

        ###################################################
        ############### Valor de B minimo #################
        ###################################################

        Acmin_trafico_a = A*(1-float(second_interval_a))
        Acmin_trafico_b = (A/2)*(1-float(second_interval_b))
        
        Acmin = Acmin_trafico_a + (2*Acmin_trafico_b) 

        ###################################################
        ############### Valor de B maximo #################
        ###################################################

        Acmax_trafico_a = A*(1-float(first_interval_a))
        Acmax_trafico_b = (A/2)*(1-float(first_interval_b))

        Acmax = Acmax_trafico_a + (2*Acmax_trafico_b) 

        ###################################################
        ############### Valor de B medio ##################
        ###################################################

        Acmed_trafico_a = A*(1-float(prob_block_a))
        Acmed_trafico_b = (A/2)*(1-float(prob_block_b))

        Ac = Acmed_trafico_a + (2*Acmed_trafico_b) 
        

        ######### Escribimos el fichero ###########

    with open('gnuplot/trafico_simple.plot', 'a') as fw:
        fw.write(""+str(A)+" "+str(Acmed_trafico_a)+" "+str(Acmin_trafico_a)+" "+str(Acmax_trafico_a)+"\n")

    with open('gnuplot/trafico_doble.plot', 'a') as fw:
        fw.write(""+str(A)+" "+str((Acmed_trafico_b*2))+" "+str((Acmin_trafico_b*2))+" "+str((Acmax_trafico_b*2))+"\n")

    with open('gnuplot/trafico_total.plot', 'a') as fw:
        fw.write(""+str(AT)+" "+str(Ac)+" "+str(Acmin)+" "+str(Acmax)+"\n")


    array = []
    array.append(prob_block_a)
    array.append(prob_block_b)
    array.append(first_interval_a)
    array.append(first_interval_b)
    array.append(second_interval_a)
    array.append(second_interval_b)

    PBlockAnt = float(max(array))
    print("Probabilidad de bloqueo maxima: "+str(PBlockAnt))
    iteracion+=1
    
os.chdir('gnuplot')

process = Popen(["gnuplot","config.gnuplot"], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()   

    

