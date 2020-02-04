from maq20 import MAQ20

system = MAQ20(ip_address="192.168.1.101", port=502)

#print (system.find("S0124418-04"))

print(system)


m = system.find("VO")
m= system.find("S0124418-04")
m = system.find("S0115278-06")


#m=system.find("S0120611-14")

#print (m)

#print(m.write_channel_data(1,True))


#print(m.write_channel_data(0,4.5))
#print(m.read_channel_data(0))


#m2 = system.find("S0115278-06")
#print(m2.read_channel_data(0))
