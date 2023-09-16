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

class Price():
	def update_price(app_id,shop_id,token,data):
		url = "https://fs.tokopedia.net/inventory/v1/fs/"+app_id+"/price/update?shop_id="+shop_id
		payload = json.dumps(data)
		headers = {
			'Authorization': 'Bearer '+token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)
		# frappe.msgprint("Update Harga Berhasil !")

	def update_stock(app_id,shop_id,token,data):
		url = "https://fs.tokopedia.net/inventory/v1/fs/"+app_id+"/stock/update?shop_id="+shop_id
		payload = json.dumps(data)
		headers = {
			'Authorization': 'Bearer '+token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		# print(response.text)
		data = json.loads(response.text)
		# frappe.msgprint(str(data['data']['succeed_rows_data'][0]['shopID']))
		if data['header']['messages'] == "Your request has been processed successfully" :
			dataToko = frappe.get_value('Tokopedia Setting', {'shop_id': data['data']['succeed_rows_data'][0]['shopID']}, ["name"])
			shop_name = dataToko
			result_print = ("update Stock Tokopedia di toko <b> {} </b> berhasil!".format(shop_name))

			return result_print