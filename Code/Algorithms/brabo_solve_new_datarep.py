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
        # house list = [[cost to battery1, cost to battery2, ... , cost to battery n, connected to battery, output][...]]


    def solve(self):
        for i, battery in enumerate(self.batteries):

            # If output fits in battery
            if self.houses[self.houseNumber][-1] < battery['capacity']:

                # Update the house and the batteries
                nextSubPrice = self.subPrice + self.houses[self.houseNumber][i]
                nextHouseNumber = self.houseNumber + 1
                battery['capacity'] -= self.houses[self.houseNumber][-1]
                self.houses[self.houseNumber][-2] = i

                if nextHouseNumber is len(self.houses):

                    # Here the last one is connected so check if a better price is found
                    if (nextSubPrice < self.bestPrice):

                        # Write better solution
                        with open("../../Results/best_brabo_solution_1337.json", 'w') as jsonfile:
                            json.dump({"META": {"DATA": self.houses, "BATTERIES": self.batteries}}, jsonfile)
                        with open("../../Results/best_brabo_solution_1337.csv1", "w") as f:
                            writer = csv.writer(f)
                            writer.writerow(["score", "configuration"])
                            writer.writerow([nextSubPrice, {"DATA": self.houses}])
                        print("Er is een beter oplossing gevonden!!!")

                        self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1][-1]
                        battery['capacity'] += self.houses[self.houseNumber][-1]
                        return nextSubPrice
                    else:

                        # If there is not a better solution just continue searching
                        self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1][-1]
                        battery['capacity'] += self.houses[self.houseNumber][-1]
                        return self.bestPrice


                elif nextSubPrice < self.bestPrice:

                    # If the next subprice from the node is lower than the best price, create new node and continue path
                    newNode = node(self.batteries, self.houses, self.bestPrice, nextSubPrice, nextHouseNumber, i)
                    self.bestPrice = newNode.solve()

                else:

                    # Prune the rest of the path
                    self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1][-1]
                    battery['capacity'] += self.houses[self.houseNumber][-1]
                    return self.bestPrice

        # If battery could not be connected, return to previous node
        self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1][-1]
        return self.bestPrice
