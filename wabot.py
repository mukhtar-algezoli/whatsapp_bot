import json
import requests
import datetime

from flask import Flask, request, jsonify
#from wabot import WABot
import json

from flask import Flask, request
from transitions import Machine

users = {}
machines = {}
triggers = None


class Map(object):
    pass

def initFsm(chatId):
   user = Map()


   # The states
   states=['START', 'VOICE', 'Data_Services','IVR', 'BACK', 'SIM_BROADBAND', 'INDEPENDENT_4G_SERVICES', 'POST_PAID', 'PREPAID']


   #the transitions
   transitions = [
    #    { 'trigger': 'GREETING', 'source': 'START', 'dest': 'GREETING' },
    #    { 'trigger': 'BACK', 'source': 'GREETING', 'dest': 'START' },
    #    { 'trigger': 'VOICE', 'source': 'GREETING', 'dest': 'VOICE' },
    #    { 'trigger': 'BACK', 'source': 'VOICE', 'dest': 'GREETING' },
    #    { 'trigger': 'Data_Services', 'source': 'GREETING', 'dest': 'Data_Services' },
    #    { 'trigger': 'BACK', 'source': 'Data_Services', 'dest': 'GREETING' },
    #    { 'trigger': 'IVR', 'source': 'GREETING', 'dest': 'IVR' },
    #    { 'trigger': 'BACK', 'source': 'IVR', 'dest': 'GREETING' },
      
       { 'trigger': 'Data_Services', 'source': 'START', 'dest': 'Data_Services' },
       { 'trigger': 'BACK', 'source': 'Data_Services', 'dest': 'START' },
       { 'trigger': 'IVR', 'source': 'START', 'dest': 'IVR' },
       { 'trigger': 'BACK', 'source': 'IVR', 'dest': 'START' },
       { 'trigger': 'VOICE', 'source': 'START', 'dest': 'VOICE' },
       { 'trigger': 'BACK', 'source': 'VOICE', 'dest': 'START' },
       { 'trigger': 'POST_PAID', 'source': 'VOICE', 'dest': 'POST_PAID' },
       { 'trigger': 'BACK', 'source': 'POST_PAID', 'dest': 'VOICE' },
       { 'trigger': 'PREPAID', 'source': 'VOICE', 'dest': 'PREPAID' },
       { 'trigger': 'BACK', 'source': 'PREPAID', 'dest': 'VOICE' },
       { 'trigger': 'SIM_BROADBAND', 'source': 'Data_Services', 'dest': 'SIM_BROADBAND' },
       { 'trigger': 'BACK', 'source': 'SIM_BROADBAND', 'dest': 'Data_Services' },
       { 'trigger': 'INDEPENDENT_4G_SERVICES', 'source': 'Data_Services', 'dest': 'INDEPENDENT_4G_SERVICES' },
       { 'trigger': 'BACK', 'source': 'INDEPENDENT_4G_SERVICES', 'dest': 'Data_Services' }
    #    { 'trigger': 'CHECKING_ACCOUNT', 'source': 'ACCOUNTS', 'dest': 'CHECKING_ACCOUNT' },
    #    { 'trigger': 'BACK', 'source': 'CHECKING_ACCOUNT', 'dest': 'ACCOUNTS' },
    #    { 'trigger': 'SAVINGS_ACCOUNT', 'source': 'ACCOUNTS', 'dest': 'SAVINGS_ACCOUNT' },
    #    { 'trigger': 'BACK', 'source': 'SAVINGS_ACCOUNT', 'dest': 'ACCOUNTS' }
]

   # Initialize
   users[chatId] = user
   machines[chatId] = Machine(user, states=states, transitions=transitions, initial='START')

