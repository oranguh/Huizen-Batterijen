import json
from operator import itemgetter

def main():

    bat_comp_path = "../../Results/battery_compositions.json"
    with open(bat_comp_path, "r") as f:
        parsed_data = json.load(f)

    battery_comps = sorted(parsed_data["ALL_CONFIGURATIONS"], key=itemgetter('score'))[0:4]
    print(battery_comps)



if __name__ == "__main__":
    main()
