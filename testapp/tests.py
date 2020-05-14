import requests
import json
# Create your tests here.

BASE_URL = 'http://127.0.0.1:8000/'
END_POINT = 'api/'

def get_resources(id=None):
	data={}
	if id is not None:
		data={
		'id':id
		}
	resp = requests.get(BASE_URL+END_POINT, data=json.dumps(data))
	print(resp.status_code)
	print(resp.json())
#get_resources(2) #with id
get_resources()   #without id

# def create_resource():
# 	new_emp = {
# 	'eno':700,
# 	'ename':'sunny',
# 	'esal':700000,
# 	'eaddr':'Mumbai',
# 	}
# 	r = requests.post(BASE_URL+END_POINT,data=json.dumps(new_emp))
# 	print(r.status_code)
# 	# print(r.text)
# 	print(r.json())
# create_resource()

# def update_resource(id):
# 	new_data = {
# 	'id':id,
# 	'eaddr':'Ameerpet',
# 	'esal':1500000,
# 	}
# 	r = requests.put(BASE_URL+END_POINT,data=json.dumps(new_data))
# 	print(r.status_code)
# 	print(r.json())
# update_resource(1)	


# def delete_resource(id):
# 	data={
# 	'id':id,
# 	}
# 	r = requests.delete(BASE_URL+END_POINT,data=json.dumps(data))
# 	print(r.status_code)
# 	print(r.json())
# delete_resource(7)


