from os import path
import csv
import pyexcel_xlsx



def import_mappings(modbus_mapping_path ,testbox_mapping_path,sheet):

    testBox = dict()
    modbus = dict()
    headers = dict()

    testbox_mapping = pyexcel_xlsx.get_data(testbox_mapping_path)



    headers_row=testbox_mapping[sheet][7]
    for i, h in enumerate(headers_row):
        headers[h] = i

    names = []
    for row in testbox_mapping['Internal connections']:
        try:
            names.append(row[12])
        except:
            names.append('')

    def getMaq20Add(name):

        n = names.index(name)

        while len(testbox_mapping['Internal connections'][n])<15:
            testbox_mapping['Internal connections'][n].append('')

        #print(name,testbox_mapping['Internal connections'][n])

        maq20ModuleAddr = testbox_mapping['Internal connections'][n][13]
        maq20ModuleSn =testbox_mapping['Internal connections'][n][7]
        maq20Module = testbox_mapping['Internal connections'][n][8]

        return maq20ModuleAddr,maq20ModuleSn,maq20Module


    for row in testbox_mapping[sheet][9:]:

        while len(row)<30:
            row.append('')

        port = row[headers["Plc Port"]]



        if port != "" and port!='SHIELD' and port!='0V' and port.find('GND')!=0:
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
                if testBox[port]["modbus"] == '':
                    raise KeyError
            except KeyError:
                testBox[port]["modbus"] = []

            side = 'plc'

            testBox[port][side]["testBoxPin"] = row[1]
            testBox[port][side]["testBoxName"] = row[2]
            print(port)
            testBox[port][side]["maq20ModuleAddr"], testBox[port][side]["maq20ModuleSn"], testBox[port][side]["maq20Module"] = getMaq20Add(testBox[port][side]["testBoxName"])

            testBox[port][side]["type"] = row[headers["Type"]]
            testBox[port][side]["default_value"] = row[headers["PlcDefaultValue"]]
            testBox[port][side]["boot_value"] = row[headers["PlcBootValue"]]

            side = 'cam'

            testBox[port][side]["testBoxPin"] = row[11]
            testBox[port][side]["testBoxName"] = row[12]
            testBox[port][side]["maq20ModuleAddr"], testBox[port][side]["maq20ModuleSn"],testBox[port][side]["maq20Module"] = getMaq20Add(testBox[port][side]["testBoxName"])

            testBox[port][side]["type"] = row[headers["Type"]]
            testBox[port][side]["default_value"] = row[headers["PlcDefaultValue"]]
            testBox[port][side]["boot_value"] = row[headers["PlcBootValue"]]




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


#testBox,modbus = import_mappings(path.join(path.dirname(path.realpath(__file__)), "mapping", "vac_modbus_mapping.csv"),'V:\KIPAC\LSST\Camera\Protection\PLCs Test Box\PLC_Certification_Chassis.xlsx','Vaccum cables')