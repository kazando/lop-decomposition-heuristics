set terminal pdfcairo enhanced color font "Helvetica,12"
set output "maxsize_time.pdf"

set xlabel "MAXSIZE"
set ylabel "Average computation time (s)"
set logscale y
set key top left
set grid

plot "maxsize_summary.dat" using 1:2 with linespoints title "Level graph", \
     "maxsize_summary.dat" using 1:4 with linespoints title "Minimum cut", \
     "maxsize_summary.dat" using 1:6 with linespoints title "Recursive Borda"
