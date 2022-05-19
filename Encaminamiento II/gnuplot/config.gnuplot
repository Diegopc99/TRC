set terminal png size 1920,1080
#!/usr/bin/gnuplot
# Documentación sobre sus comandos en uso interactivo, con comando help

# Poner escala logarítmica y en qué base en eje de abscisas:
#set logscale x 10
# Poner etiqueta en eje de abscisas:
set xlabel 'A'
# Ídem ordenadas
set ylabel 'Ac'

# Fijar posición de la leyenda de funciones
set key bottom right

# Cambio a salida postscript:
#set term postscript color

set title 'Encaminamiento 2'

# Cambia rango de representación de eje de abscisas:
#set xrange [35:55]
#set yrange [35:46]

# Salida hacia fichero (tras activar modo postscript):
#set output 'imagen.ps'

# Gráfica  con líneas
#plot 1.0000000000 title 'valor teorico', 'sim1.plot' title 'función' with lines
#Otra forma: plot 2.555555555555555 'prueba.plot' with lines

#pause -1

# Pausa de 5 segundos hasta siguiente gráfica
#pause 5

# Salida hacia fichero (tras activar modo postscript): 
set output 'Encaminamiento_II.png'
# Gráficas con líneas y barras de error (intervalos de confianza)
#plot 2.555555555555555 title 'valor teorico', 'resultado.plot' title 'estimación' with errorbars, 'resultado.plot' notitle with lines
#Otra forma : 
plot 'sim.plot' with errorbars, 'sim.plot' notitle with lines

pause -1
quit
# Pausa de 5 segundos hasta siguiente gráfica
pause 5

# Gráficas con doble eje de ordenadas
#
# De ser necesario cambiar el rango representado del segundo eje de ordenadas:
#set y2range
# Anular las marcas reflejo en el segundo eje de ordenadas
#set ytics nomirror
# y activar las marcas independientes
#set y2tics
# Etiqueta del segundo eje de ordenadas 
#set y2label 'F'
#set key right center
# Salida hacia fichero (tras activar modo postscript):
#set output 'imagen3.ps'
#plot 2.555555555555555 title 'valor teorico a', 'prueba.plot' title 'estimación a' with errorbars, 'prueba.plot' notitle with lines, 5 #axes x1y2 title 'valor teorico b', 'prueba-b.plot' axes x1y2 title 'estimación b' with errorbars, 'prueba-b.plot' axes x1y2 notitle with #lines

# Pausa hasta retorno de carro (-1), o el  tiempo especificado:
pause -1
