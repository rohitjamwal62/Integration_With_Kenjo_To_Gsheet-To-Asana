input_data = {"Calender_Del_Id":"47ors16e7lgjpt0qvg1lusk"}
CalenderDel_Id = input_data.get('Calender_Del_Id')
import requests,json
headers = {'Authorization': 'Bearer 07689c20e47a9a670c56b2c150','Accept': 'application/json'}
Event_url = "https://calendyze.bubbleapps.io/version-test/api/1.1/obj/event"
response = requests.request("GET", Event_url, headers=headers)
if response.status_code == 200:
    Collect_Response = json.loads(response.text).get('response').get('results')
    for rec in Collect_Response:
        if rec.get('calendar id') != None:
            if CalenderDel_Id == rec.get('calendar id'):
                bubble_Event_Id = rec.get('_id')
                url = f"https://calendyze.bubbleapps.io/version-test/api/1.1/obj/event/{bubble_Event_Id}"
                response = requests.request("DELETE", url, headers=headers)
                output = {"Response":response.status_code}
                print(response.status_code,"Deleted Successfully")
