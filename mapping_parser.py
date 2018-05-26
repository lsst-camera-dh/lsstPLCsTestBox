from os import path
import csv



def import_mappings(modbus_mapping_path ,testbox_mapping_path):

    testBox = dict()
    modbus = dict()
    headers = dict()

    with open(testbox_mapping_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            if first:
                for i,h in enumerate(row):
                    headers[h]=i
                first = False
            else:

                port = row[headers["PlcPort"]]

                if port != "":
                    try:
                        values = testBox[port]
                    except KeyError:
                        testBox[port] = dict(plc=dict(), cam=dict())

                    try:
                        if testBox[port]["device"] == "":
                            raise KeyError
                    except KeyError:
                        testBox[port]["device"] = row[headers["Device"]]

                    try:
                        if testBox[port]["connector"] == "":
                            raise KeyError
                    except KeyError:
                        testBox[port]["connector"] = row[headers["Connector"]]

                    try:
                        if testBox[port]["pin"] == "":
                            raise KeyError
                    except KeyError:
                        testBox[port]["pin"] = row[headers["ConnectorPin"]]

                    try:
                        if testBox[port]["modbus"] == "":
                            raise KeyError
                    except KeyError:
                        testBox[port]["modbus"] =[]

                    side = row[headers["TestBoxSide"]]

                    testBox[port][side]["testBoxPin"] = row[headers["TestBoxPin"]]
                    testBox[port][side]["testBoxName"] = row[headers["TestBoxName"]]
                    testBox[port][side]["maq20ModuleAddr"] = int(row[headers["Maq20ModuleAddr"]])
                    testBox[port][side]["maq20ModuleSn"] = row[headers["Maq20ModuleSn"]]
                    testBox[port][side]["maq20Module"] = row[headers["Maq20Module"]]
                    testBox[port][side]["type"] = row[headers["Type"]]
                    testBox[port][side]["default_value"] = row[headers["DefaultValue"]]
                    testBox[port][side]["boot_value"] = row[headers["BootValue"]]



    with open(modbus_mapping_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            if first:
                for i, h in enumerate(row):
                    headers[h] = i
                first = False
            else:
                name = row[headers["name"]]

                if name != "":
                    modbus[name] = dict()

                    def intt(str):
                        try:
                            return int(str)
                        except Exception:
                            return None

                    modbus[name]["mb_type"] = row[headers["mb_type"]]
                    modbus[name]["unit_id"] = intt(row[headers["unit_id"]])
                    modbus[name]["permissions"] = row[headers["permissions"]]
                    modbus[name]["addr"] = intt(row[headers["addr"]])
                    modbus[name]["bit"] = intt(row[headers["bit"]])
                    modbus[name]["related"] = row[headers["related"]]
                    modbus[name]["default_value"] = row[headers["default_value"]]
                    modbus[name]["type"] = row[headers["type"]]
                    modbus[name]["boot_value"] = row[headers["boot_value"]]

                    if modbus[name]["related"] != "":
                        testBox[modbus[name]["related"]]["modbus"].append(name)


    return testBox,modbus


#testBox, modbus =import_mappings()