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
# from frappe import _



class Product():
	def delete_product2(app_id,shop_id,product_id,shop):
		# frappe.throw(_("Apakah anda yakin ??"))
		# frappe.throw("Apakah anda yaki ??")
		token = frappe.get_value("Tokopedia Setting",{"name": shop}, "token")
		url = "https://fs.tokopedia.net/v3/products/fs/"+app_id+"/delete?shop_id="+shop_id
		payload =json.dumps({
					"product_id": [int(product_id)]
				})
		headers = {
			'Authorization': 'Bearer '+token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)

		frappe.msgprint(str(response.text))
	
	def get_all_product_shop(app_id,token,shop_id,page):
		url = "https://fs.tokopedia.net/inventory/v1/fs/"+app_id+"/product/info?shop_id="+shop_id+"&page="+str(page)+"&per_page=50"
		payload={}
		headers = {
	    	'Authorization': 'Bearer '+ token
	    }
		r_product = requests.request("GET", url, headers=headers, data=payload)
		data_p = json.loads(r_product.text)
		# frappe.msgprint(str(data_p['data']))

		return data_p

	def get_all_product(app_id,token):
		url = "https://fs.tokopedia.net/v2/products/fs/"+app_id+"/1/10000"
		payload={}
		headers = {
	    	'Authorization': 'Bearer '+ token
	    }
		r_product = requests.request("GET", url, headers=headers, data=payload)
		data_p = json.loads(r_product.text)
		frappe.msgprint(str(data_p))

		return data_p

	def get_product_info(app_id,product_id,token):
		url = "https://fs.tokopedia.net/inventory/v1/fs/"+app_id+"/product/info?product_id="+product_id
		payload={}
		headers = {
				'Authorization': 'Bearer '+token
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		detail_p = json.loads(response.text)
		frappe.msgprint(str(detail_p))
		
		return detail_p

	def get_product_info_sku(app_id,item,token):
		url = "https://fs.tokopedia.net/inventory/v1/fs/"+app_id+"/product/info?sku="+item
		payload={}
		headers = {
			'Authorization': 'Bearer '+ token
		}
		r_product = requests.request("GET", url, headers=headers, data=payload)
		data_p = json.loads(r_product.text)
		return data_p

	def edit_product(app_id,shop_id,data,token):
		url = "https://fs.tokopedia.net/v2/products/fs/"+app_id+"/edit?shop_id="+shop_id
		payload =json.dumps({
					"products": data
				})
		headers = {
			'Authorization': 'Bearer '+token,
			'Content-Type': 'application/json'
		}
		response = requests.request("PATCH", url, headers=headers, data=payload)
		print(response.text)
		frappe.msgprint(str(response.text))

	def create_product(app_id,shop_id,data,token):
		url = "https://fs.tokopedia.net/v3/products/fs/"+app_id+"/create?shop_id="+shop_id
		payload =json.dumps({
					"products": data
				})
		headers = {
			'Authorization': 'Bearer '+token,
			'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		

		frappe.msgprint(str(response.text))
		hasil = json.loads(response.text) 
		
		return hasil
		# print(response.text)
		#frappe.msgprint("create data berhasil !")


	def get_all_variants(cat):
		datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['*'])
		url = "https://fs.tokopedia.net/inventory/v2/fs/"+datas[0]['app_id']+"/category/get_variant?cat_id="+str(cat)
		# "https://fs.tokopedia.net/inventory/v2/fs/"+datas[0]['app_id']+"/category/get_variant?cat_id="+cat
		# "https://fs.tokopedia.net/inventory/v1/fs/"+datas[0]['app_id']+"/category/get_variant?cat_id="+cat
		#"https://fs.tokopedia.net/inventory/v2/fs/15209/category/get_variant?cat_id=3412"
		# https://fs.tokopedia.net/inventory/v1/fs/15209/category/get_variant?cat_id=1769
		# c:f3jX5CIzSTm7gdbrTL1wEQ
		payload={}
		headers = {
			'Authorization': 'Bearer '+datas[0]['token']
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		variant = json.loads(response.text)
		
		# frappe.msgprint("test"+str(variant))
		#frappe.msgprint("test"+response.text)
		
		return variant

	def get_all_variants_v1(cat):
		datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['*'])
		url = "https://fs.tokopedia.net/inventory/v1/fs/"+datas[0]['app_id']+"/category/get_variant?cat_id="+cat
		payload={}
		headers = {
			'Authorization': 'Bearer '+datas[0]['token']
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		variant = json.loads(response.text)
		
		# frappe.msgprint("test"+str(variant))
		
		return variant
		

	def get_all_variants_by_idproduct(app_id,product_id,token):
		datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['*'])
		url = "https://fs.tokopedia.net/inventory/v1/fs/"+app_id+"/product/variant/"+str(product_id)
		payload={}
		headers = {
			'Authorization': 'Bearer '+token
		}
		response = requests.request("GET", url, headers=headers, data=payload)
		variant = json.loads(response.text)
		## frappe.msgprint(str(variant))
		return variant
		

@frappe.whitelist()
def get_product_annotation(cat):
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['*'])
	url = "https://fs.tokopedia.net/v1/fs/"+datas[0]['app_id']+"/product/annotation?cat_id="+cat
	
	payload={}
	headers = {
		'Authorization': 'Bearer '+datas[0]['token']
	}
	response = requests.request("GET", url, headers=headers, data=payload)
	annotation = json.loads(response.text)
	# data=[]
	# for i in annotation['data']:
	# 	data.append(i['variant'])
	# frappe.msgprint(str(annotation))
	return annotation

@frappe.whitelist()
def variant_item(item_parent):
	get_var = frappe.db.get_list('Item Variant Attribute',filters={'parent': item_parent},fields=['*'])
	data=[]
	data2=[]
	for i in get_var:
		get_val = frappe.db.get_list('Item Attribute Value',filters={'parent': i['attribute']},fields=['*'])
		for j in get_val:
			data.append(j['abbr']+'|'+j['attribute_value'])
			if len(data) == len(get_val):
				data2.append(data)
				data=[]
	
	return get_var,data2

@frappe.whitelist()
def delete_product(app_id,shop_id,product_id,shop):
	# frappe.throw(_("Apakah anda yakin ??"))
	# frappe.throw("Apakah anda yaki ??")
	token = frappe.get_value("Tokopedia Setting",{"name": shop}, "token")
	url = "https://fs.tokopedia.net/v3/products/fs/"+app_id+"/delete?shop_id="+shop_id
	payload =json.dumps({
				"product_id": [int(product_id)]
			})
	headers = {
		'Authorization': 'Bearer '+token,
		'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	# name = frappe.get_value("Marketplace Item Tokopedia",{"product_id": product_id}, "name")
	# doc = frappe.get_doc("Marketplace Item Tokopedia",name)
	# doc.product_id =""
	
	# doc.flags.ignore_permission=True
	# doc.save()

	frappe.msgprint(str(response.text))