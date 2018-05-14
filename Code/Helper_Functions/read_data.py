import csv

def read_data(house_path, battery_path, intify = False):
    """
        Reads the data of batteries and houses and returns a list of dictionaries
        in the format:
        houses {'position': [x,y], 'output': <value>}
        batteries {'position': [x,y], 'capacity': <value>}
    """
    houses = []
    batteries = []

    with open(house_path) as housereader:
        houses_info = csv.reader(housereader)
        for i, row in enumerate(houses_info):
            # skips header
            if i is 0:
                continue
            # make a position list as [x,y]
            position = []
            position.append(int(row[0]))
            position.append(int(row[1]))
            # add dictionary item to houses
            if intify == False:
                houses.append({'position': position, 'output': float(row[2])})
            else:
                houses.append({'position': position, 'output': int(float(row[2])*1000)})
    with open(battery_path) as f:
        reader = csv.reader(f, csv.excel_tab)
        for i, row in enumerate(reader):
            # skips header
            if i is 0:
                continue
            # remove any empty elements
            row = list(filter(None, row))
            # the first element is a bit weird, so had to get it correct
            position = row[0].strip('[]').split(',')
            # int cast all elements
            position = [int(x) for x in position]
            # add dictionary item to batteries
            if intify == False:
                batteries.append({'position': position, 'capacity': float(row[1])})
            else:
                batteries.append({'position': position, 'capacity': int(float(row[1])*1000)})

    return houses, batteries
