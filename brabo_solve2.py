import csv

def solve(batteryDict, houseDict, bestPrice, subPrice = 0,houseNumber = 0, previousBattery = None):
    for i, battery in enumerate(batteryDict):
        # If kan connecten
        if houseDict[houseNumber]['output'] < battery['capacity']:
            diff_x = abs(houseDict[houseNumber]['position'][0] - battery['position'][0])
            diff_y = abs(houseDict[houseNumber]['position'][1] - battery['position'][1])
            nextSubPrice = subPrice + ((diff_x + diff_y) * 9)
            nextHouseNumber = houseNumber + 1
            battery['capacity'] -= houseDict[houseNumber]['output']
            houseDict[houseNumber]['connected_to'] = battery['position']
            # Hier is dus de laatste geconnect
            if nextHouseNumber is len(houseDict):
                # Is dit de beste oplossing tot nu toe?
                if (nextSubPrice < bestPrice):
                    with open("best_brabo_solution.csv", "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(["score", "configuration"])
                        writer.writerow([nextSubPrice, {"DATA":houseDict}])
                        print("Betere oplossing gevonden!")
                    batteryDict[previousBattery]['capacity'] += houseDict[houseNumber - 1]['output']
                    battery['capacity'] += houseDict[houseNumber]['output']
                    return nextSubPrice
                else:
                    batteryDict[previousBattery]['capacity'] += houseDict[houseNumber - 1]['output']
                    battery['capacity'] += houseDict[houseNumber]['output']
                    return bestPrice
            elif nextSubPrice < bestPrice:
                bestPrice = solve(batteryDict, houseDict, bestPrice, nextSubPrice, nextHouseNumber, i)
            else:
                batteryDict[previousBattery]['capacity'] += houseDict[houseNumber - 1]['output']
                battery['capacity'] += houseDict[houseNumber]['output']
                return bestPrice
        #if niet kan connecten
        # elif battery['capacity'] < 20: #willen we dit 20?
        #     continue
        else:
            continue
    batteryDict[previousBattery]['capacity'] += houseDict[houseNumber - 1]['output']
    return bestPrice
