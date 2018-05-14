import csv
import json
class node:

    def __init__(self, batteryDict, houseDict, bestPrice, subPrice = 0,houseNumber = 0, previousBattery = None):
        self.houseNumber = houseNumber
        self.subPrice = subPrice
        self.batteries = batteryDict
        self.houses = houseDict
        self.bestPrice = bestPrice
        self.previousBattery = previousBattery

        # battery dict = pos, capacity_left
        #house dict = pos, output, connected_to

    def solve(self):
        for i, battery in enumerate(self.batteries):
            # If kan connecten
            if self.houses[self.houseNumber]['output'] < battery['capacity']:
                diff_x = abs(self.houses[self.houseNumber]['position'][0] - battery['position'][0])
                diff_y = abs(self.houses[self.houseNumber]['position'][1] - battery['position'][1])
                nextSubPrice = self.subPrice + ((diff_x + diff_y) * 9)
                nextHouseNumber = self.houseNumber + 1

                battery['capacity'] -= self.houses[self.houseNumber]['output']
                self.houses[self.houseNumber]['connected_to'] = battery['position']

                # Hier is dus de laatste geconnect
                if nextHouseNumber is len(self.houses):
                    # Is dit de beste oplossing tot nu toe?
                    if (nextSubPrice < self.bestPrice):
                        with open("../../Results/best_brabo_solution.csv1", "w") as f:
                            writer = csv.writer(f)
                            writer.writerow(["score", "configuration"])
                            writer.writerow([nextSubPrice, {"DATA": self.houses}])
                        print("Er is een beter oplossing gevonden!!!")

                        self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1]['output']
                        battery['capacity'] += self.houses[self.houseNumber]['output']
                        return nextSubPrice
                    else:
                        # print("111")
                        self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1]['output']
                        battery['capacity'] += self.houses[self.houseNumber]['output']
                        return self.bestPrice


                elif nextSubPrice < self.bestPrice:

                    newNode = node(self.batteries, self.houses, self.bestPrice, nextSubPrice, nextHouseNumber, i)
                    self.bestPrice = newNode.solve()

                else:

                    self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1]['output']
                    battery['capacity'] += self.houses[self.houseNumber]['output']
                    return self.bestPrice

            #if niet kan connecten

        self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1]['output']
        return self.bestPrice
