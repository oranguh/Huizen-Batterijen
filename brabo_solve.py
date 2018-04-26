import csv

class node:

    def __init__(self, batteryDict, houseDict, bestPrice, subPrice = 0,houseNumber = 0):
        self.houseNumber = houseNumber
        self.subPrice = subPrice
        self.batteries = batteryDict
        self.houses = houseDict
        self.bestPrice = bestPrice
        for i, battery in enumerate(self.batteries):
            float battiji = battery[caoacity]

        # battery dict = pos, capacity_left
        #house dict = pos, output, connected_to

    def solve(self):

        for i, battery in enumerate(self.batteries):
            # print(battery)
            # If kan connecten
            print(self.batteries)
            print("HouseNumber: {}".format(self.houseNumber))
            if self.houses[self.houseNumber]['output'] < battery['capacity']:
                diff_x = abs(self.houses[self.houseNumber]['position'][0] - battery['position'][0])
                diff_y = abs(self.houses[self.houseNumber]['position'][1] - battery['position'][1])
                nextSubPrice = self.subPrice + ((diff_x + diff_y) * 9)
                nextHouseNumber = self.houseNumber + 1
                battery['capacity'] -= self.houses[self.houseNumber]['output']
                self.houses[self.houseNumber]['connected_to'] = battery['position']
                # print(self.batteries)
                newNode = node(self.batteries, self.houses, self.bestPrice, nextSubPrice, nextHouseNumber)
                # Hier is dus de laatste geconnect
                if nextHouseNumber is len(self.houses):
                    # Is dit de beste oplossing tot nu toe?
                    if (nextSubPrice < self.bestPrice):
                        with open("Best_brabo_solution", "w") as f:
                            writer = csv.writer(f)
                            writer.writerow(["score", "configuration"])
                            writer.writerow([nextSubPrice, self.houses])
                        return nextSubPrice
                    else:
                        return self.bestPrice


                elif nextSubPrice < self.bestPrice:
                    # print("volgende solve")
                    self.bestPrice = newNode.solve()
                # else:
                #     # print("Deze solve wordt gestopt met HouseNumber {}".format(nextHouseNumber))
                #     return self.bestPrice

            #if niet kan connecten
            elif battery['capacity'] < 20: #willen we dit 20?
                print("batteryfull")
                # Delete de batterij uit de node als er minder dan 20 capacity over is
                # print("3")
                # del self.batteries[i]
                continue
            else:
                print("123batteryfull")
                # print("4")
                continue
        # print("1")
        # print(self.batteries)
        # print("Einde for loop bereikt")
        return self.bestPrice
