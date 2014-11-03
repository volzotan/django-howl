set terminal png size 600,370
set output "/tmp/graphs.png"

set datafile separator " "

set size 1,1
set origin 0,0

set tmargin 0.5
set bmargin 0.5
# set lmargin 3
# set rmargin 3

set terminal png linewidth 2
set ytics font "Fira Mono Bold, 12"

set xtics format " "
set xtics 3600

set multiplot layout 3,1 columnsfirst scale 1,1

set yrange [0:80]
set ytics 10,20
plot "/tmp/plotdata.csv" using 1:2 with lines title "luminosity" lt rgb "black" 
set ytics 18,4
set yrange [16:28]
plot "/tmp/plotdata.csv" using 1:3 with lines title "temperature" lt rgb "black" 
set ytics 30,10
set yrange [25:65]
plot "/tmp/plotdata.csv" using 1:4 with lines title "humidity" lt rgb "black" 

unset multiplot
