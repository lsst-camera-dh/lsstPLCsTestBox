import tester
import vac_tests
import time

vac_tester = tester.Tester()


#asdas

a= vac_tests.TestPlutoConnect(vac_tester, -1)
a.run()
a= vac_tests.TestTestBoxConnect(vac_tester, -1)
a.run()







while 1:
    start=time.time()

    a = vac_tests.TestCvTurboOnOfflogic(vac_tester, -1)
    a.run()

    print("YYYYYYEEEEEEEEESSSSSSSSSSSSSS!!!!!!!!!!!")
    print((time.time()-start)/60.0)

    break


vac_tester.plutoGateway.close()
vac_tester.testBox.close()