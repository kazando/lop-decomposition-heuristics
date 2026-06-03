set terminal pdfcairo enhanced color font "Helvetica,12"
set output "maxsize_dev.pdf"

set xlabel "MAXSIZE"
set ylabel "Average relative deviation (%)"
set key top right
set grid

plot "maxsize_summary.dat" using 1:3 with linespoints title "Level graph", \
     "maxsize_summary.dat" using 1:5 with linespoints title "Minimum cut", \
     "maxsize_summary.dat" using 1:7 with linespoints title "Recursive Borda"
