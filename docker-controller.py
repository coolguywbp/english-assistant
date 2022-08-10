import subprocess, yaml, json
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPConnection
"""Микро-сервис, запущенный без docker. Используется для перезагрузки настройки и перзагрузки сервисов."""

hostName = "localhost"
serverPort = 9000

backend_url = "localhost:8000"

class AsLiteral(str):
  pass

def represent_literal(dumper, data):
  return dumper.represent_scalar(yaml.resolver.BaseResolver.DEFAULT_SCALAR_TAG,
      data, style="|")

def create_nlu_yml(intents_data):
    intents_dict = {'version': '3.1', 'nlu': []}
    yaml.add_representer(AsLiteral, represent_literal)
    for item in intents_data:
        examples = item['examples'].replace("'", '').replace("- ", '').split('\r\n')
        examples_str = AsLiteral(yaml.dump(examples, allow_unicode=True))
        intents_dict['nlu'].append({'intent': item['intent'], 'examples': examples_str})
    return intents_dict

class MyServer(BaseHTTPRequestHandler):
    def __init__(self, process, *args):
        self.process = process
        BaseHTTPRequestHandler.__init__(self, *args)
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
            # os.system("docker-compose up --build --force-recreate --no-deps rasa")
            # os.popen("docker-compose up --build --force-recreate --no-deps rasa")
            # self.process
            
            self.send_response(code=200, message='Success')
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
        else:
            self.send_response(code=404, message="Path doesn't exist")
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()

if __name__ == "__main__":        
   
    process = subprocess.Popen(['docker-compose', 'up', '--build'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while process.poll() is None:
        print(process.stdout.readline().decode(encoding="utf-8"))
    
    webServer = HTTPServer((hostName, serverPort), MyServer(process))
    print(f"Docker Controller started http://{hostName}:{serverPort}")
    
    try:
        webServer.serve_forever()
        # os.popen('docker-compose up --build')        
    except KeyboardInterrupt:        
        process.stdout.close()
        pass
    
    webServer.server_close()
    print("Docker Controller stopped.")
    