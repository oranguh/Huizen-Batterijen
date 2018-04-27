import csv

def solve(batteryDict, houseDict, bestPrice, subPrice = 0,houseNumber = 0):

    for i, battery in enumerate(batteryDict):
        # print(battery)
        # If kan connecten
        print(batteryDict)
        print("HouseNumber: {}".format(houseNumber))
        if houseDict[houseNumber]['output'] < battery['capacity']:
            diff_x = abs(houseDict[houseNumber]['position'][0] - battery['position'][0])
            diff_y = abs(houseDict[houseNumber]['position'][1] - battery['position'][1])
            nextSubPrice = subPrice + ((diff_x + diff_y) * 9)
            nextHouseNumber = houseNumber + 1
            battery['capacity'] -= houseDict[houseNumber]['output']
            houseDict[houseNumber]['connected_to'] = battery['position']
            # print(batteryDict)
            # Hier is dus de laatste geconnect
            if nextHouseNumber is len(houseDict):
                # Is dit de beste oplossing tot nu toe?
                if (nextSubPrice < bestPrice):
                    with open("best_brabo_solution.csv", "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(["score", "configuration"])
                        writer.writerow([nextSubPrice, {"DATA":houseDict}])
                    return nextSubPrice
                else:
                    return bestPrice


            elif nextSubPrice < bestPrice:
                # print("volgende solve")
                solve(batteryDict, houseDict, bestPrice, nextSubPrice, nextHouseNumber)
            # else:
            #     # print("Deze solve wordt gestopt met HouseNumber {}".format(nextHouseNumber))
            #     return bestPrice

        #if niet kan connecten
        elif battery['capacity'] < 20: #willen we dit 20?
            print("batteryfull")
            # Delete de batterij uit de node als er minder dan 20 capacity over is
            # print("3")
            # del batteryDict[i]
            continue
        else:
            print("123batteryfull")
            # print("4")
            continue
    # print("1")
    # print(batteryDict)
    # print("Einde for loop bereikt")
    return bestPrice
