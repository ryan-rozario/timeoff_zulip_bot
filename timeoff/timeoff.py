from csv import reader
import requests 
import json
import os


TIMEOFF_API_TOKEN = os.environ.get('TIMEOFF_API_TOKEN', None)

BASE = "https://timeoff-zulipbot.herokuapp.com"

headers = {'Content-type': 'application/json', 'Accept': 'text/plain',"Authorization": "Bearer "+TIMEOFF_API_TOKEN}

class TimeoffHandler(object):
    '''
    This bot allows you to request, review and approve time off.
    '''

    def _split_commas(self,body):
        for line in reader([body]):
            return line
    
    def _create_request_parse(self,original_content):
        #request <manager email related to zulip account> for <vacation/sick leave/work from home> from DD/MM/YY to DD/MM/YY as <details>

        timeoff_request={
            "leave_type":None,
            "start_time":None,
            "end_time":None,
            "manager":None,
            "details":None
        }

        command, _, original_content = original_content.partition("request")
        timeoff_request["manager"], _, original_content = original_content.partition("for")
        timeoff_request["leave_type"], _, original_content = original_content.partition("from")
        timeoff_request["start_time"], _, original_content = original_content.partition("to")
        timeoff_request["end_time"], _, timeoff_request["details"] = original_content.partition("as")

        timeoff_request["manager"] = timeoff_request["manager"].strip()
        timeoff_request["leave_type"] = timeoff_request["leave_type"].strip()
        timeoff_request["start_time"] = timeoff_request["start_time"].strip()
        timeoff_request["end_time"] = timeoff_request["end_time"].strip()
        timeoff_request["details"] = timeoff_request["details"].strip()

        return timeoff_request


            



    def usage(self):
        return '''
        This bot allows you to request, review and approve time off.
        Version 1.0

        request <manager email related to zulip account> for <vacation/sick leave/work from home> from DD/MM/YY to DD/MM/YY as <details>

        approve request <application number>
        
        view requests sent

        view requests received
        '''

    def handle_message(self, message, bot_handler):
        original_content = message['content']
        original_sender = message['sender_email']
        #print(message)

        original_content = original_content.replace("@**timeoff|15742**", " ")
        original_content = original_content.replace("@**timeoff|15760**", " ")
        original_content = original_content.strip()

        command, _, body = original_content.partition(" ")

        command = command.strip().lower()

        if command=="request":
            timeoff_request=self._create_request_parse(original_content)
            timeoff_request["sender"]=original_sender
            url = "/api/leaves"
            url = BASE+url
            #print(timeoff_request)
            response = requests.post(url, data = json.dumps(timeoff_request) ,headers=headers)


            if response.status_code==200:
                leave_number = response.json()["id"]
                
                leave_mes = f' \nApplication Number : {leave_number} \n  Type : {timeoff_request["leave_type"]} \n Start Date : {timeoff_request["start_time"]} \n End Date : {timeoff_request["end_time"]} \n '

                bot_handler.send_reply(message, "Request has been Created."+leave_mes)

                bot_handler.send_message(dict(
                    type='private',
                    to=timeoff_request["manager"],
                    subject= f"Leave Request {leave_number}",
                    content="New Leave Request for Approval"+leave_mes
                ))


            else:
                bot_handler.send_reply(message, "There was an eror while creating your request. Please try again later")

        if command=="approve":
            body = original_content.replace("approve request", " ")
            body=body.strip()
            timeoff_request={"accepted":True}
            timeoff_request["manager"]=original_sender


            leave_id = body.strip().lower()
            url = "/api/leaves"
            url = BASE+url+"/"+leave_id
            
            response = requests.put(url, data = json.dumps(timeoff_request) ,headers=headers)



            if response.status_code==200:
                timeoff_request = response.json()
                print(timeoff_request)
                leave_number = timeoff_request["id"]
                leave_mes = f' \nApplication Number : {leave_number} \n  Type : {timeoff_request["leave_type"]} \n Start Date : {timeoff_request["start_time"]} \n End Date : {timeoff_request["end_time"]} \n '
                bot_handler.send_reply(message, "Request has been Approved."+leave_mes)

                bot_handler.send_message(dict(
                    type='private',
                    to=timeoff_request["sender"],
                    subject= f"Leave Request Approved {leave_number}",
                    content="Leave Request Approved" + leave_mes
                ))


            else:
                bot_handler.send_reply(message, "There was an eror while approving. Please try again later")


        if command=="view":
            body = original_content.replace("view requests", "")
            body = original_content.replace("view request", "")
            body=body.strip()
            option = body.strip().lower()
            url = "/api/leaves"
            url = BASE+url
            if option=="sent":


                timeoff_request={"sender":original_sender}

                response = requests.get(url, data = json.dumps(timeoff_request) ,headers=headers)
            elif option=="received":

                timeoff_request={"manager":original_sender}

                response = requests.get(url, data = json.dumps(timeoff_request) ,headers=headers)
            else:
                bot_handler.send_reply(message, "Incorrect Format")
            
            if response.status_code==200:
                response_list = response.json()

                

                leave_mes=""
                for timeoff_request in response_list:
                    leave_number = str(timeoff_request["id"])
                    leave_mes += f'Application Number : {leave_number}  Accepted:{timeoff_request["accepted"]}  \nType : {timeoff_request["leave_type"]}    Start Date : {timeoff_request["start_time"]}   End Date : {timeoff_request["end_time"]}  \nDetails : {timeoff_request["details"]}  \n\n '
                bot_handler.send_reply(message, leave_mes)


            else:
                bot_handler.send_reply(message, "There was an eror while approving. Please try again later. Use help command to view list of commands")


        if command=="help":
            mes = "request <manager email related to zulip account> for <vacation/sick leave/work from home> from DD/MM/YY to DD/MM/YY as <details>\n\n approve request <application number>\n\n view requests sent\n\n view requests received\n\n help \n\n"
            bot_handler.send_reply(message, mes)


            

            
        



handler_class = TimeoffHandler