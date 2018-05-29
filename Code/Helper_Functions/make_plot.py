import csv
import matplotlib.pyplot as plt
import matplotlib.lines as lines

first_distr = []
second_distr = []
third_distr = []

with open('../../Results/Old_results/random_solutions10000.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        for i, item in enumerate(row):
            first_distr.append(int(item))
        break

with open('../../Results/Old_results/random_solutions.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        for i, item in enumerate(row):
            second_distr.append(int(item))
        break

with open('../../Results/random_solutions_final.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        for i, item in enumerate(row):
            third_distr.append(int(item))
        break

title_string = 'Score simulated annealing t.o.v. bounds'
 # + '\n' + 'Ongeldige oplossingen: 985077'
# title_string = 'Vergelijking resultaten'
# plt.hist(first_distr, 50, facecolor='blue')
# plt.hist(second_distr, 50, facecolor='red')
plt.hist(third_distr, 50, facecolor='green')
# plt.plot([53000, 53000], [0, 750], 'b--', lw=1)
# plt.plot([40000, 40000], [0, 750], 'r--', lw=1)
plt.plot([22770, 22770], [0, 750], 'g--', lw=1)
# plt.plot([23750, 23750], [0, 750], 'g-', lw=1)
plt.rcParams.update({'font.size': 16})
plt.xlabel('Grid Score')
plt.ylabel('Count')
plt.title(title_string)
plt.xlim(xmin = 20000)
plt.ylim(ymax = 700)
plt.show()
