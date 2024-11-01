import json
from .eg1 import get_data

def get_suspect_data():
    data=get_data()
    with open(r'C:\Desktop\CodeUtsava\Project\api\drugtrafficking\Models\susp_user.json','r') as file:
        suspected_user_id=json.load(file)
    
    suspected_user_data=[]
    for inst in data:
        if inst['id'] in suspected_user_id:
            suspected_user_data.append(inst)
    return data

get_suspect_data()