class WABot():
  def __init__(self, json):
    self.json = json
    self.dict_messages = json['messages']
    self.APIUrl = 'https://api.chat-api.com/instance272372/'
    self.token = 'kyzv7ana3jo9nfo7'
  def send_requests(self, method, data):  
    url = f"{self.APIUrl}{method}?token={self.token}"
    headers = {'Content-type': 'application/json'}
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    return answer.json()
  def send_message(self, chatId, text):
    data = {"chatId" : chatId,
            "body" : text}
    answer = self.send_requests('sendMessage', data)
    return answer

  def send_image(self, chatId, body, filename):
    data = {
      'chatId' : chatId,
      'body' : body,
      'filename' : filename,
      'caption'  : f''

    }
    answer = self.send_requests('sendFile', data)
    return answer
  
  def welcome(self,chatId, noWelcome = False):
        global triggers
        welcome_string = ''
        if (noWelcome == False):
            welcome_string = "Y'ello, how can I help you?\n"
            
        welcome_string = welcome_string + "Please choose a number:\n"
        for index,trigger in enumerate(triggers):
             welcome_string = welcome_string + str(index + 1) + "." + trigger + "\n"   

        return self.send_message(chatId, welcome_string)

  def send_SIM_BROADBAND(self, chatId):
      
      return self.send_image(chatId,'https://i.imgur.com/irfSoVi.jpg', 'irfSoVi.jpg')

  def INDEPENDENT_4G_SERVICES(self, chatId):
      return self.send_image(chatId,'https://i.imgur.com/pXNI2IP.jpg', 'pXNI2IP.jpg')

  def VOICE(self, chatId):
      return self.send_message(chatId, "send IVR")

  def IVR(self, chatId):
      message = """The Cloud IVR is one of the most sophisticated tools for great automated service by giving the customer optimized self-service options and lower operation cost. 
 You can choose the number of departments (customer options), and the number pf extensions associated with each department. 
 The basic bundle include two departments and two extensions. You can send a text and we will process the recording, or you can send a one minute STANDARD audio. Service fees are shown below:"""
      self.send_message(chatId, message)

      return self.send_image(chatId,'https://i.imgur.com/iLob0Su.jpg', 'iLob0Su.jpg')
    
  def POST_PAID(self, chatId):
      return self.send_message(chatId, "POST_PAID offers")

  def PREPAID(self, chatId):
      return self.send_message(chatId, "PREPAID offers")
  






  def processing(self):
    global triggers
    global machines
    if self.dict_messages != []:
      for message in self.dict_messages:
        text = message['body'].split()
        if not message['fromMe']:
            id  = message['chatId']
            try:
                    new_user = id not in users
                    if new_user:
                        initFsm(id)

                    triggers = machines[id].get_triggers(users[id].state)
                    triggers = [k for k in triggers if 'to' not in k]
                    triggers = [k for k in triggers if 'BACK' not in k]
                    if "Data_Services" not in triggers:
                        triggers.append('BACK')
                    if not new_user and triggers[int(text[0].lower()) - 1] == "SIM_BROADBAND":
                        return self.send_SIM_BROADBAND(id)

                    if not new_user and triggers[int(text[0].lower()) - 1] == "INDEPENDENT_4G_SERVICES":
                        return self.INDEPENDENT_4G_SERVICES(id)

                    if not new_user and triggers[int(text[0].lower()) - 1] == "IVR":
                        return self.IVR(id)
                    
                    if not new_user and triggers[int(text[0].lower()) - 1] == "POST_PAID":
                        return self.POST_PAID(id)
                    
                    if not new_user and triggers[int(text[0].lower()) - 1] == "PREPAID":
                        return self.PREPAID(id)
                    
                    # if not new_user and triggers[int(text[0].lower()) - 1] == "VOICE":
                    #     self.send_message(id, message)
                    
                    else:
                        if not new_user:
                            get_trigger = triggers[int(text[0].lower()) - 1]
                            getattr(users[id],get_trigger)()
                        
                        if not new_user and triggers[int(text[0].lower()) - 1] == "VOICE":
                            message = """ Customer will be provided with NEW 093xxxx Range for the required number of Lines and the same range can be reserved for future use. 
            All lines are CUG FREE (Free Calls within the Corporate closed user group) """
                            self.send_message(id, message)
                        triggers = machines[id].get_triggers(users[id].state)
                        triggers = [k for k in triggers if 'to' not in k]
                        triggers = [k for k in triggers if 'BACK' not in k]
                        if "Data_Services" not in triggers:
                            triggers.append('BACK')
                        print(triggers)
                        if text[0].lower() == 'hi':
                            return self.welcome(id)
                        else:
                            # content = triggers[int(text[0].lower()) - 1]
                            return self.welcome(id, True)
            except:
              return self.send_message(id, "wrong command")
    else:
      return 'NoCommand'


  



app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        bot = WABot(request.json)
        bot.processing()
    return "valid response"

if(__name__) == '__main__':
    app.run()

