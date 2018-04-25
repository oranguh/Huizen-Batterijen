    """
    1) Maak ‘route-klasse’ maar geen stack
    2) vulVolgendePlaatsIn(Route p)
    3) Maak alle kinderen k1 ... k13 (of minder)
    4) Voor alle kx: controleer if laatste plaats.
    4a) Ja? Stop en bereken lengte. (beter? bewaren!)
    4b) Nee? vulVolgendePlaatsIn(p)
    5) Klaar? Bewaarde route = best
    """

class node:

    def __init__(self, houseNumber = 0, batterydict, houseDict, subPrice = 0, bestPrice):
        self.houseNumber = houseNumber
        self.lastNode = False
        self.subPrice = price
        self.batteries = batteryDict
        self.houses = houseDict
        self.bestPrice = bestPrice
        # battery dict = pos, capacity_left
        #house dict = pos, output, connected_to

    def solve(self, bestPrice):
        for i, battery in enumerate(self.batteries):
            if self.houses[houseNumber]['output'] < battery['capacity_left']
                diff_x = abs(self.houses[houseNumber]['position'][0] - battery['position'][0])
                diff_y = abs(self.houses[houseNumber]['position'][1] - battery['position'][1])
                nextSubPrice += ((diff_x + diff_y) * 9)
                nextHouseNumber = self.houseNumber + 1
                battery['capacity_left'] -= houses[houseNumber]['output']
                self.houses[houseNumber]['connected_to'] = battery['position']
                newNode = node(nextHouseNumber, self.batteries, self.houses, nextSubPrice)
                # Hier is dus de laatste geconnect
                if nextHouseNumber is len(self.houses
                    # Is dit de beste oplossing tot nu toe?
                    if nextSubPrice < bestPrice:
                    with open("Best_brabo_solution", "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(["score", "configuration"])
                        writer.writerow([nextSubPrice, houses])
                        return nextSubPrice

                elif nextSubPrice < bestPrice:
                    self.bestPrice = newnode.solve()
                else:
                    return self.bestPrice
            elif battery['capacity_left'] < 20: #willen we dit 20?
                # Delete de batterij uit de node als er minder dan 20 capacity over is
                del self.batteries[i]
            else:
                continue
        return self.bestPrice
