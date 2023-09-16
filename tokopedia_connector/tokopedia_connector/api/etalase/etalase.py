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

class Etalase():
	def get_all_etalase(app_id,shop_id,token):
		url = "https://fs.tokopedia.net/inventory/v1/fs/"+app_id+"/product/etalase?shop_id="+shop_id
		payload={}
		headers = {
			'Authorization': 'Bearer '+ token
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		etalse = json.loads(response.text)

		return etalse