from subprocess import Popen, PIPE
import re
import os
import json


def minimum(a,b): 

    if a <= b: 
        return a 
    else: 
        return b 
    

def create_plot_files():

    with open('basic_config.gnuplot', 'r') as src_file, open('gnuplot/config.gnuplot', 'w') as dest_file:
        # Read the contents of the source file
        file_contents = src_file.read()

        # Write the contents to the destination file
        dest_file.write(file_contents)

        # Append some additional text to the destination file
        dest_file.write("set title 'Encaminamiento 1'\n")
        dest_file.write("set key left top\n")
        dest_file.write("set output './traficos_simples.png'\n")
        dest_file.write("plot 'trafico_a.plot' with yerrorlines linecolor rgb '#001DBC' lw 2 title 'Tráfico A', 'trafico_b.plot' with yerrorlines linecolor rgb '#B85450' lw 2 title 'Tráfico B',\
                         'trafico_c.plot' with yerrorlines linecolor rgb '#B09500' lw 2 title 'Tráfico C', 'trafico_d.plot' with yerrorlines linecolor rgb '#3A5431' lw 2 title 'Tráfico D' \n")
        dest_file.write("pause 1\n")

        dest_file.write("set output './traficos_dobles.png'\n")
        dest_file.write("set key left top\n")
        dest_file.write("plot 'trafico_e.plot' with yerrorlines linecolor rgb '#432D57' lw 2 title 'Tráfico E', 'trafico_f.plot' with yerrorlines linecolor rgb '#C73500' lw 2 title 'Tráfico F', \
                        'trafico_g.plot' with yerrorlines linecolor rgb '#314354' lw 2 title 'Tráfico G', 'trafico_h.plot' with yerrorlines linecolor rgb '#10739E' lw 2 title 'Tráfico H', 'trafico_i.plot' \
                         with yerrorlines linecolor rgb '#B46504' lw 2 title 'Tráfico I', 'trafico_j.plot' with yerrorlines linecolor rgb '#82B366' lw 2 title 'Tráfico J' \n")
        dest_file.write("pause 1\n")

        

def generate_plot(A, data):

    bloqueo = []

    bloqueo.append(list(data.items())[0]) ## Corresponde con el promediador a
    bloqueo.append(list(data.items())[1]) ## Corresponde con el promediador b
    bloqueo.append(list(data.items())[2]) ## Corresponde con el promediador c
    bloqueo.append(list(data.items())[3]) ## Corresponde con el promediador d
    bloqueo.append(list(data.items())[4]) ## Corresponde con el promediador e
    bloqueo.append(list(data.items())[5]) ## Corresponde con el promediador f
    bloqueo.append(list(data.items())[6]) ## Corresponde con el promediador g
    bloqueo.append(list(data.items())[7]) ## Corresponde con el promediador h
    bloqueo.append(list(data.items())[8]) ## Corresponde con el promediador i
    bloqueo.append(list(data.items())[9]) ## Corresponde con el promediador j

    for bloqueo_trafico in bloqueo:
        
        promediador = bloqueo_trafico[0]
        AC_min = A*(1-float(bloqueo_trafico[1]['Confidence interval 1'][0]))
        AC_max = A*(1-float(bloqueo_trafico[1]['Confidence interval 1'][1]))
        AC_med = A*(1-float(bloqueo_trafico[1]['Probabilidad de bloqueo']))

        with open('gnuplot/trafico_'+str(promediador)+'.plot', 'a') as fw:
            fw.write(""+str(A)+" "+str(AC_med)+" "+str(AC_min)+" "+str(AC_max)+"\n")



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

for file_name in os.listdir('./gnuplot'):
    file_path = os.path.join('./gnuplot', file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)

create_plot_files() ## Tantos plot files como casos tengamos

for i in range(int(min_i),int(max_i)+1):

    ######################################
    ########### Calculamos r #############
    ######################################

    r = (1-(0.04*i))

    ######################################
    ######### Calculamos landa ###########
    ######################################

    landa_simple = (15*r)/int(S)
    landa_dual = (15*r)/(int(S)) # Cambiar por S*2 para encaminamientos 2, 3 y 4

    print("Lambda simple "+str(landa_simple))
    print("Lambda dual "+str(landa_dual))

    ######################################
    #### Generamos fichero config.cfg ####
    ######################################

    with open('basic_config.cfg', 'r') as fr, open ('config/config'+str(i)+'.cfg', 'w') as fw:

        simple_substitution = str(1/landa_simple)
        dual_substitution = str(1/landa_dual)

        for line in fr:
            # Replace all instances of "SIMPLE" with the constant substitution string
            modified_line = line.replace("TIEMPO_LLEGADAS_S", simple_substitution).replace("TIEMPO_LLEGADAS_D", dual_substitution)
            # Write the modified line to the output file
            fw.write(modified_line)
        
    ################################
    ######## Calculo de t ##########
    ################################

    #if iteracion == 0:
    t = 0.002
    #else:
    #    t = minimum(1 , ((1-PBlockAnt)/PBlockAnt)*0.002)

    #####################################
    ###### Ejecutamos el simulador ######
    #####################################

    process = Popen(["./SimRedMMkk","-s",str(seed),"-q",str(q),"-t",str(t),"-c","config/config"+str(i)+".cfg"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    os.rename("config/config"+str(i)+".cfg.out", "config_out/config"+str(i)+".cfg.out")

    ##################################################
    #### Guardamos los valores en el fichero plot ####
    ##################################################

    with open('config_out/config'+str(i)+'.cfg.out', 'r') as f:
        lines = f.readlines()

    data = {}
    current_block = 0

    for line in lines:
        line = line.strip()
        if line.startswith('Trafico/s promediado/s'):
            current_block = line.split(" ")[-1][0]
        if line.startswith('Probabilidad de bloqueo estimada:'):
            data[current_block] = {}
            data[current_block]['Probabilidad de bloqueo'] = float(line.split(":")[1])
        elif line.startswith('Confidence interval 1:'):
            print(re.findall('\((.*?)\)', line))
            data[current_block]['Confidence interval 1'] = tuple([float(num) for num in re.findall('\((.*?)\)', line)[0].split(",")])
        elif line.startswith('Confidence interval 2:'):
            data[current_block]['Confidence interval 2'] = tuple([float(num) for num in re.findall('\((.*?)\)', line)[0].split(",")])

    #print(data)

    with open('config_out/data'+str(i)+'.json', 'w') as f:
        json.dump(data, f, indent=4)


    A = float(landa_simple)*int(S)
    
    generate_plot(A, data)

    iteracion+=1

os.chdir('gnuplot')

process = Popen(["gnuplot","config.gnuplot"], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()   


