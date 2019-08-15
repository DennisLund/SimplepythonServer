#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    try:
      if self.path.endswith('ip'):
        self.send_response(200)

        self.send_header('Content-type','text/html')
        self.end_headers()

        message = testHTTPServer_RequestHandler.misppull('ip-%')

        self.wfile.write(bytes(message, 'utf8'))

      elif self.path.endswith('domain'):
        self.send_response(200)

        self.send_header('Content-type','text/html')
        self.end_headers()

        message = testHTTPServer_RequestHandler.misppull('domain')

        self.wfile.write(bytes(message, 'utf8'))

      else:
        self.send_response(200)

        self.send_header('Content-type','text/html')
        self.end_headers()

        message = 'Hello World'

        self.wfile.write(bytes(message, 'utf8'))

    except IOError:
      self.send_error(404,'File not found: %s' % self.path)



  def misppull(dataType):
    headers={'Authorization':'<YOUR MISP API-KEY>','Accept':'application/json','Content-type':'application/json'}
    data=json.dumps({"returnFormat":"json","type":dataType,"tags":"Feed-%","to_ids":"yes","includeEventTags":"yes","includeContext":"yes"})
    response = requests.post('https://<YOUR MISP ADDRESS>/attributes/restSearch',headers=headers,data=data,verify=False)
    data=response.json()
    list=''
    for item in data['response']['Attribute']:
      list=list+(str(item['value'] + '\n'))
#    with open('/opt/scripts/debug.txt','w') as file:
#      file.write(list)
#      file.write('\n\n')
    return list


def run():
  print('starting server...')

  server_address=('0.0.0.0',8080)
  httpd=HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

run()

