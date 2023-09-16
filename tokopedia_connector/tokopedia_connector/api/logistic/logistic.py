# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
import requests
from datetime import date
from frappe.utils import flt, rounded, add_months,add_days, nowdate, getdate
import time
import datetime
import subprocess
from Crypto.Cipher import AES
import binascii, os
import base64


@frappe.whitelist()
def get_active_courier(app_id,token,shop_id):
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['*'])
	url = "https://fs.tokopedia.net/v1/logistic/fs/"+app_id+"/active-info?shop_id="+shop_id
	
	payload={}
	headers = {
		'Authorization': 'Bearer '+token
	}
	response = requests.request("GET", url, headers=headers, data=payload)
	courier = json.loads(response.text)
	return courier

@frappe.whitelist()
def get_shipment_info():
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['*'])
	url = "https://fs.tokopedia.net/v2/logistic/fs/"+datas[0]['app_id']+"/info?shop_id="+datas[0]['shop_id']
	payload={}
	headers = {
		'Authorization': 'Bearer '+datas[0]['token']
	}
	response = requests.request("GET", url, headers=headers, data=payload)
	shipment = json.loads(response.text)
	frappe.msgprint(str(shipment))
	# for i in shipment['data']:
	# 	frappe.msgprint(str(i['services']))
	# 	doc = frappe.new_doc('Logistic Tokopedia')
	# 	doc.shipper_id = i['shipper_id']
	# 	doc.shipper_name = i['shipper_name']
	# 	for j in i['services']:
	# 		#frappe.msgprint(str(j))
	# 		row = doc.append('services_logistic', {})
	# 		row.service_id = j['service_id']
	# 		row.service_name = j['service_name']
	# 		row.service_desc = j['service_desc']

	# 	doc.flags.ignore_permission = True
	# 	doc.save()
	# 	frappe.msgprint('Sukses !!')


	# return data_p

@frappe.whitelist()
def get_all_variants():
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['*'])
	url = "https://fs.tokopedia.net/inventory/v2/fs/"+datas[0]['app_id']+"/category/get_variant?cat_id=3412"
	
	payload={}
	headers = {
		'Authorization': 'Bearer '+datas[0]['token']
	}
	response = requests.request("GET", url, headers=headers, data=payload)
	variant = json.loads(response.text)
	frappe.msgprint(str(variant))