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
    
    def _create_request_parse(self,body):


        body = self._split_commas(body)
        #print(body)
        timeoff_request={
            "leave_type":None,
            "start_time":None,
            "end_time":None,
            "manager":None,
            "details":None
        }
        for line in body:
            body_head, _, body_body  = line.partition(":")
            body_head = body_head.strip().lower()
            body_body = body_body.strip().lower()
            #print(body_head)
            #print(body_body)
            if body_head=="type":
                timeoff_request["leave_type"] = body_body
            elif body_head=="start":
                timeoff_request["start_time"] = body_body
            elif body_head=="end":
                timeoff_request["end_time"] = body_body
            elif body_head=="manager":
                timeoff_request["manager"] = body_body
            elif body_head=="details":
                timeoff_request["details"] = body_body
            else:
                return 0

        return timeoff_request


            



    def usage(self):
        return '''
        This bot allows you to request, review and approve time off.
        Version 1.0

        create_request type:<vacation/sick leave/work from home>, details:<details>, start :DD/MM/YY, end:DD/MM/YY, manager:<manager email related to zulip account>
        
        approve_request <application number>
        
        view_requests sent
        
        view_requests received
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
            
            command, _, body = original_content.partition("request")
            command, _, body = original_content.partition("for")            

            command, _, body = body.partition(" ")

            timeoff_request=self._create_request_parse(body)
            if timeoff_request==0:
                bot_handler.send_reply(message, "Incorrect Format")
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
            body = message.replace("approve request", " ")
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
            body = message.replace("view requests", "")
            body = message.replace("view request", "")
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
            mes = " create_request type:<vacation/sick leave/work from home>, details:<details>, start :DD/MM/YY, end:DD/MM/YY, manager:<manager email related to zulip account>\n\n approve request <application number>\n\n view requests sent\n\n view requests received\n\n help \n\n"
            bot_handler.send_reply(message, mes)


            

            
        



handler_class = TimeoffHandler