import csv
import matplotlib.pyplot as plt
import matplotlib.lines as lines

first_distr = []
second_distr = []

with open('../../Results/random_solutions10000.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        for i, item in enumerate(row):
            first_distr.append(int(item))
        break

with open('../../Results/random_solutions.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        for i, item in enumerate(row):
            second_distr.append(int(item))
        break

title_string = 'Random solve distributie n = 10000' + '\n' + 'Ongeldige oplossingen: 985077'
# title_string = 'Vergelijking resultaten'
plt.hist(first_distr, 50, facecolor='blue')
plt.hist(second_distr, 50, facecolor='red')
plt.plot([53000, 53000], [0, 750], 'b-', lw=1)
plt.plot([40000, 40000], [0, 750], 'r-', lw=1)
lines.line2D()
# plt.plot([64492, 64492], [0, 400], 'k:', lw=2)
# plt.plot([41596, 41596], [0, 400], 'k-.', lw=2)
# plt.plot([41371, 41371], [0, 400], 'r:', lw=1)
# plt.plot([40000, 40000], [0, 400], 'r-', lw=1)
plt.xlabel('Grid Score')
plt.ylabel('Count')
plt.title(title_string)
plt.xlim(xmin = 38000)
plt.ylim(ymax = 700)
plt.show()
