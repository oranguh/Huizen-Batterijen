import csv
import sys
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
            # print(battery)
            # If kan connecten
            # print(self.subPrice)
            # print(self.batteries)
            # print("HouseNumber: {}".format(self.houseNumber))
            if self.houses[self.houseNumber]['output'] < battery['capacity']:
                diff_x = abs(self.houses[self.houseNumber]['position'][0] - battery['position'][0])
                diff_y = abs(self.houses[self.houseNumber]['position'][1] - battery['position'][1])
                # print(type(diff_y))
                nextSubPrice = self.subPrice + ((diff_x + diff_y) * 9)
                nextHouseNumber = self.houseNumber + 1
                # print(type(nextSubPrice))
                # print(type(nextHouseNumber))
                battery['capacity'] -= self.houses[self.houseNumber]['output']
                # print(type(battery['capacity']))
                self.houses[self.houseNumber]['connected_to'] = battery['position']
                # print(self.batteries)
                newNode = node(self.batteries, self.houses, self.bestPrice, nextSubPrice, nextHouseNumber, i)
                # Hier is dus de laatste geconnect
                if nextHouseNumber is len(self.houses):
                    # Is dit de beste oplossing tot nu toe?
                    if (nextSubPrice < self.bestPrice):
                        with open("best_brabo_solution.csv", "w") as f:
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
                    # print("2")
                    self.bestPrice = newNode.solve()

                else:
                    # print ("3!")
                # print("Deze solve wordt gestopt met HouseNumber {}".format(nextHouseNumber
                    # print("waarom kom ik hier")
                    self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1]['output']
                    battery['capacity'] += self.houses[self.houseNumber]['output']
                    return self.bestPrice

            #if niet kan connecten
            elif battery['capacity'] < 20: #willen we dit 20?
                # print("batteryfull")
                # Delete de batterij uit de node als er minder dan 20 capacity over is
                # print("3")
                # del self.batteries[i]
                continue
            else:
                # print("123batteryfull")
                # print("4")
                continue
        # print("1")
        # print(self.batteries)
        # print("Einde for loop bereikt")
        self.batteries[self.previousBattery]['capacity'] += self.houses[self.houseNumber - 1]['output']
        # battery['capacity'] += self.houses[self.houseNumber]['output']
        return self.bestPrice
