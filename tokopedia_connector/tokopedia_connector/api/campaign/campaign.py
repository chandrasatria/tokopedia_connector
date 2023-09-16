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

class Campaign():
	def add_slash_price(app_id,shop_id,token,data):
		url = "https://fs.tokopedia.net/v1/slash-price/fs/"+app_id+"/add?shop_id="+shop_id 
		payload = json.dumps(data)
		headers = {
			'Authorization': 'Bearer '+token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)
		frappe.msgprint(str(response.text))
		frappe.msgprint("slash-price !")

	def update_slash_price(app_id,shop_id,token,data):
		url = "https://fs.tokopedia.net/v1/slash-price/fs/"+app_id+"/update?shop_id="+shop_id
		payload = json.dumps(data)
		headers = {
			'Authorization': 'Bearer '+token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)
		frappe.msgprint(str(response.text))
		frappe.msgprint("update slash-price !")

	def view_campaign_products(app_id,token,product_id,shop_id):
		url = "https://fs.tokopedia.net/v1/campaign/fs/"+app_id+"/view?product_id="+product_id+"&shop_id="+shop_id
		payload={}
		headers = {
	    	'Authorization': 'Bearer '+ token
	    }
		response = requests.request("GET", url, headers=headers, data=payload)
		sp = json.loads(response.text)
		frappe.msgprint(str(sp))

		return sp

	def cancel_slash_price(app_id,shop_id,token,data):
		url = "https://fs.tokopedia.net/v1/slash-price/fs/"+app_id+"/cancel?shop_id="+shop_id
		payload = json.dumps(data)
		headers = {
			'Authorization': 'Bearer '+token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)
		frappe.msgprint(str(response.text))
		frappe.msgprint("cancel slash-price !")

