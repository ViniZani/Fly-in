from typing import Any, Optional


class Parser:
    def __init__(self, archive) -> None:
        self.archive = archive

    def process_data(self, line: str) -> dict:
        _hub = {'name': None, 'x': None, 'y': None,
                'zone': 'normal', 'color': None,
                'max_drones': 1}
        try:
            has_meta = False
            if '[' in line:
                data = line.replace(']', '').split("[")
                main_part: Any = data[0]
                metadata_part = data[1]
                has_meta = True
            else:
                main_part = line
            main_part = main_part.split()
            if len(main_part) > 4:
                raise ValueError("Name of hubs cant have any space."
                                 " Verify if your data is:"
                                 " <name> <x> <y> [metadata]")
            _hub['name'] = main_part[1]
            if '-' in main_part[1]:
                raise ValueError("Names of hubs cant have any '-'")
            if not main_part[2].lstrip('-').isdigit():
                raise ValueError("Coordinates must be valid integers")
            _hub['x'] = int(main_part[2])
            _hub['y'] = int(main_part[3])
            if has_meta is True:
                for item in metadata_part.split(" "):
                    if "=" in item:
                        k, v = item.split("=")
                        if (k == "zone" and v not in ['normal', 'blocked',
                                                      'restricted',
                                                      'priority']):
                            raise ValueError("Zone must be one of the "
                                             "following types: 'normal',"
                                             "'blocked', 'restricted',"
                                             " 'priority'")
                        else:
                            _hub[k] = v
                        if k == "max_drones":
                            if not v.isdigit() or int(v) < 1:
                                raise ValueError("max_drones must be a "
                                                 "positive integer")
                            else:
                                _hub[k] = int(v)
                    else:
                        raise ValueError("Metadata must have the "
                                         "following sintax: type=value")
            return _hub
        except (ValueError, TypeError) as e:
            print("[ERROR DETECTED]:", e)
            exit(1)

    def get_data(self) -> tuple[int, Optional[dict[Any, Any]],
                                list[dict[str, Any]],
                                Optional[dict[Any, Any]],
                                list[dict[str, Any]]]:
        nb_drones = 0
        start_hub = None
        end_hub = None
        curr_hub = None
        list_hubs: list[dict[str, Any]] = []
        connection_model = {"a": None, "b": None, "max_link_capacity": 1}
        list_conects: list[dict[str, Any]] = []
        try:
            with open(self.archive, "r", encoding='utf-8') as archive:
                count_start = 0
                count_end = 0
                first_line = False
                for line in archive:
                    line = line.strip()
                    if line.startswith("#") or not line:
                        continue

                    if not first_line and not line.startswith("nb_drones"):
                        raise ValueError("The first non-comment line at "
                                         "the data file must be nb_drones:"
                                         " positive int num of drones")
                    elif line.startswith("nb_drones"):
                        data = line.split(':')
                        nb_drones = int(data[1].strip())
                        if first_line is True:
                            raise ValueError("At the data file, must be "
                                             "only 1 line with end_hub data")
                        if nb_drones < 1:
                            raise ValueError("The number of drones must"
                                             " be at least 1")
                        first_line = True

                    elif line.startswith("start_hub"):
                        start_hub = start_hub
                        count_start += 1
                        if count_start > 1:
                            raise ValueError("At the data file, must be "
                                             "only 1 line with start_hub data")
                        start_hub = self.process_data(line)

                    elif line.startswith("hub"):
                        curr_hub = self.process_data(line)
                        list_names = [h["name"] for h in list_hubs]
                        if curr_hub["name"] not in list_names:
                            list_hubs.append(curr_hub)
                        else:
                            raise ValueError("Each hubs must have "
                                             "unique names")

                    elif line.startswith("end_hub"):
                        end_hub = end_hub
                        count_end += 1
                        if count_end > 1:
                            raise ValueError("At the data file, must be "
                                             "only 1 line with end_hub data")
                        end_hub = self.process_data(line)

                    elif line.startswith("connection"):
                        connection = connection_model.copy()
                        has_meta = False
                        if '[' in line:
                            data = line.replace(']', '').split("[")
                            main_part: Any = data[0]
                            metadata_part = data[1]
                            has_meta = True
                        else:
                            main_part = line
                        main_part = main_part.split()
                        if len(main_part) > 4:
                            raise ValueError("Name of hubs cant have any space"
                                             " Verify if your data is:"
                                             " <name> <x> <y> [metadata]")
                        if '-' not in main_part[1]:
                            raise ValueError("Names of connection must be "
                                             "like 'a-b'")
                        vertex = main_part[1].split('-')
                        connection['a'] = vertex[0]
                        connection['b'] = vertex[1]
                        if has_meta is True:
                            for item in metadata_part.split():
                                if "=" in item:
                                    k, v = item.split("=")
                                    if k == "max_link_capacity":
                                        if not v.isdigit() or int(v) < 1:
                                            raise ValueError("max_link_capacity must"
                                                             " be a positive"
                                                             "integer")
                                        connection["max_link_capacity"] = int(v)
                                else:
                                    raise ValueError("Metadata must have the "
                                                     "following sintax: "
                                                     "type=value")
                        possible_names = [h["name"] for h in list_hubs]
                        if start_hub is not None:
                            possible_names.append(start_hub["name"])
                        if end_hub is not None:
                            possible_names.append(end_hub["name"])
                        if (connection['a'] in possible_names
                                and connection['b'] in possible_names):
                            for c in list_conects:
                                if (c['a'] == connection['a']
                                    and c['b'] == connection['b']) or \
                                   (c['a'] == connection['b']
                                        and c['b'] == connection['a']):
                                    raise ValueError("Duplicate connection"
                                                     "detected.")
                            list_conects.append(connection)
                        else:
                            raise ValueError("Connection with an "
                                                     "inexisted HUb.")

            return nb_drones, start_hub, list_hubs, end_hub, list_conects
        except Exception as e:
            print("[ERROR]", e)
            exit(1)
