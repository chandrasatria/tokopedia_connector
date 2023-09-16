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

class Shop():
	def get_shop(app_id,token):
		url = "https://fs.tokopedia.net/v1/shop/fs/"+app_id+"/shop-info"
		payload={}
		headers = {
			'Authorization': 'Bearer '+token
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		datatest = json.loads(response.text)

		return datatest

	def gen_token(basic_base_64):
		url_t = "https://accounts.tokopedia.com/token?grant_type=client_credentials"
		payload_t ={}
		headers_t = {
			'Authorization': 'Basic '+basic_base_64,
	  	  	'Content-Length': '0',
	    	'User-Agent': 'PostmanRuntime/7.17.1'
		}
		response_t = requests.request("POST", url_t, headers=headers_t, data=payload_t)
		tokens = json.loads(response_t.text)
		frappe.msgprint(str(tokens))
		return tokens

@frappe.whitelist()
def gen_token2(basic_base_64):
		url_t = "https://accounts.tokopedia.com/token?grant_type=client_credentials"
		payload_t ={}
		headers_t = {
			'Authorization': 'Basic '+basic_base_64,
	  	  	'Content-Length': '0',
	    	'User-Agent': 'PostmanRuntime/7.17.1'
		}
		response_t = requests.request("POST", url_t, headers=headers_t, data=payload_t)
		tokens = json.loads(response_t.text)

		return tokens



