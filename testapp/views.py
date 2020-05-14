from django.shortcuts import render
from django.views.generic import View
from .models import Employee
import json
from .utils import is_json
from django.http import HttpResponse
from .mixins import SerializeMixin, HttpResopnseMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import EmployeeForm

# Create your views here.


@method_decorator(csrf_exempt,name='dispatch')
class EmployeeCRUDCBV(SerializeMixin,HttpResopnseMixin,View):
	def get_object_by_id(self,id):
		try:
			emp = Employee.objects.get(id=id)
		except Employee.DoesNotExist:
			emp = None
		return emp
	def get(self,request,*args,**kwargs):
		data = request.body
		if not is_json(data):
			return self.render_to_http_response(json.dumps({'msg':'please send valid json data only'}),status=400)
		data = json.loads(request.body)
		id = data.get('id',None)
		if id is not None:
			obj = self.get_object_by_id(id)
			if obj is None:
				return self.render_to_http_response(json.dumps({'msg':'No matched record with specfied id'}),status=404)
			json_data = self.serialize([obj,])
			return self.render_to_http_response(json_data)
		qs = Employee.objects.all()
		json_data = self.serialize(qs)
		return self.render_to_http_response(json_data)

	def post(self,request,*args,**kwargs):
		data = request.body
		if not is_json(data):
			return self.render_to_http_response(json.dumps({'msg':'please send valid json data only'}),status=400)
		empdata = json.loads(request.body)
		form = EmployeeForm(empdata)
		if form.is_valid():
			obj = form.save(commit=True)
			return self.render_to_http_response(json.dumps({'msg':'resource created successfully'}))
		if forms.erros:
			json_data = json.dumps(forms.errors)
			return self.render_to_http_response(json_data, status=400)

	def put(self,request,*args,**kwargs):
		data = request.body
		if not is_json(data):
			return self.render_to_http_response(json.dumps({'msg':'please send valid json data only'}), status=400)
		data = json.loads(data)
		id = data.get('id',None)
		if id is None:
			return self.render_to_http_response(json.dumps({'msg':'Id is compulsary for updation'}), status=400)
		obj = self.get_object_by_id(id)
		if obj is None:
			json_data = json.dumps({'msg':'Record not found, unable to perform updation'})
			return self.render_to_http_response(json_data, status=404)
		new_data = data
		old_data={
		'eno': obj.eno,
		'ename': obj.ename,
		'esal': obj.esal,
		'eaddr': obj.eaddr,
		}
		old_data.update(new_data)
		form = EmployeeForm(old_data, instance=obj)
		if form.is_valid():
			form.save(commit=True)
			json_data = json.dumps({'msg':'Resource Updated Successfully'})
			return self.render_to_http_response(json_data, status=201)
		if form.errors:
			json_data = json.dumps(form.errors)
			return self.render_to_http_response(json_data, status=400)

	def delete(self,request,*args,**kwargs):
		data = request.body
		if not is_json(data):
			return self.render_to_http_response(json.dumps({'msg':'please send valid json data only'}), status=400)
		data = json.loads(data)
		id = data.get('id',None)
		if id is None:
			return self.render_to_http_response(json.dumps({'msg':'Id is compulsary for deletion'}), status=400)
		obj = self.get_object_by_id(id=id)
		if obj is None:
			json_data = json.dumps({'msg':'No matched record found, not possible to perform deletion'})
			return self.render_to_http_response(json_data,status=404)
		status, deleted_item = obj.delete()
		if status==1:
			json_data = json.dumps({'msg': 'Resource deleted successfully'})
			return self.render_to_http_response(json_data,status=201)
		json_data = json.dumps({'msg':'Unnable to delete. Please try again'})
		return self.render_to_http_response(json_data,status=500)



# @method_decorator(csrf_exempt, name='dispatch')
# class EmployeeListCBV(HttpResopnseMixin,SerializeMixin,View):
# 	def get_object_by_id(self,id):
# 		try:
# 			emp = Employee.objects.get(id=id)
# 		except Employee.DoesNotExist:
# 			emp = None
# 		return emp

# 	def get(self,request,*args,**kwargs):
# 		data = request.body
# 		if not is_json(data):
# 			return self.render_to_http_response(json.dumps({'msg':'please send valid json data only'}),status=400)
# 		data = json.loads(request.body)
# 		id = data.get('id',None)
# 		if id is not None:
# 			obj = self.get_object_by_id(id)
# 			if obj is None:
# 				return self.render_to_http_response(json.dumps({'msg':'No matched record with specfied id'}),status=404)
# 			json_data = self.serialize([obj,])
# 			return self.render_to_http_response(json_data)
# 		qs = Employee.objects.all()
# 		json_data = self.serialize(qs)
# 		return self.render_to_http_response(json_data)
	
	