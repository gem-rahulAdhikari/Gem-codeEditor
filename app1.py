from flask import Flask, render_template, jsonify,make_response, redirect,url_for, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse, abort
import logging
import json
import requests
from logging.handlers import RotatingFileHandler
import datetime

log_file = datetime.datetime.now().strftime('app_%Y-%m-%d.log')

app = Flask(__name__, static_folder='static')

CORS(app)
api = Api(app)

ip_address='34.131.140.81'

hashMap = { "Python": "Python (3.8.1)", "Java": "Java (OpenJDK 13.0.1)", "C": "C (GCC 9.2.0)"}


logging.basicConfig(filename=log_file,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/')
def home():
    name = request.args.get('name', 'World')
    print(name)
    return render_template('index.html')

@app.route('/api1/data123')
def get_data1():
    print('hello')
    return redirect(url_for('index'))

@app.route('/hiii')
def demo():
      url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getSubmissions"
      response = requests.get(url)
      if response.status_code == 200:
        data = response.json();
        for item in data:
         print(item['url'])
        
        return data
      else:
        raise Exception("Error accessing API: " + response.text)


   

@app.route('/select_lang', methods=['POST'])
def example_route():
    Selected_value = request.json.get('Selected_value')
    Selected_option = request.json.get('Selected_option')
    print(Selected_option)
    print(Selected_value)
    logging.info(Selected_option+": "+Selected_value)
    response = requests.get('http://'+ip_address+'/languages/all')
    data = response.json()
    return jsonify(data)   


@app.route('/run', methods=['POST'])
def submit_form():
    textarea_value = request.get_json()['textareaValue']
    Selected_value = request.get_json()['Selected_value']
    stdin = request.get_json()['stdin']
    print(Selected_value)
    print(textarea_value)
    print(stdin)
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': 'X-Auth-Token'
    }

    # Create the JSON body for the request
    json_body = {
       'source_code':textarea_value,
       'language_id': Selected_value,
       'stdin': stdin,
       'number_of_runs': None,
       'expected_output': None,
       'cpu_time_limit': None,
       'cpu_extra_time': None,
       'wall_time_limit': None,
       'memory_limit': None,
       'stack_limit': None,
       'max_processes_and_or_threads': None,
       'enable_per_process_and_thread_time_limit':None,
       'enable_per_process_and_thread_memory_limit': None,
       'max_file_size': None,
       'enable_network': None
    }

    # Send the POST request with the headers and JSON body
    response = requests.post('http://'+ip_address+'/submissions', headers=headers, json=json_body)

    data = response.json()
    out=tocken_gen(data['token'])
    logging.info("Code_Output"+":" +out)
    return out

@app.route('/submit', methods=['POST'])
def submit_form1():
    textarea_value = request.get_json()['textareaValue']
    Selected_value = request.get_json()['Selected_value']
    stdin = request.get_json()['stdin']
    name = request.args.get('name', 'World')
    print(Selected_value)
    print(textarea_value)
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': 'X-Auth-Token'
    }

    # Create the JSON body for the request
    json_body = {
       'source_code':textarea_value,
       'language_id': Selected_value,
       'stdin': stdin,
       'number_of_runs': None,
       'expected_output': None,
       'cpu_time_limit': None,
       'cpu_extra_time': None,
       'wall_time_limit': None,
       'memory_limit': None,
       'stack_limit': None,
       'max_processes_and_or_threads': None,
       'enable_per_process_and_thread_time_limit':None,
       'enable_per_process_and_thread_memory_limit': None,
       'max_file_size': None,
       'enable_network': None
    }

    # Send the POST request with the headers and JSON body
    response = requests.post('http://'+ip_address+'/submissions', headers=headers, json=json_body)

    data = response.json()
    out=tocken_gen(data['token'])
    logging.info("Code_Output"+":" +out)
    updateVal(out,name)
    
    # use the textarea_value variable as needed
    return out


def tocken_gen(token):
        
          url = 'http://'+ip_address+'/submissions/{}?base64_encoded=false&fields=stdout,stderr,status_id,language_id,source_code'.format(token)
          params = {"base64_encoded": "false", "fields": "stdout,stderr,status_id,language_id,source_code"}
          response = requests.get(url, params=params)
         
          
           
           
        # success, handle the response
          data = response.json()
          while data['status_id'] == 1 or data['status_id'] == 2:
                url = 'http://'+ip_address+'/submissions/{}?base64_encoded=false&fields=stdout,stderr,status_id,language_id,source_code'.format(token)
                params = {"base64_encoded": "false", "fields": "stdout,stderr,status_id,language_id,source_code"}
                response = requests.get(url, params=params)
                data = response.json()
               # print(data['status_id'])

          print(data)

          if data['status_id'] == 4 or data['status_id'] == 5 or data['status_id'] == 6 or data['status_id'] == 7 or data['status_id'] == 8 or data['status_id'] == 9 or data['status_id'] == 10 or data['status_id'] == 11 or data['status_id'] == 12 or data['status_id'] == 13 or data['status_id'] == 14:
               errorStatus=Status(data['status_id'])
               return errorStatus
               
          else :
               if data['stderr'] == None:
                     return data['stdout']
               else :
                    return data['stderr']
              
           
         # print(data['stdout'])
        
     
     
     
          
          #return data['stdout']
          
        # process the data
        # ...
         
def Status(StatusId):
     if StatusId == 4:
          error1="Wrong Answer"
          return error1
     elif StatusId == 5:
          error1="Time Limit Exceeded"
          return error1
     elif StatusId == 6:
          error1="Compilation Error"
          return error1
     elif StatusId == 7:
          error1="Runtime Error (SIGSEGV)"
          return error1
     elif StatusId == 8:
          error1="Runtime Error (SIGXFSZ)"
          return error1
     elif StatusId == 9:
          error1="Runtime Error (SIGFPE)"
          return error1
     elif StatusId == 10:
          error1="Runtime Error (SIGABRT)"
          return error1
     elif StatusId == 11:
          error1="Runtime Error (NZEC)"
          return error1
     elif StatusId == 12:
          error1="Runtime Error (Other)"
          return error1
     elif StatusId == 13:
          error1="Internal Error"
          return error1
     elif StatusId == 14:
          error1="Exec Format Error"
          return error1
          

def getUrl():
     url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getSubmissions"
     response = requests.get(url)
     if response.status_code == 200:
        data = response.json();
        for item in data:
          print(item['url'])
        
        
        return data
     else:
        raise Exception("Error accessing API: " + response.text)
    
     
def updateVal(submit_result):
    # url = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/updateData'
    # payload = {'value': submit_result}
    # response = requests.put(url, params=payload)
    # logging.info("Submitted_Code : "+submit_result)
    # return response.text
    
      api_url = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/updateSubmissions'

      payload = {
    'filter': {
        'url': 'https://gem-codeeditor.com/user/fbf8f89a27cd8a4e5eb64ee975e97286615461576a5349dc36da5983128859aa'
    },
    'newSubmission': submit_result
}

      headers = {
      'Content-Type': 'application/json'
                }

      response = requests.put(api_url, data=json.dumps(payload), headers=headers)

      if response.ok:
         response_data = response.json()
         print(response_data)
      else:
         print(f"Request failed with status code {response.status_code}")
           


if __name__ == '__main__':
    app.run(debug=True)
