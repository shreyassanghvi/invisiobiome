import httplib, urllib
from pyfirmata import Arduino, util
from sys import exit
import time


sleep =15
key = 'UVW2CAWC9JENAXKK'
board = Arduino('/dev/ttyACM4')
it = util.Iterator(board)
it.start()
analog_0 = board.get_pin('a:0:i')
D13=board.get_pin('d:13:o')
temp=analog_0.read()

def GsSensor():
        flg=0
        while flg is 0:
                temp=analog_0.read()
                if temp is None:
                        temp=0;
                else:
                        temp=analog_0.read()

                params = urllib.urlencode({'field1': temp, 'key':key })
                headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
                conn = httplib.HTTPConnection("api.thingspeak.com:80")
                try:
                        conn.request("POST", "/update", params, headers)
                        response = conn.getresponse()
                        print temp
                        print response.status, response.reason
                        data = response.read()
                        conn.close()
                except:
                        print "connection failed"
                        break
                if temp>0.1500:
                        flg=1
                        break
                time.sleep(sleep)

        if flg == 1:
                while True:
                        D13.write(1)
                        time.sleep(1)
                        D13.write(0)
                        time.sleep(1)


if __name__ == "__main__":
        while True:
                GsSensor()
