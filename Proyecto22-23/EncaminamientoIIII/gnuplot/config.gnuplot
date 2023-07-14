set terminal png size 1920,1080
# Poner etiqueta en eje de abscisas:
set xlabel 'A'
# Ídem ordenadas
set ylabel 'Ac'
# Fijar posición de la leyenda de funciones
set key bottom right
set title 'Encaminamiento 3'
set key left top
set output './traficos_simples.png'
plot 'trafico_a.plot' with yerrorlines linecolor rgb 'blue' lw 2 title 'Tráfico A', 'trafico_b.plot' with yerrorlines linecolor rgb 'red' lw 2 title 'Tráfico B' 
 pause 1
set output './traficos_dobles.png'
set key left top
plot 'trafico_c.plot' with yerrorlines linecolor rgb 'yellow' lw 2 title 'Tráfico C', 'trafico_d.plot' with yerrorlines linecolor rgb 'green' lw 2 title 'Tráfico D',                         'trafico_e.plot' with yerrorlines linecolor rgb 'purple' lw 2 title 'Tráfico E', 'trafico_f.plot' with yerrorlines linecolor rgb 'violet' lw 2 title 'Tráfico F' 
pause 1
