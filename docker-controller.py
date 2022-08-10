import subprocess, yaml, json, logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPConnection
"""Микро-сервис, запущенный без docker. Используется для настройки и перезагрузки сервисов."""

hostName = "172.17.0.1"
serverPort = 9000

backend_url = "localhost:8000"

logger = logging.getLogger(__name__)

class AsLiteral(str):
  pass

def represent_literal(dumper, data):
  return dumper.represent_scalar(yaml.resolver.BaseResolver.DEFAULT_SCALAR_TAG,
      data, style="|")

def create_nlu_yml(intents_data):
    intents_dict = {'version': '3.1', 'nlu': []}
    yaml.add_representer(AsLiteral, represent_literal)
    for item in intents_data:
        if item['examples'] == '': continue
        examples = item['examples'].replace("'", '').replace("- ", '').split('\r\n')
        examples_str = AsLiteral(yaml.dump(examples, allow_unicode=True))
        intents_dict['nlu'].append({'intent': item['intent'], 'examples': examples_str})
    return intents_dict

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/rebuild_rasa':
            
            """Получаем intents из backend, генерируем новый nlu.yml, перезапускаем rasa"""
            
            connection = HTTPConnection(backend_url)
            connection.request("GET", "/intents/")
            response = connection.getresponse()
            intents_data = response.read().decode('utf8')
            intents_data = json.loads(intents_data)
            connection.close()
            
            intents_dict = create_nlu_yml(intents_data)
            with open('./rasa/data/nlu.yml', 'w') as yaml_file:
                yaml.dump(intents_dict, yaml_file, allow_unicode=True, default_flow_style=False, sort_keys=False)
                
            subprocess.Popen(['docker-compose', 'up', '--build', '--force-recreate', '--no-deps', '-d', 'rasa'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            self.send_response(code=200, message='Rasa rebuild started')
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'code': '200', 'text': 'Rasa rebuild started'}).encode('utf-8'))
        else:
            self.send_response(code=404, message="Path doesn't exist")
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'code': '200', 'text': "Path doesn't exist"}).encode('utf-8'))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Docker Controller started http://{hostName}:{serverPort}")
 
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
 
    webServer.server_close()
    print("Docker Controller stopped.")
    