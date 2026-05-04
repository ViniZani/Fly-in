from parser_config import Parser
import sys


if __name__ == "__main__":
    # try:
    if len(sys.argv) == 2:
        parser = Parser(sys.argv[1])
        (nb_drones, start_hub, list_hubs,
         end_hub, list_conects) = parser.get_data()
        print("nb_hubs:", nb_drones)
        # print("start_hub:", start_hub)
        # print("lista de hubs:", list_hubs)
        # print("end_hub:", end_hub)
        print("conexions:", list_conects)
    # except Exception:
        print("Must have contain one txt")
