# urllib3 used for retrieving webserver token and switching device mode
import urllib3
import re 
import xmltodict
import xml.etree.ElementTree as ET


if __name__ == "__main__":
    # assign http as a urllib3 pool manager
#def getToken():
    http = urllib3.PoolManager()
    baseurl = 'http://192.168.8.1'
    addurl = '/api/webserver/token/SesTokInfo'
    print("retrieving token at <" + baseurl+addurl +">")
    response = http.request("GET",baseurl+addurl,preload_content=False)
    xml=response.read()
    token=xml[59:-23]
    print("The token is: " % token)

    # get inputs for script (router url and mode) with some error checking
    while True:
        try:
            mode=int(input('Choose mode: \n1 - Debug \n2 - HiLink \n3 - Stick Modem\n'))
        except ValueError:
            print('\nERROR!\nPlease choose from 1-3\n')
            continue
        else:
            break
    
    # switch device mode
    payload='<request><mode>' + str(mode) + '</mode></request>'
    url='http://192.168.8.1/api/device/mode'
    send = http.request('POST',
                        baseurl+addurl,
                        body = payload,
                        headers = { 'Content-type': 'text/xml',
                        '__RequestVerificationToken': token })
    answer = str(send.data.decode('utf-8'))
    data = ET.fromstring(answer)
    code = '\>(.*?)\<'
    print('\nModem sent back: \n' + answer)
