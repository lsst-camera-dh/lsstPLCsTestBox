
from os import path

import tester
import mpm_tests
import cold_tests
from mapping_parser import import_mappings
import logging
import time


plutoGateway_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "cold_modbus_mapping.csv")
testbox_mapping_path = path.join(path.dirname(path.realpath(__file__)), "mapping", "PLC_Certification_Chassis.xlsx")

testBox, plutoGateway = import_mappings(plutoGateway_mapping_path, testbox_mapping_path, 'ColdCryo Cables')


mpm_tester = tester.Tester(testBox, plutoGateway)
mpm_tester.connectTestBox()
mpm_tester.connectGateway(timeout=30)


#asdas

#a= mpm_tests.TestPlutoConnect(mpm_tester, -1)
#a.run()
#a= mpm_tests.TestTestBoxConnect(mpm_tester, -1)
#a.run()



a = cold_tests.TestDigitalInputs(mpm_tester, 1)
a.button_run()


'''
while 1:
    start=time.time()

    #mpm_tester.tests.append(mpm_tests.TestPlutoGatewayConfig(mpm_tester, 1))
    a = cold_tests.TestDigitalInputs(mpm_tester, -1)
    a.button_run()

    print("YYYYYYEEEEEEEEESSSSSSSSSSSSSS!!!!!!!!!!!")
    print((time.time()-start)/60.0)

    break

'''
mpm_tester.plutoGateway.close()
mpm_tester.testBox.close()