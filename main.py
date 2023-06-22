from flask import Flask, render_template, jsonify,make_response, redirect,url_for, request, g, session, Response
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse, abort
import logging
from datetime import datetime, timedelta,date
from flask_session import Session
import json
import requests
import os
from logging.handlers import RotatingFileHandler
import datetime 
import time
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://flask-app-b27bb-default-rtdb.firebaseio.com'
})

log_file = datetime.datetime.now().strftime('app_%Y-%m-%d.log')

app = Flask(__name__, static_folder='static')

active_keys = set()
access_duration = timedelta(seconds=30)

CORS(app)
api = Api(app)

ip_address='34.136.47.80'

hashMap = { "Python": "Python (3.8.1)", "Java": "Java (OpenJDK 13.0.1)", "C": "C (GCC 9.2.0)"}


logging.basicConfig(filename=log_file,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#login logic for admin---------------------
json_file_path = os.path.join(os.getcwd(), 'data', 'data.json')
app.secret_key=os.urandom(24)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
Session(app)

emailKey ='';

@app.route('/login')
def login():
    if g.user:
     return redirect(url_for('protected'))
    else:
       return render_template('login.html') 


@app.route('/login',methods=['GET','POST'])
def index():
    session.permanent = True
    if request.method == "POST":
        
        session.pop('user', None)
        session.pop('password', None)
        username=request.form["username"]
        password=request.form["password"]
        url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/admin"
        response = requests.get(url)
        if response.status_code == 200:
           data = response.json();
        for item in data:
          if username == item['userId']:
           fetchedUsername = item['userId']
           fetchedpassword = item['password']
           Role = item['Role']
          
        if(username==fetchedUsername and password==fetchedpassword and Role =='Admin'):
            session['user']=username
            session['password']=password
            session['role'] = Role
            return redirect(url_for('protected',Role=Role))
        elif(username==fetchedUsername and password==fetchedpassword and Role =='HR'):
             session['user']=username
             session['password']=password
             session['role'] = Role
             return redirect(url_for('protected',Role=Role))
        else:
            return render_template('error.html') 
        
    return render_template('login.html')    
        

@app.route('/admin')
def protected1():
    if g.user:
        data_array = []
        keys_to_display = ['_id','name','url','modified','status']
        url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getSubmissions"
        #url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getSubmission"
        response = requests.get(url)
        if response.status_code == 200:
           data = response.json();
           for item in data:
            fetchedUrl = item['url']
            result = fetchedUrl.split("/")
            print(result)
           
            filtered_item = {k: v for k, v in item.items() if k in keys_to_display}
            data_array.append(filtered_item)
            headers = [k.upper() for k in keys_to_display]  
        return render_template('demo.html', data=data_array,headers=headers)
           
        
    return redirect(url_for('index'))
        


@app.route('/stream')
def stream():
    def event_stream():
        messages = []
        def callback(snapshot):
            messages.append(snapshot.val())
        messagesRef = db.reference('messages')
        messagesRef.order_by_key().limit_to_last(50).on('child_added', callback)
        while True:
            if messages:
                yield 'data: {}\n\n'.format(json.dumps(messages.pop()))
    return Response(event_stream(), mimetype="text/event-stream")


@app.before_request
def before_request():
    print("start")
    g.user = None

    if 'user' in session:
           
          g.user = session['user']
          print(g.user+"this is user")

    
      

@app.route("/logout", methods=["POST"])
def dropsession():
    session.pop('user', None)
    session.pop('password', None)
    return render_template('login.html')



# @app.route("/data")
# def get_data():
#       data_array = []
#       keys_to_display = ['_id','name','url']
#       url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getSubmissions"
#       response = requests.get(url)
#       if response.status_code == 200:
#        data = response.json()
#        print(type(data))
#        for item in data:
#          filtered_item = {k: v for k, v in item.items() if k in keys_to_display}
#          data_array.append(filtered_item)
#        headers = [k.upper() for k in keys_to_display]  
#       return render_template('demo.html', data=data_array,headers=headers)



#--------------------AdminTbale---------------------------

# @app.route("/data")
# def protected():
#     role = request.args.get('Role')
#     print("this is"+role);
#     if g.user:  
#       data_array = []
#       keys_to_display = ['_id','Status','Name','Recruiter','Experience','Current_Company']
#     #   keys_to_display_hr = ['_id', 'Status', 'Name', 'Recruiter', 'Experience', 'Current_Company']
#     #   keys_to_display_admin = ['_id', 'Name','Recruiter', 'Experience', 'Current_Company']  # Adjust this list according to the columns you want to display for normal users

#     #   url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getAdminTableData"
#       with open(json_file_path) as f:
#         data = json.load(f)
#         url =  data.get("adminTableData", "")
     
#       response = requests.get(url)
#       if response.status_code == 200:
#         data = response.json()
#         for item in data:
#           filtered_item = {k: v for k, v in item.items() if k in keys_to_display}
#         # Combine values of Key1 and Key2 into a new column called CombinedKey
#           filtered_item['CombinedKey'] = f"{item.get('url', '')} {item.get('SecretKey', '')}"
#           data_array.append(filtered_item)
#         headers = [k.upper() for k in keys_to_display] + ['Url and SecretKey']  # Add CombinedKey to the headers list
#       return render_template('adminTable.html', data=data_array, headers=headers)
#     return redirect(url_for('index'))
@app.route("/data")
def protected():
    role = request.args.get('Role')
    print("this is"+role);
    if g.user:  
      data_array = []
    #   keys_to_display = ['_id','Status','Name','Recruiter','Experience','Current_Company']
      keys_to_display_hr = ['_id', 'Status', 'Name', 'Recruiter', 'Experience', 'Current_Company','keyStatus']
      keys_to_display_admin = ['_id', 'Status', 'Name', 'Recruiter', 'Experience', 'Current_Company']  # Adjust this list according to the columns you want to display for normal users

    #   url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getAdminTableData"
      with open(json_file_path) as f:
        data = json.load(f)
        url =  data.get("adminTableData", "")
     
      response = requests.get(url)
      if response.status_code == 200:
        data = response.json()
        headers = []
        if role == 'HR':
             print("this is hr")
             keys_to_display = keys_to_display_hr
             headers = [k.upper() for k in keys_to_display] + ['Url and SecretKey']
        else:
              print("this is admin")
              keys_to_display = keys_to_display_admin
              headers = [k.upper() for k in keys_to_display]
        for item in data:
          filtered_item = {k: v for k, v in item.items() if k in keys_to_display}
          filtered_item['CombinedKey'] = f"{item.get('url', '')} {item.get('SecretKey', '')}"
          data_array.append(filtered_item)
          # Add CombinedKey to the headers list
      return render_template('adminTable.html', data=data_array, headers=headers,role=role)
    return redirect(url_for('index'))




#---------------------------------------------------------------------


@app.route('/updateTable', methods=['POST'])
def update_status():
    row_id = request.form.get('rowId')
    new_value = request.form.get('newValue')
    email=''
    reqKey = request.form.get('key')
    print(row_id);
    print(new_value);
  
    print(reqKey);

    # url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getAdminTableData"
    with open(json_file_path) as f:
        data = json.load(f)
        url =  data.get("adminTableData", "")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json();
    for item in data:
        id_value = item['_id']
        if(row_id==id_value):
            email = item['Email'];
            emailKey=email;
            print(emailKey)
            break;
    print(email+"hello email")
    with open(json_file_path) as f:
        data = json.load(f)
        api_url =  data.get("updateAdminTableData", "")
    # api_url = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/updateAdminTable'

    payload = {
    'filter': {
       'Email': email
  
    },
    "key": reqKey,
    "value": new_value
    
    
}

    headers = {
      'Content-Type': 'application/json'
                }

    response = requests.put(api_url, json=payload, headers=headers)

    if response.ok:
         response_data = response.json()
         print(response_data)
    else:
         print(f"Request failed with status code {response.status_code}")

    
    return jsonify({'success': True})
#-------------------------------------

#--------------------AdminTbale---------------------------

# @app.route('/updateStatus', methods=['POST'])
# def update_status():
#     row_id = request.form.get('rowId')
#     new_value = request.form.get('newValue')
#     url = request.form.get('url')
#     print(row_id);
#     print(new_value);
#     print(url);
#     api_url = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/updateStatus'

#     payload = {
#     'filter': {
#       # 'url': 'https://gem-codeeditor.com/user/fbf8f89a27cd8a4e5eb64ee975e97286615461576a5349dc36da5983128859aa'
#        'url': url
  
#     },
#     'status':new_value,
    
    
# }

#     headers = {
#       'Content-Type': 'application/json'
#                 }

#     response = requests.put(api_url, data=json.dumps(payload), headers=headers)

#     if response.ok:
#          response_data = response.json()
#          print(response_data)
#     else:
#          print(f"Request failed with status code {response.status_code}")

#     # Process the data as needed
#     # Return a JSON response
#     return jsonify({'success': True})
   


#---------------------------------------

keyStatus='F';

@app.route('/')
def home():
     full_url = request.url
     print("hello")
     url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getAdminTableData"
     response = requests.get(url)
     if response.status_code == 200:
        data = response.json();
        for item in data:
            print(item)
            print(full_url)
            if full_url == item['url']:
                keyStatus=item['keyStatus']
                print(keyStatus+"this is key STATUS")
                break;
    
     if keyStatus == 'F':
         return redirect(url_for('error'))
                
        
     return render_template('index.html', logged_in=True)
    

@app.route('/url')
def url():
   
    return render_template('uniqueUrlGenerator.html')

@app.route('/select_lang', methods=['POST'])
def languageSelection_route():
    Selected_value = request.json.get('Selected_value')
    Selected_option = request.json.get('Selected_option')
    print(Selected_option)
    print(Selected_value)
    logging.info(Selected_option+": "+Selected_value)
    response = requests.get('http://'+ip_address+'/languages/all')
    data = response.json()
    return jsonify(data)   


@app.route('/run', methods=['POST'])
def run_form():
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
def submit_form():
    today = date.today()
    date_string = today.strftime("%Y-%m-%d")
    textarea_value = request.get_json()['textareaValue']
    Selected_value = request.get_json()['Selected_value']
    input_value = request.get_json()['inputValue']
    output_value = request.get_json()['outputValue']
    stdin = request.get_json()['stdin']
    name = request.get_json()['name']
    print("lello")
    print(name)
    print(Selected_value)
    print(textarea_value)
    print(today)
    print("lello")
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
    req_url=getUrl(name)
    print("helloooo");
    print(req_url)
    req_name=getName(req_url)
    print("heloo prya")
    print(req_name)
    updateVal(out,req_url,textarea_value,input_value,output_value,date_string)
    
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
          

def getUrl(name):
     my_bool = False;
     with open(json_file_path) as f:
        data = json.load(f)
        url =  data.get("getSubmissions", "")
    #  url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getSubmissions"
     response = requests.get(url)
     if response.status_code == 200:
        data = response.json();
        for item in data:
          fetchedUrl = item['url']
          print( fetchedUrl)
          result = fetchedUrl.split("/")
          print(result)
          my_string = result[-1]
          result1 = my_string.split("=")
          print(result1[-1])
          if result1[-1] == name:
              my_bool=True;
              print("got it")
              return item['url']
         
        print("not find")
        setUrl(name)
        return name      
          
     else:
        raise Exception("Error accessing API: " + response.text)
     


def setUrl(name):
     
     req_url="https://gem-codeeditor.wl.r.appspot.com/?name="+name
     req_name=getName(req_url)
     with open(json_file_path) as f:
        data = json.load(f)
        api_url =  data.get("setSubmissions", "")
    #  api_url = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/userSubmissions'

     data = {
    # Replace with your body parameter
    "submissions": [],
    "submittedCode": [],
    "inputArray": [],
    "outputArray": [],
    "name":req_name,
     # "url": "http://127.0.0.1:5000/?name="+name
    "url": "https://gem-codeeditor.wl.r.appspot.com/?name="+name,
     "modified":"",
     "status":"None",
            },
    

     headers = {
         'Content-Type': 'application/json'
           }

     response = requests.post(api_url, headers=headers, data=json.dumps(data))
     response_json = response.json()
     print(response_json)    
    
     
def updateVal(submit_result,name,textarea_value,input_value,output_value,today):
      print("this is updateVal")
      print(textarea_value)
      print(input_value)
      print(output_value)
      
      
      with open(json_file_path) as f:
        data = json.load(f)
        api_url =  data.get("updateSubmissions", "")


      api_url1 = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getSubmissions'
      response1 = requests.get(api_url1)
      if response1.status_code == 200:
        data = response1.json()  # Assuming the response is in JSON format
        for item in data:
            fetchedUrl = item['url']
            if fetchedUrl == name:
                req_Round=item['Rounds']
                rounds_length = len(req_Round[0])
                print(rounds_length)
                print(req_Round)
                print(req_Round[0].get(str(rounds_length)))
                req_data=req_Round[0].get(str(rounds_length))
                print(type(req_data))
                print(type(req_data[0]));
                
                for key, value in req_data[0].items():
                    if key == 'SubmittedCode':
                        if value:
                            print("SubmittedCode is not empty.")
                            api_url3 = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/updateRounds'
                     
                            payload = {
                                       'filter': {
                                                    'url': name
  
                                       },
                                       "submission_No":"2",
                                       'submittedCode':textarea_value,
                                       'inputParameter': input_value,
                                       'output': output_value,
                                        "roundNumber":rounds_length
                                       }

                            headers = {
                                'Content-Type': 'application/json'
                                        }
                            response = requests.put(api_url3, data=json.dumps(payload), headers=headers)

                            if response.ok:
                             response_data = response.json()
                             print(response_data)
                            else:
                              print(f"Request failed with status code {response.status_code}")
                         
                        else:
                          print("it is empty")
                          api_url2 = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/updateRoundsSubmission'
                          payload = {
                                       'filter': {
                                                    'url': name
  
                                       },
                                      
                                       "submittedCode": textarea_value,
                                       "inputParameter": input_value,
                                       "output": output_value,
                                        "roundNumber":rounds_length
                                       
                                       }

                          headers = {
                                'Content-Type': 'application/json'
                                        }
                          response = requests.put(api_url2, data=json.dumps(payload), headers=headers)

                          if response.ok:
                             response_data = response.json()
                             print(response_data)
                          else:
                              print(f"Request failed with status code {response.status_code}")
                            
                     
                    
                

                # print(len(req_Round))
                # if len(req_Round) == 1:
                #  for round_data in req_Round:
                #     submission_array = round_data["1"]
                #     print(submission_array+"this is submission array")
                #     for submission_data in submission_array:
                #         if submission_data['SubmittedCode'] == '':
                #             print("moves to if")
                #             api_url2 = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/updateRoundsSubmission'
                #             payload = {
                #                        'filter': {
                #                                     'url': name
  
                #                        },
                #                        'submittedCode':textarea_value,
                #                        'inputParameter': input_value,
                #                        'output': output_value
                #                        }

                #             headers = {
                #                 'Content-Type': 'application/json'
                #                         }
                #             response = requests.put(api_url2, data=json.dumps(payload), headers=headers)

                #             if response.ok:
                #              response_data = response.json()
                #              print(response_data)
                #             else:
                #               print(f"Request failed with status code {response.status_code}")

                #         else:
                #                 print("moves to else")
                #                 api_url3 = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/updateRounds'
                #                 payload = {
                #                     'filter': {
                #                         'url': name
  
                #                            },
                #                            "submission_No":len(submission_array)+1,
                #                            "submittedCode": textarea_value,
                #                            "inputParameter": input_value,
                #                            "output": output_value,
                #                            "req_Round":"0"
                #                 }
                #                 headers = {
                #                 'Content-Type': 'application/json'
                #                         }
                #                 response = requests.put(api_url3, data=json.dumps(payload), headers=headers)
                #                 break;
                # else:
                #     print("there are other rounds also")
                #     req_len=len(req_Round)
                #     print(req_len)
                    # array_object = req_Round[len(req_Round)-1]["2"]#.get('0',"2 not found")
                    # print(array_object)
                    # Process each item in the response
            
      else:
        print("API request failed with status code:", response1.status_code)

# def updateVal(submit_result,name,textarea_value,input_value,output_value,today):
#      api_url1 = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getSubmissions'
#      response1 = requests.get(api_url1)
#      if response1.status_code == 200:
#           data = response1.json()  
#           for item in data:
#             fetchedUrl = item['url']
#             if fetchedUrl == name:
#                 req_Round=item['Rounds']
#                 print(len(req_Round))




        #------------------------------------------------------------------------

    

    #   api_url2 = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/updateRoundsSubmission'

    #   payload = {
    # 'filter': {
    #       'url': name
  
    # },
    # 'newSubmission': submit_result,
    # 'code' : textarea_value,
    # 'input': input_value,
    # 'output': output_value,
    # 'modified':today,
    # 'submittedCode':textarea_value,
    # 'inputParameter': input_value,
    # 'output': output_value

# }

#       headers = {
#       'Content-Type': 'application/json'
#                 }

    #   response = requests.put(api_url2, data=json.dumps(payload), headers=headers)

    #   if response.ok:
    #      response_data = response.json()
    #      print(response_data)
    #   else:
    #      print(f"Request failed with status code {response.status_code}")
         
           
def getName(req_url):
    with open(json_file_path) as f:
        data = json.load(f)
        url =  data.get("getSubmissions", "")
        print("hello how are you")
    # url = "https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getSubmission"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json();
        
        for item in data:
          print(item)
          if item['url'] == req_url:
             req_name=item['name']
             print(req_name)
             return req_name
          


# @app.route('/updateTable', methods=['POST'])
# def update_status():

#     return 1;          
# @app.route('/generate_session/<key>',methods=['POST'])
# def generate_session(key):
#     # print(key)
#     if key not in active_keys:
#         # print("hello bhai")
#         active_keys.add(key)
#         session['key_active'] = True
#         session.permanent = True
#         expiry_time = datetime.datetime.now() + access_duration
#         expiry_time_str = expiry_time.strftime('%Y-%m-%d %H:%M:%S')
#         session['expiry_time'] = expiry_time_str
#         return redirect(url_for('open_page'))
#     else:
#         return redirect(url_for('error'))
    

# @app.route('/open_page')
# def open_page():
#     print("hello sir")
#     if ('key_active' in session and session['key_active']) and session_valid():
#         print("hello key is active")
#         return render_template('open_page.html')
#     else:
#         return redirect(url_for('error'))    

# def session_valid():
#     if 'expiry_time' in session:
#         print("hello");
#         expiry_time_str = session['expiry_time']
#         expiry_time = datetime.datetime.strptime(expiry_time_str, '%Y-%m-%d %H:%M:%S')
#         if datetime.datetime.now() < expiry_time:
#             return True
#     return False

# @app.route('/expire_session/<key>',methods=['POST'])
# def expire_session(key):
#     active_keys.clear()
#     session.pop('key_active', None)
#     return redirect(url_for('error'))

@app.route('/error')
def error():
    print("heelooo errror")
    return render_template('error1.html')        

if __name__ == '__main__':
    app.run(debug=True)
