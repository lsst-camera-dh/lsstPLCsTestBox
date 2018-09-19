from os import path
import csv
import pyexcel_xlsx



def import_mappings(modbus_mapping_path ,testbox_mapping_path,sheet):

    testBox = dict()
    modbus = dict()


    testbox_mapping = pyexcel_xlsx.get_data(testbox_mapping_path)

    indexHeaders = dict()
    headers_row=testbox_mapping['Internal connections'][3]
    for i, h in enumerate(headers_row):
        indexHeaders[h] = i
        #print(headers)


    names = []
    for row in testbox_mapping['Internal connections']:
        try:
            names.append(row[indexHeaders['Logical Name']])
        except:
            names.append('')

    def getMaq20Add(name):

        n = names.index(name)

        while len(testbox_mapping['Internal connections'][n])<16:
            testbox_mapping['Internal connections'][n].append('')

        #print(name)
        #print(name,testbox_mapping['Internal connections'][n])

        maq20ModuleAddr = testbox_mapping['Internal connections'][n][indexHeaders['Address']]
        maq20ModuleSn =testbox_mapping['Internal connections'][n][indexHeaders['MAQ20 Module SN']]
        if maq20ModuleSn.find('S')!=0:
            maq20ModuleSn = 'S'+maq20ModuleSn
        maq20Module = testbox_mapping['Internal connections'][n][indexHeaders['MAQ20 Module Label']]


        return maq20ModuleAddr,maq20ModuleSn,maq20Module




    for row in testbox_mapping[sheet][9:]:

        while len(row)<30:
            row.append('')

        ports = row[7]

        ports = ports.split(';')

        for port in ports:

            if port != "" and port!='SHIELD' and port!='0V' and port.find('GND')!=0:
                try:
                    testBox[port]
                except KeyError:
                    testBox[port] = dict(plc=dict(), cam=dict())

                try:
                    if testBox[port]["device"] == "":
                        raise KeyError
                except KeyError:
                    testBox[port]["device"] = row[17]

                try:
                    if testBox[port]["modbus"] == '':
                        raise KeyError
                except KeyError:
                    testBox[port]["modbus"] = []

                side = 'plc'

                testBox[port][side]["testBoxPin"] = row[1]
                testBox[port][side]["testBoxName"] = row[2]
                testBox[port][side]["maq20ModuleAddr"], testBox[port][side]["maq20ModuleSn"], testBox[port][side]["maq20Module"] = getMaq20Add(testBox[port][side]["testBoxName"])

                testBox[port][side]["type"] = row[20]
                testBox[port][side]["default_value"] = row[21]
                testBox[port][side]["boot_value"] = row[22]

                side = 'cam'

                testBox[port][side]["testBoxPin"] = row[11]
                testBox[port][side]["testBoxName"] = row[12]
                testBox[port][side]["maq20ModuleAddr"], testBox[port][side]["maq20ModuleSn"],testBox[port][side]["maq20Module"] = getMaq20Add(testBox[port][side]["testBoxName"])

                testBox[port][side]["type"] = row[20]
                testBox[port][side]["default_value"] = ''
                testBox[port][side]["boot_value"] = ''


    with open(modbus_mapping_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        headers = dict()
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
                    #modbus[name]["boot_value"] = row[headers["boot_value"]]

                    if modbus[name]["related"] != "":
                        testBox[modbus[name]["related"]]["modbus"].append(name)


    return testBox,modbus


testBox,modbus = import_mappings(path.join(path.dirname(path.realpath(__file__)), "mapping", "mpm_modbus_mapping.csv"),path.join(path.dirname(path.realpath(__file__)), "mapping", "PLC_Certification_Chassis.xlsx"),'MPM Cables')