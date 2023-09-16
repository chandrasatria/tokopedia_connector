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

class Order():
	
	def coba():
		frappe.msgprint("On Update Coba !")
		
	def get_all_order2(app_id,shop_id,token,strtime_from,strtime_to):
		#url = "https://fs.tokopedia.net/v1/fs/"+app_id+"/fulfillment_order"
		url = "https://fs.tokopedia.net/v2/order/list?fs_id="+app_id+"&shop_id="+shop_id+"&from_date="+ strtime_from +"&to_date="+ strtime_to +"&page=1&per_page=1000"
		payload={}
		headers = {
		  'Authorization': 'Bearer '+ token
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		datao = json.loads(response.text)
		# frappe.msgprint(str(datao))

		return datao

	def get_all_order(app_id,token):
		url = "https://fs.tokopedia.net/v1/fs/"+app_id+"/fulfillment_order"
		#url = "https://fs.tokopedia.net/v2/order/list?fs_id="+i['app_id']+"&shop_id="+i['shop_id']+"&from_date="+ strtime_from +"&to_date="+ strtime_to +"&page=1&per_page=10"
		payload={}
		headers = {
		  'Authorization': 'Bearer '+ token
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		datao = json.loads(response.text)
		frappe.msgprint(str(datao))
		
		return datao

	def get_singgle_order(app_id,token,order_id):
		urlsave = "https://fs.tokopedia.net/v2/fs/"+app_id+"/order?order_id=" + order_id
		#urlsave = "https://fs.tokopedia.net/v2/fs/"+app_id+"/order?order_id=" + str(x)
		payloadssave={}
		headers = {
  			'Authorization': 'Bearer '+ token
		}
		r = requests.request("GET", urlsave, headers=headers, data=payloadssave)
		datasave = json.loads(r.text)
		# frappe.msgprint(str(datasave))
		return datasave



