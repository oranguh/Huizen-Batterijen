import csv
import json
class node:

    def __init__(self, batteryDict, houseList, bestPrice, subPrice = 0,houseNumber = 0, previousBattery = None):
        self.houseNumber = houseNumber
        self.subPrice = subPrice
        self.batteries = batteryDict
        self.houses = houseList
        self.bestPrice = bestPrice
        self.previousBattery = previousBattery

        # battery dict = pos, capacity_left
        #house list = [[cost to battery1, cost to battery2, ... , cost to battery n, connected to battery, output][...]]


    def solve(self):
        for i, battery in enumerate(self.batteries):
            # If kan connecten
            if self.houses[self.houseNumber][-1] < battery['capacity']:
                nextSubPrice = self.subPrice + self.houses[self.houseNumber][i]
                nextHouseNumber = self.houseNumber + 1

                battery['capacity'] -= self.houses[self.houseNumber][-1]
                self.houses[self.houseNumber][-2] = battery[i]

                # Hier is dus de laatste geconnect
                if nextHouseNumber is len(self.houses):
                    # Is dit de beste oplossing tot nu toe?
                    if (nextSubPrice < self.bestPrice):
                        with open("best_brabo_solution.csv1", "w") as f:
                            writer = csv.writer(f)
                            writer.writerow(["score", "configuration"])
                            writer.writerow([nextSubPrice, {"DATA": self.houses}])
                        print("Er is een beter oplossing gevonden!!!")

                        self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1][-1]
                        battery['capacity'] += self.houses[self.houseNumber]['output']
                        return nextSubPrice
                    else:
                        # print("111")
                        self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1][-1]
                        battery['capacity'] += self.houses[self.houseNumber][-1]
                        return self.bestPrice


                elif nextSubPrice < self.bestPrice:

                    newNode = node(self.batteries, self.houses, self.bestPrice, nextSubPrice, nextHouseNumber, i)
                    self.bestPrice = newNode.solve()

                else:

                    self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1][-1]
                    battery['capacity'] += self.houses[self.houseNumber][-1]
                    return self.bestPrice

            #if niet kan connecten

        self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1][-1]
        return self.bestPrice
