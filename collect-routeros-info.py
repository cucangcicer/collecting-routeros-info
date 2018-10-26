'''
    RIFKI HERMAWAN
    MikroTik Consultant
    PLONTOS,SWiN
    twitter @erdotha_
    facebook.com/cucangerz
'''
from librouteros import connect
import ssl
import time
import getpass

def deepKey(y,k,g):
    i=len(y)
    for x in range(0,i):
        z=y[x][k]
        g.append(z)

sr_login=raw_input('Input your username: ')
pasw_login=getpass.getpass('Password: ')
temp_ip=str(raw_input('Input IP Address: '))
ip_list=[]
ip_list.append(temp_ip)
u=raw_input('There is another IP[y/n]?: ')
while (u=='y'):
    temp_ip=str(raw_input('Input IP Address: '))
    ip_list.append(temp_ip)
    u=raw_input('There is another IP[y/n]?: ')

for x in ip_list:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.set_ciphers('ADH')
    api = connect(username=sr_login, password=pasw_login, host=x, ssl_wrapper=ctx.wrap_socket, port=8729)

    routerboard_info = api(cmd="/system/routerboard/print")
    resource_info = api(cmd="/system/resource/print")
    identity_info = api(cmd="/system/identity/print")
    interface_info=api(cmd='/interface/print')
    ip_address_info=api(cmd='/ip/address/print')

    identity = identity_info[0]['name']                         #Identity
    model=resource_info[0]['board-name']                        #Model
    uptime=resource_info[0]['uptime']                           #Uptime
    version=resource_info[0]['version']                         #Version
    serialNumber=routerboard_info[0]['serial-number']           #Serial Number
    currentFirmware=routerboard_info[0]['current-firmware']     #Firmware
    addresses_list=[]                                           #IP Address List
    deepKey(ip_address_info,'address',addresses_list)
    interface_list=[]                                           #IP Interface List
    deepKey(ip_address_info,'actual-interface',interface_list)

    print('For {}\nCollecting Data...'.format(x))
    print('------------------------------------')
    time.sleep(0.5)
    print('Name: {}'.format(identity))
    print('Model: {}'.format(model))
    print('Serial Number: {}'.format(serialNumber))
    print('Uptime: {}'.format(uptime))
    print('Firmware: {}'.format(currentFirmware))
    print('Version: {}'.format(version))
    try:
        badBlock=resource_info[0]['bad-blocks']                     #Bad Block
    except KeyError:
        badBlock='-'
    print('Bad Block: {}'.format(badBlock))
    print('\nIP Address List')
    for y in range(0,len(addresses_list)):
        temp_ip=addresses_list[y]
        temp_int=interface_list[y]
        print('{} on {}'.format(temp_ip,temp_int))
    
