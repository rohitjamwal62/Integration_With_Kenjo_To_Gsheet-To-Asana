input_data = {
    "Email":"w4mapsdfpbabous34cwwwsode2020@gmail.com",
    "description": "bahuballi",
    "summary":"Vcodify Technology",
    "duration":"56",
    "start":"2023-06-26T10:30:00-04:00",
    "eventname":"Google Msssssssseet",
    "end":"2023-06-26T10:30:00-04:00",
    "timezone":"America/New_York",
    "type":"default",
    "Event_Cal_Id":"123",
    "Guests":"neha@calendyze.com,jessica.johnson@divaris.com,andrew@calendyze.com"
    }
import requests,json
Email = input_data.get('Email')
description = input_data.get('description')
summary = input_data.get('summary')
duration = input_data.get('duration')
start = input_data.get('start')
eventname = input_data.get('eventname')
end = input_data.get('end')
timezone = input_data.get('timezone')
type = input_data.get('type')
calendar_id = input_data.get('Event_Cal_Id')
Guests = str(input_data.get('Guests'))


Get_Participants_Store = list()
Create_Participation_Store = list()

Bubble_Token ="61a316cb574d013104f3ce607fb6"
Bubble_TokenHeaders = {'Authorization': f'Bearer {Bubble_Token}','Accept': 'application/json','Content-Type': 'application/json'}

# Get Company
Company_url = "https://calendyze.bubbleapps.io/version-test/api/1.1/obj/Company"
response = requests.request("GET", Company_url, headers=Bubble_TokenHeaders)
if response.status_code == 200:
    Company_Name_Store = [rec.get('name') for rec in json.loads(response.text).get('response').get('results')]
    if summary not in Company_Name_Store:
        # Create Company
        print("Creating Company......................")
        payload = json.dumps({"name": summary})
        response = requests.request("POST", Company_url, headers=Bubble_TokenHeaders, data=payload)
        if response.status_code == 201:
            companyId = json.loads(response.text).get('id')
            company_Name = summary
    else:
        print("Existing company..................")
        Store_Company_Info = json.loads(response.text).get('response').get('results')
        for comp in Store_Company_Info:
            companyId = comp.get('_id')
            company_Name = comp.get('name') 
    
    if ',' in Guests:
        Store_Guests = str(Guests).split(',')
        for guest in Store_Guests:
            Store_Guest_Name = str(guest.split("@")[0]).capitalize()
            Store_Guest_Email = guest
            # Get user
            url = "https://calendyze.bubbleapps.io/version-test/api/1.1/obj/User"
            response = requests.request("GET", url, headers=Bubble_TokenHeaders)
            if response.status_code == 200:
                emailsExisting = json.loads(response.text).get('response').get('results')
                data = [em.get('authentication').get('email').get('email') for em in emailsExisting]
                if Store_Guest_Email in data:
                    for em in emailsExisting: 
                        if Store_Guest_Email == em.get('authentication').get('email').get('email'):
                            print("User already exist................")
                            if em.get('fullname'):
                                participants = em.get('fullname')
                            else:
                                participants = em.get('_id')
                            Get_Participants_Store.append(participants)
                            print(participants,"Participants Name")
                
                else:
                    # Create User
                    print("Create Single User")
                    url = "https://calendyze.bubbleapps.io/version-test/api/1.1/obj/user"
                    payload = {
                        "email": Store_Guest_Email,
                        "fullname":Store_Guest_Name,
                        "company":companyId
                        }
                    response = requests.post(url, headers=Bubble_TokenHeaders, json=payload)
                    participants_Id = json.loads(response.text)
                    participants_Name = Store_Guest_Name
                    Get_Participants_Store.append(participants_Name)
                    print("Participants Id: ",participants_Id,"participants Name: ",participants_Name)


des_list = list()
summ_list = list()
Match_Cal_id = list()
# Check Existing-----------
Event_url = "https://calendyze.bubbleapps.io/version-test/api/1.1/obj/Event"
response = requests.request("GET", Event_url, headers=Bubble_TokenHeaders)
if response.status_code == 200:
    Collect_Response = json.loads(response.text).get('response').get('results')
    for rec in Collect_Response:
        Match_Calender_Id = rec.get('calendar id')
        eve_descriptions = rec.get('description')
        eve_summary = rec.get('summary')
        # Event_Calender = rec.get('')
        des_list.append(eve_descriptions)
        summ_list.append(eve_summary)
        Match_Cal_id.append(Match_Calender_Id)
if calendar_id not in Match_Cal_id:
    # if summary not in summ_list and description not in des_list:
    print("Create Different event")
    type = input_data.get('type')
    if 'default' == type:
        payload = json.dumps({
            "Participants": Get_Participants_Store,
            "description": description,
            "summary":summary,
            "duration":str(duration),
            "start":start,
            "eventname":summary,
            "end":end,
            "timezone":timezone,
            "type":"Event",
            # "busy":"busy",
            # "recurring":"",
            "username":Email,
            # "username":summary
                "calendar id":calendar_id,
            #  "company":str(companyId)
                "Companyname":company_Name
        })
    response = requests.request("POST", Event_url, headers=Bubble_TokenHeaders, data=payload)
    output = {"User_Email":Email,"User Name":summary,"response":response.text}
    print("Sucessfully Create Event.......................",output)
else:
    output = {"Response":"Event Already Exists"}
    print(output)