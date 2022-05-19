set terminal png size 1920,1080

# Poner etiqueta en eje de abscisas:
set xlabel 'A'
# Ídem ordenadas
set ylabel 'Ac'

# Fijar posición de la leyenda de funciones
set key bottom right

set title 'Encaminamiento 1'

# Cambia rango de representación de eje de abscisas:
#set xrange [35:55]
#set yrange [35:46]

set output './Encaminamiento_I.png'
plot 'trafico_simple.plot' with yerrorlines lw 2 title 'Tráfico de un salto', 'trafico_doble.plot' with yerrorlines lw 2 title 'Tráfico de dos saltos'

pause 1

set output './Encaminamiento_I_Total.png'
plot 'trafico_total.plot' with yerrorlines lw 2 title 'Tráfico total'

# Pausa hasta retorno de carro (-1), o el  tiempo especificado:
pause -1
