set terminal png size 1920,1080
# Poner etiqueta en eje de abscisas:
set xlabel 'A'
# Ídem ordenadas
set ylabel 'Ac'
# Fijar posición de la leyenda de funciones
set key bottom right
set title 'Encaminamiento 1'
set key left top
set output './traficos_simples.png'
plot 'trafico_a.plot' with yerrorlines linecolor rgb '#001DBC' lw 2 title 'Tráfico A', 'trafico_b.plot' with yerrorlines linecolor rgb '#B85450' lw 2 title 'Tráfico B',                         'trafico_c.plot' with yerrorlines linecolor rgb '#B09500' lw 2 title 'Tráfico C', 'trafico_d.plot' with yerrorlines linecolor rgb '#3A5431' lw 2 title 'Tráfico D' 
pause 1
set output './traficos_dobles.png'
set key left top
plot 'trafico_e.plot' with yerrorlines linecolor rgb '#432D57' lw 2 title 'Tráfico E', 'trafico_f.plot' with yerrorlines linecolor rgb '#C73500' lw 2 title 'Tráfico F',                         'trafico_g.plot' with yerrorlines linecolor rgb '#314354' lw 2 title 'Tráfico G', 'trafico_h.plot' with yerrorlines linecolor rgb '#10739E' lw 2 title 'Tráfico H', 'trafico_i.plot'                          with yerrorlines linecolor rgb '#B46504' lw 2 title 'Tráfico I', 'trafico_j.plot' with yerrorlines linecolor rgb '#82B366' lw 2 title 'Tráfico J' 
pause 1
