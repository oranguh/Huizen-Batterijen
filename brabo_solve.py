class node:

    def __init__(self, batteryDict, houseDict, bestPrice, subPrice = 0,houseNumber = 0):
        self.houseNumber = houseNumber
        self.subPrice = subPrice
        self.batteries = batteryDict
        self.houses = houseDict
        self.bestPrice = bestPrice
        # battery dict = pos, capacity_left
        #house dict = pos, output, connected_to

    def solve(self):

        for i, battery in enumerate(self.batteries):
            print("1")

            # If kan connecten
            if self.houses[self.houseNumber]['output'] < battery['capacity']:
                print("2")
                diff_x = abs(self.houses[self.houseNumber]['position'][0] - battery['position'][0])
                diff_y = abs(self.houses[self.houseNumber]['position'][1] - battery['position'][1])
                print(diff_x)
                print(diff_y)
                nextSubPrice = self.subPrice + ((diff_x + diff_y) * 9)
                print(nextSubPrice)
                nextHouseNumber = self.houseNumber + 1
                battery['capacity'] -= self.houses[self.houseNumber]['output']
                self.houses[self.houseNumber]['connected_to'] = battery['position']

                newNode = node(self.batteries, self.houses, nextSubPrice, nextHouseNumber)
                # Hier is dus de laatste geconnect
                if nextHouseNumber is len(self.houses):
                    # Is dit de beste oplossing tot nu toe?
                    if (nextSubPrice < self.bestPrice):
                        with open("Best_brabo_solution", "w") as f:
                            writer = csv.writer(f)
                            writer.writerow(["score", "configuration"])
                            writer.writerow([nextSubPrice, houses])
                        return nextSubPrice
                    else:
                        return self.bestPrice


                elif nextSubPrice < self.bestPrice:
                    print("HALLO")
                    self.bestPrice = newNode.solve()
                elif nextSubPrice > self.bestPrice:
                    print("DOEI")
                else:
                    return self.bestPrice
                print("5")
            #if niet kan connecten
            elif battery['capacity'] < 20: #willen we dit 20?
                # Delete de batterij uit de node als er minder dan 20 capacity over is
                print("3")
                del self.batteries[i]
            else:
                print("4")
                continue
        return self.bestPrice
