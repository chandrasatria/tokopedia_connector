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
from tokopedia_connector.tokopedia_connector.api.order.order import Order
from tokopedia_connector.tokopedia_connector.api.product.product import Product
from tokopedia_connector.tokopedia_connector.api.etalase.etalase import Etalase
from tokopedia_connector.tokopedia_connector.api.price.price import Price


class Tokopedia():
	@frappe.whitelist()
	def crate_product2_coba(item_code,data_item):
		#frappe.msgprint("test Lutfi")
		data_i = frappe.db.get_list('Item',filters={'name': item_code},fields=['*'])
		# data_item = json.loads(data_item)
		token = frappe.get_value("Tokopedia Setting",{"name": data_item['shop']}, "token")
		data = []
		for i in data_i:
			price= frappe.get_value("Item Price",{"item_code": i['item_code']}, "price_list_rate")
			stock= frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
			images=[]

			img = {
				"file_path": frappe.utils.get_url()+i['gambar_utama']
			}

			images.append(img)

			if i['gambar_depan']:
				img1 = {
					"file_path": frappe.utils.get_url()+i['gambar_depan']
				}
				images.append(img1)

			if i['gambar_atas']:
				img2 = {
					"file_path": frappe.utils.get_url()+i['gambar_atas']
				}
				images.append(img2)
			

			if i['gambar_samping']:
				img3 = {
					"file_path": frappe.utils.get_url()+i['gambar_samping']
				}
				images.append(img3)
			
			if i['gambar_detail']:
				img4 = {
					"file_path": frappe.utils.get_url()+i['gambar_detail']
				}
				images.append(img4)

			frappe.msgprint(str(images))

			isi ={
							"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
							"condition": data_item['condition'],
							"description": i['description'],
							"sku": data_item['sku'], #tidak boleh ada spasi
							"price": int(price),
							"status": data_item['status'],
							"stock": int(stock),
							"min_order": data_item['min_order'],
							"category_id": data_item['category_id'],
							"price_currency": data_item['price_currency'],
							"weight": int(i['weight_per_unit']),
							"weight_unit": i['weight_uom'],
							"is_free_return": data_item['is_free_return'],
							"is_must_insurance": data_item['is_must_insurance'],
							"dimension": {
								"height": float(i['height']),
								"width":  float(i['width']),
								"length":  float(i['length'])
							},
							"custom_product_logistics": data_item['custom_product_logistics'],
							"annotations": data_item['annotations'],
							"etalase": data_item['etalase'],
							"pictures": images,
							"wholesale": [],
							"preorder": {},
							"videos": []
						}
			data.append(isi)
			
			test = Product.create_product(data_item['app_id'],data_item['shop_id'],data,token)
			# frappe.msgprint(str(test['data']['success_rows_data'][0]['product_id']))
			name = frappe.get_value("Marketplace Item Tokopedia",{"shop": data_item['shop'],"item_code": item_code}, "name")
			frappe.msgprint(name)
			doc = frappe.get_doc("Marketplace Item Tokopedia",name)
			doc.product_id = test['data']['success_rows_data'][0]['product_id']
			
			doc.flags.ignore_permission=True
			doc.save()
			frappe.msgprint("Cretae data berhasil !")	

	@frappe.whitelist()
	def edit_product_coba(item_code,data_item):
		frappe.msgprint(str(data_item))
		data_i = frappe.db.get_list('Item',filters={'name': item_code},fields=['*'])
		# data_item = json.loads(data_item)
		token = frappe.get_value("Tokopedia Setting",{"name": data_item['shop']}, "token")
		frappe.msgprint(str(data_i))
		data = []
		for i in data_i:
			price= frappe.get_value("Item Price",{"item_code": i['item_code']}, "price_list_rate")
			stock= frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
			images=[]

			img = {
				"file_path": frappe.utils.get_url()+i['gambar_utama']
			}

			images.append(img)

			if i['gambar_depan']:
				img1 = {
					"file_path": frappe.utils.get_url()+i['gambar_depan']
				}
				images.append(img1)

			if i['gambar_atas']:
				img2 = {
					"file_path": frappe.utils.get_url()+i['gambar_atas']
				}
				images.append(img2)
			

			if i['gambar_samping']:
				img3 = {
					"file_path": frappe.utils.get_url()+i['gambar_samping']
				}
				images.append(img3)
			
			if i['gambar_detail']:
				img4 = {
					"file_path": frappe.utils.get_url()+i['gambar_detail']
				}
				images.append(img4)

			frappe.msgprint(str(images))
			


			isi ={
					"id": data_item['product_id'],
					"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
					"condition": data_item['condition'],
					"description": i['description'],
					"sku": data_item['sku'], #tidak boleh ada spasi
					"price": int(price),
					"status": data_item['status'],
					"stock": int(stock),
					"min_order": data_item['min_order'],
					"category_id": data_item['category_id'],
					"price_currency": data_item['price_currency'],
					"weight": int(i['weight_per_unit']),
					"weight_unit": i['weight_uom'],
					"is_free_return": data_item['is_free_return'],
					"is_must_insurance": data_item['is_must_insurance'],
					"dimension": {
						"height": float(i['height']),
						"width":  float(i['width']),
						"length":  float(i['length'])
					},
					"custom_product_logistics": data_item['custom_product_logistics'],
					"annotations": data_item['annotations'],
					"etalase": data_item['etalase'],
					"pictures": images,
					"wholesale": [],
					"preorder": {},
					"videos": []
				}
			data.append(isi)
			
			Product.edit_product(data_item['app_id'],data_item['shop_id'],data,token)
			frappe.msgprint("edit data berhasil !")	
		

@frappe.whitelist()
def get_etalase():
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['app_id','shop_name','token','shop_id'])
	url = "https://fs.tokopedia.net/inventory/v1/fs/15209/product/etalase?shop_id="+datas[0]['shop_id']
	payload={}
	headers = {
		'Authorization': 'Bearer '+ datas[0]['token']
	}
	response = requests.request("GET", url, headers=headers, data=payload)
	etalse = json.loads(response.text)
	return(etalse)

@frappe.whitelist()
def get_etalase2(app_id,shop_id,token):
	frappe.msgprint("bisaaaa etlasse")
	etalse = Etalase.get_all_etalase(app_id,shop_id,token)
	for i in etalse['data']['etalase']:
		get_e = frappe.get_value("List Etalase",{"name" : i['etalase_id']}, "name")
		if get_e:
			frappe.msgprint("Etalase "+i['etalase_name']+" Sudah ada")
		else:
			doc = frappe.new_doc('List Etalase')
			doc.id = i['etalase_id']
			doc.etalase = i['etalase_name']
			doc.name_shop = etalse['data']['shop']['name']

			doc.flags.ignore_permission = True
			doc.save()
			frappe.msgprint(i['etalase_name']+"Sudah DItambahkan !")



@frappe.whitelist()
def get_cat_manual():
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['app_id','shop_name','token','shop_id'])
	datac =frappe.db.get_list('List Category Tokopedia',filters={'docstatus': '0'},fields=['keyword'])
	#datac[0]['keyword']
	#doc = frappe.new_doc('Item')
	url = "https://fs.tokopedia.net/inventory/v1/fs/"+datas[0]['app_id']+"/product/category"
	payload={}
	headers = {
		'Authorization': 'Bearer '+ datas[0]['token']
	}
	response = requests.request("GET", url, headers=headers, data=payload)
	cat = json.loads(response.text)
	return(cat)

@frappe.whitelist()
def get_cat_manual2():
	frappe.msgprint("bisa")
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['app_id','shop_name','token','shop_id'])
	datac =frappe.db.get_list('List Category Tokopedia',filters={'docstatus': '0'},fields=['*'])
	#datac[0]['keyword']
	#doc = frappe.new_doc('Item')
	url = "https://fs.tokopedia.net/inventory/v1/fs/"+datas[0]['app_id']+"/product/category"
	payload={}
	headers = {
		'Authorization': 'Bearer '+ datas[0]['token']
	}
	response = requests.request("GET", url, headers=headers, data=payload)
	cat = json.loads(response.text)
	# frappe.msgprint(str(cat))
	data = []
	data = cat['data']['categories']
	for j in range(28):
		try:
			data2 = data[j]['child']
			# list child
			for i in data2:
					if i['child']:
						for j in i['child']:
							doc = frappe.get_doc("Child Tokopedia",i['id'])
							row = doc.append('list_child', {})
							row.id= j['id']
							row.child_name= j['name']

							doc.flags.ignore_permission = True
							doc.save()
		except:
			print("An exception occurred")
				
	# # child 1
	# for j in range(28):
	# 	try:
	# 		for i in data[j]['child']:
	# 			doc = frappe.new_doc('Child Tokopedia')
	# 			doc.id_parent = data[j]['id']
	# 			doc.id = i['id']
	# 			doc.name_child = i['name']
				
	# 			doc.flags.ignore_permission = True
	# 			doc.save()
	# 	except:
	# 		print("An exception occurred")
	
	#induk
	# for i in cat['data']['categories']:
	# 	doc = frappe.new_doc('List Category Tokopedia')
	# 	doc.id = i['id']
	# 	doc.kategori = i['name']
		
	# 	doc.flags.ignore_permission = True
	# 	doc.save()

	


@frappe.whitelist()
def get_cat():
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['app_id','shop_name','token','shop_id'])
	#datac =frappe.db.get_list('List Category Tokopedia',filters={'docstatus': '0'},fields=['keyword'])
	#datac[0]['keyword']
	doc = frappe.new_doc('Item')
	url = "https://fs.tokopedia.net/inventory/v1/fs/"+datas[0]['app_id']+"/product/category?keyword=%"+doc.keyword+"%"
	payload={}
	headers = {
		'Authorization': 'Bearer '+ datas[0]['token']
	}
	response = requests.request("GET", url, headers=headers, data=payload)
	cat = json.loads(response.text)
	return(cat)

@frappe.whitelist()
def gen_token():
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['name','basic_base_64'])
	for i in datas:
		url = "https://accounts.tokopedia.com/token?grant_type=client_credentials"
		payload={}
		headers = {
			'Authorization': 'Basic '+i['basic_base_64'],
	  	  	'Content-Length': '0',
	    	'User-Agent': 'PostmanRuntime/7.17.1'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		tokens = json.loads(response.text)
		get_token = frappe.get_doc("Tokopedia Setting",i['name'])
		get_token.token = tokens['access_token']
		
		get_token.flags.ignore_permission = True
		get_token.save()

@frappe.whitelist()
def get_data_manual(date):
	frappe.msgprint("coba")
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['app_id','shop_name','token','shop_id'])
	for i in datas:
		app_id = i['app_id']
		token = i['token']
		shop_id = i['shop_id']
		shop_name= i['shop_name']
		# today = date.today()
		back_date = str(add_days(date, -2))
		start_date = str(add_days(date, 1))
		from_date = back_date+ " 00:00:00"
		to_date = start_date+ " 00:00:00"
		time_from = int(time.mktime(datetime.datetime.strptime(str(from_date), "%Y-%m-%d %H:%M:%S").timetuple()))
		time_to = int(time.mktime(datetime.datetime.strptime(str(to_date), "%Y-%m-%d %H:%M:%S").timetuple()))
		strtime_from = str(time_from)
		strtime_to = str(time_to)
		datao = Order.get_all_order2(app_id,shop_id,token,strtime_from,strtime_to)
		# datao = Order.get_all_order(app_id,token)
		# order = ['349489530','831754337','819122178','788797562','868426373','868416432']
		if datao['data']:
			frappe.msgprint("data o ada isinya")
			for x in datao['data']:
			# for x in datao['data']['order_data']:
				get_order = frappe.get_value("Tokopedia Orders",{"name" : str(x['order_id'])}, "name")
				datasave = Order.get_singgle_order(app_id,token,str(x['order_id']))
				# get_order = frappe.get_value("Tokopedia Orders",{"name" : str(x['order']['order_id'])}, "name")
				# datasave = Order.get_singgle_order(app_id,token,str(x['order']['order_id']))
				if get_order :
					doc = frappe.get_doc("Tokopedia Orders",get_order)
					status = datasave['data']['order_status']
					doc.days_to_ship = datasave['data']['order_info']['delivered_age_day']
					# doc.customer_email = data_c['buyer_info']['buyer_email']
					doc.tracking_no = datasave['data']['order_info']['shipping_info']['awb']
					if status == 0:
						doc.order_status = 'Seller cancel order'
					if status == 5:
						doc.order_status = 'Order Canceled by Fraud'
					if status == 10:
						doc.order_status = 'Order Pending Replacement'
					if status == 100:
						doc.order_status = 'Pending order'
					if status == 103:
						doc.order_status = 'Wait for payment confirmation from third party'
					if status == 220:
						doc.order_status = 'Payment verified, order ready to process'
					if status == 400:
						doc.order_status = 'Seller accept order'
					if status == 450:
						doc.order_status = 'Waiting for pickup'
					if status == 500:
						doc.order_status = 'Order shipment'
					if status == 520:
						doc.order_status = 'Invalid shipment reference number (AWB)'
					if status == 600:
						doc.order_status = 'Order delivered'
					if status == 700:
						doc.order_status = 'Order finished'

					# berrat
					total_weight = []
					total_asuransi = []
					for w in  datasave['data']['order_info']['order_detail']:
						total_weight.append(w['total_weight'])
						total_asuransi.append(w['insurance_price'])

					doc.total_weight = sum(total_weight)
					
					for t in datasave['data']['order_info']['order_history']:
						if t['hist_status_code'] == 500:
							driver=t['comment']
							name = driver.split("\n")
							pengambil = name[1].split(":")
							doc.pengambil = pengambil[1]

							doc.flags.ignore_permission = True
							doc.save()

					doc.flags.ignore_permission = True
					doc.save()

					order_id_so = frappe.get_value("Tokopedia Orders",{"name" : get_order}, "name")
					toko = frappe.get_value("Tokopedia Orders",{"name" : get_order}, "shop_name")
					cek_sinv = frappe.get_value("Tokopedia Setting",{"name" : toko}, "make_sinv")
					if order_id_so:
						if cek_sinv == 0 and status == 400:
							frappe.msgprint("bikn dn nih.")
							make_dn(order_id_so)
				else :
					doc = frappe.new_doc('Tokopedia Orders')
					#doc.order_id = str(x['order']['order_id'])
					doc.order_id = datasave['data']['order_id']
					doc.marketplace = "Tokopedia"
					doc.shop_name = shop_name
					status = datasave['data']['order_status']
					if status == 0:
						doc.order_status = 'Seller cancel order'
					if status == 5:
						doc.order_status = 'Order Canceled by Fraud'
					if status == 10:
						doc.order_status = 'Order Pending Replacement'
					if status == 100:
						doc.order_status = 'Pending order'
					if status == 103:
						doc.order_status = 'Wait for payment confirmation from third party'
					if status == 220:
						doc.order_status = 'Payment verified, order ready to process'
					if status == 400:
						doc.order_status = 'Seller accept order'
					if status == 450:
						doc.order_status = 'Waiting for pickup'
					if status == 500:
						doc.order_status = 'Order shipment'
					if status == 520:
						doc.order_status = 'Invalid shipment reference number (AWB)'
					if status == 600:
						doc.order_status = 'Order delivered'
					if status == 700:
						doc.order_status = 'Order finished'

					doc.days_to_ship = datasave['data']['order_info']['delivered_age_day']
					doc.customer = datasave['data']['buyer_info']['buyer_id']
					doc.recipient_city = datasave['data']['order_info']['destination']['address_city']
					item = frappe.get_list("Tokopedia Orders Item",{"parent" : get_order},"parent")

					if len(item) == 0 :
						for i in datasave['data']['order_info']['order_detail']:
							row = doc.append('items', {})
							# if '-' in i['product_name']:
							# 	name = i['product_name'].split("-")
							# 	variant = i['product_name'].split("-")
							# 	row.item_name = name[0]
							# 	row.variant = variant[1]
							# else :
							# 	row.item_name = i['product_name']
							row.item_name = i['product_name']
							row.variant = i['product_name']
							row.item_sku = i['sku']
							row.qty = i['quantity']
							row.price_list_rate= i['product_price']
							row.rate = i['subtotal_price']

					if datasave['data']['promo_order_detail']['summary_promo'] :
						for p in datasave['data']['promo_order_detail']['summary_promo']:
							get_promo = frappe.get_value("List Promo",{"name1" : p['name'],"parent" : get_order}, "name1")
							if get_promo:
								frappe.msgprint("Promo Name Sudah ada")
							else :
								row = doc.append('list_promo', {})
								row.name1=p['name']
								row.type=p['type']
								row.cashback_points=p['cashback_points']
								row.cashback_amount=p['cashback_amount']

					doc.total_cashback= datasave['data']['promo_order_detail']['total_cashback']
					doc.currency = "IDR"
					doc.total_amount = datasave['data']['item_price']
					doc.shipping_carrier = datasave['data']['order_info']['shipping_info']['logistic_name']
					doc.estimated_shipping_fee = datasave['data']['order_info']['shipping_info']['shipping_price']
					doc.insurance_price = datasave['data']['order_info']['shipping_info']['insurance_price']
					doc.voucher_applied = datasave['data']['payment_info']['voucher_code']
					doc.additional_discount = datasave['data']['payment_info']['discount_amount']
					doc.tracking_no = datasave['data']['order_info']['shipping_info']['awb']
					#doc.grand_total = int(datasave['data']['order_info']['shipping_info']['shipping_price']) + int(datasave['data']['item_price']) - int(datasave['data']['payment_info']['discount_amount'])

					# # encrypt
					secret = datasave['data']['encryption']['secret']
					content = datasave['data']['encryption']['content']
					subprocess.call(["/home/frappe/ahok-bench/rsa/decrypt-secret.sh"]+['/home/frappe/ahok-bench/id_rsa']+[secret]+['/home/frappe/ahok-bench/rsa/key'])
					key = open("/home/frappe/ahok-bench/rsa/key").read()
					secretKey = key.encode('ascii')
					bcontent = base64.b64decode(content)
					bnonce = bcontent[len(bcontent) - 12:len(bcontent)]
					bcipher = bcontent[0:len(bcontent) - 12]
					taglength = 16
					tag = bcipher[len(bcipher) - taglength : len(bcipher)]
					acipher = bcipher[0 : len(bcipher) - taglength]
					aesCipher = AES.new(secretKey, AES.MODE_GCM, bnonce)
					plaintext = aesCipher.decrypt_and_verify(acipher, tag)
					data_c = json.loads(plaintext)
					doc.customer_name = data_c['buyer_info']['buyer_fullname']
					doc.customer_phone =data_c['buyer_info']['buyer_phone']
					doc.nama_penerima = data_c['order_info']['destination']['receiver_name']
					doc.recipient_phone = data_c['order_info']['destination']['receiver_phone']
					alamat = data_c['order_info']['destination']['address_street']+' '+datasave['data']['order_info']['destination']['address_city']+', '+datasave['data']['order_info']['destination']['address_district']+', '+datasave['data']['order_info']['destination']['address_postal']+', '+datasave['data']['order_info']['destination']['address_province']
					doc.recipient_address = alamat

					total_weight = []
					total_asuransi = []
					for w in  datasave['data']['order_info']['order_detail']:
						total_weight.append(w['total_weight'])
						total_asuransi.append(w['insurance_price'])

					doc.total_weight = sum(total_weight)

					for t in datasave['data']['order_info']['order_history']:
						if t['hist_status_code'] == 100:
							tanggal =t['timestamp']

					tgl = tanggal[0:10]
					doc.tanggal_pesan = tgl

					doc.flags.ignore_permission = True
					doc.save()

					order_id_so = frappe.get_value("Tokopedia Orders",{"name" : str(datasave['data']['order_id'])}, "name")
					toko = frappe.get_value("Tokopedia Orders",{"name" : str(datasave['data']['order_id'])}, "shop_name")
					cek_sinv = frappe.get_value("Tokopedia Setting",{"name" : toko}, "make_sinv")
					if order_id_so:
						if cek_sinv == 0 and status == 220:
							frappe.msgprint("bikn so nih.")
							make_so(order_id_so)
						if cek_sinv == 1 and status == 220:
							frappe.msgprint("bikn sinv nih.")
							confirm_order_sinv(order_id_so)
							make_sinv(order_id_so)

@frappe.whitelist()
def get_data():
	frappe.msgprint("coba")
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['app_id','shop_name','token','shop_id'])
	for i in datas:
		app_id = i['app_id']
		token = i['token']
		shop_id = i['shop_id']
		shop_name= i['shop_name']
		today = date.today()
		back_date = str(add_days(today, -2))
		start_date = str(add_days(today, 1))
		from_date = back_date+ " 00:00:00"
		to_date = start_date+ " 00:00:00"
		time_from = int(time.mktime(datetime.datetime.strptime(str(from_date), "%Y-%m-%d %H:%M:%S").timetuple()))
		time_to = int(time.mktime(datetime.datetime.strptime(str(to_date), "%Y-%m-%d %H:%M:%S").timetuple()))
		strtime_from = str(time_from)
		strtime_to = str(time_to)
		datao = Order.get_all_order2(app_id,shop_id,token,strtime_from,strtime_to)
		# datao = Order.get_all_order(app_id,token)
		# order = ['349489530','831754337','819122178','788797562','868426373','868416432']
		if datao['data']:
			frappe.msgprint("data o ada isinya")
			for x in datao['data']:
			# for x in datao['data']['order_data']:
				get_order = frappe.get_value("Tokopedia Orders",{"name" : str(x['order_id'])}, "name")
				datasave = Order.get_singgle_order(app_id,token,str(x['order_id']))
				# get_order = frappe.get_value("Tokopedia Orders",{"name" : str(x['order']['order_id'])}, "name")
				# datasave = Order.get_singgle_order(app_id,token,str(x['order']['order_id']))
				if get_order :
					doc = frappe.get_doc("Tokopedia Orders",get_order)
					status = datasave['data']['order_status']
					doc.days_to_ship = datasave['data']['order_info']['delivered_age_day']
					# doc.customer_email = data_c['buyer_info']['buyer_email']
					doc.tracking_no = datasave['data']['order_info']['shipping_info']['awb']
					if status == 0:
						doc.order_status = 'Seller cancel order'
					if status == 5:
						doc.order_status = 'Order Canceled by Fraud'
					if status == 10:
						doc.order_status = 'Order Pending Replacement'
					if status == 100:
						doc.order_status = 'Pending order'
					if status == 103:
						doc.order_status = 'Wait for payment confirmation from third party'
					if status == 220:
						doc.order_status = 'Payment verified, order ready to process'
					if status == 400:
						doc.order_status = 'Seller accept order'
					if status == 450:
						doc.order_status = 'Waiting for pickup'
					if status == 500:
						doc.order_status = 'Order shipment'
					if status == 520:
						doc.order_status = 'Invalid shipment reference number (AWB)'
					if status == 600:
						doc.order_status = 'Order delivered'
					if status == 700:
						doc.order_status = 'Order finished'

					# berrat
					total_weight = []
					total_asuransi = []
					for w in  datasave['data']['order_info']['order_detail']:
						total_weight.append(w['total_weight'])
						total_asuransi.append(w['insurance_price'])

					doc.total_weight = sum(total_weight)
					
					for t in datasave['data']['order_info']['order_history']:
						if t['hist_status_code'] == 500:
							driver=t['comment']
							name = driver.split("\n")
							pengambil = name[1].split(":")
							doc.pengambil = pengambil[1]

							doc.flags.ignore_permission = True
							doc.save()

					doc.flags.ignore_permission = True
					doc.save()

					order_id_so = frappe.get_value("Tokopedia Orders",{"name" : get_order}, "name")
					toko = frappe.get_value("Tokopedia Orders",{"name" : get_order}, "shop_name")
					cek_sinv = frappe.get_value("Tokopedia Setting",{"name" : toko}, "make_sinv")
					if order_id_so:
						if cek_sinv == 0 and status == 400:
							frappe.msgprint("bikn dn nih.")
							make_dn(order_id_so)
				else :
					doc = frappe.new_doc('Tokopedia Orders')
					#doc.order_id = str(x['order']['order_id'])
					doc.order_id = datasave['data']['order_id']
					doc.marketplace = "Tokopedia"
					doc.shop_name = shop_name
					status = datasave['data']['order_status']
					if status == 0:
						doc.order_status = 'Seller cancel order'
					if status == 5:
						doc.order_status = 'Order Canceled by Fraud'
					if status == 10:
						doc.order_status = 'Order Pending Replacement'
					if status == 100:
						doc.order_status = 'Pending order'
					if status == 103:
						doc.order_status = 'Wait for payment confirmation from third party'
					if status == 220:
						doc.order_status = 'Payment verified, order ready to process'
					if status == 400:
						doc.order_status = 'Seller accept order'
					if status == 450:
						doc.order_status = 'Waiting for pickup'
					if status == 500:
						doc.order_status = 'Order shipment'
					if status == 520:
						doc.order_status = 'Invalid shipment reference number (AWB)'
					if status == 600:
						doc.order_status = 'Order delivered'
					if status == 700:
						doc.order_status = 'Order finished'

					doc.days_to_ship = datasave['data']['order_info']['delivered_age_day']
					doc.customer = datasave['data']['buyer_info']['buyer_id']
					doc.recipient_city = datasave['data']['order_info']['destination']['address_city']
					item = frappe.get_list("Tokopedia Orders Item",{"parent" : get_order},"parent")

					if len(item) == 0 :
						for i in datasave['data']['order_info']['order_detail']:
							row = doc.append('items', {})
							# if '-' in i['product_name']:
							# 	name = i['product_name'].split("-")
							# 	variant = i['product_name'].split("-")
							# 	row.item_name = name[0]
							# 	row.variant = variant[1]
							# else :
							# 	row.item_name = i['product_name']
							row.item_name = i['product_name']
							row.variant = i['product_name']
							row.item_sku = i['sku']
							row.qty = i['quantity']
							row.price_list_rate= i['product_price']
							row.rate = i['subtotal_price']

					if datasave['data']['promo_order_detail']['summary_promo'] :
						for p in datasave['data']['promo_order_detail']['summary_promo']:
							get_promo = frappe.get_value("List Promo",{"name1" : p['name'],"parent" : get_order}, "name1")
							if get_promo:
								frappe.msgprint("Promo Name Sudah ada")
							else :
								row = doc.append('list_promo', {})
								row.name1=p['name']
								row.type=p['type']
								row.cashback_points=p['cashback_points']
								row.cashback_amount=p['cashback_amount']

					doc.total_cashback= datasave['data']['promo_order_detail']['total_cashback']
					doc.currency = "IDR"
					doc.total_amount = datasave['data']['item_price']
					doc.shipping_carrier = datasave['data']['order_info']['shipping_info']['logistic_name']
					doc.estimated_shipping_fee = datasave['data']['order_info']['shipping_info']['shipping_price']
					doc.insurance_price = datasave['data']['order_info']['shipping_info']['insurance_price']
					doc.voucher_applied = datasave['data']['payment_info']['voucher_code']
					doc.additional_discount = datasave['data']['payment_info']['discount_amount']
					doc.tracking_no = datasave['data']['order_info']['shipping_info']['awb']
					#doc.grand_total = int(datasave['data']['order_info']['shipping_info']['shipping_price']) + int(datasave['data']['item_price']) - int(datasave['data']['payment_info']['discount_amount'])

					# # encrypt
					secret = datasave['data']['encryption']['secret']
					content = datasave['data']['encryption']['content']
					subprocess.call(["/home/frappe/ahok-bench/rsa/decrypt-secret.sh"]+['/home/frappe/ahok-bench/id_rsa']+[secret]+['/home/frappe/ahok-bench/rsa/key'])
					key = open("/home/frappe/ahok-bench/rsa/key").read()
					secretKey = key.encode('ascii')
					bcontent = base64.b64decode(content)
					bnonce = bcontent[len(bcontent) - 12:len(bcontent)]
					bcipher = bcontent[0:len(bcontent) - 12]
					taglength = 16
					tag = bcipher[len(bcipher) - taglength : len(bcipher)]
					acipher = bcipher[0 : len(bcipher) - taglength]
					aesCipher = AES.new(secretKey, AES.MODE_GCM, bnonce)
					plaintext = aesCipher.decrypt_and_verify(acipher, tag)
					data_c = json.loads(plaintext)
					doc.customer_name = data_c['buyer_info']['buyer_fullname']
					doc.customer_phone =data_c['buyer_info']['buyer_phone']
					doc.nama_penerima = data_c['order_info']['destination']['receiver_name']
					doc.recipient_phone = data_c['order_info']['destination']['receiver_phone']
					alamat = data_c['order_info']['destination']['address_street']+' '+datasave['data']['order_info']['destination']['address_city']+', '+datasave['data']['order_info']['destination']['address_district']+', '+datasave['data']['order_info']['destination']['address_postal']+', '+datasave['data']['order_info']['destination']['address_province']
					doc.recipient_address = alamat

					total_weight = []
					total_asuransi = []
					for w in  datasave['data']['order_info']['order_detail']:
						total_weight.append(w['total_weight'])
						total_asuransi.append(w['insurance_price'])

					doc.total_weight = sum(total_weight)

					for t in datasave['data']['order_info']['order_history']:
						if t['hist_status_code'] == 100:
							tanggal =t['timestamp']

					tgl = tanggal[0:10]
					doc.tanggal_pesan = tgl

					doc.flags.ignore_permission = True
					doc.save()

					order_id_so = frappe.get_value("Tokopedia Orders",{"name" : str(datasave['data']['order_id'])}, "name")
					toko = frappe.get_value("Tokopedia Orders",{"name" : str(datasave['data']['order_id'])}, "shop_name")
					cek_sinv = frappe.get_value("Tokopedia Setting",{"name" : toko}, "make_sinv")
					if order_id_so:
						if cek_sinv == 0:
							frappe.msgprint("bikn so nih.")
							make_so(order_id_so)
						else:
							frappe.msgprint("bikn sinv nih.")
							confirm_order_sinv(order_id_so)
							make_sinv(order_id_so)

@frappe.whitelist()
def get_product(shop):
	app_id = frappe.get_value("Tokopedia Setting",{"name": shop}, "app_id")
	shop_id = frappe.get_value("Tokopedia Setting",{"name": shop}, "shop_id")
	token = frappe.get_value("Tokopedia Setting",{"name": shop}, "token")
	# di looping 5x
	temp_continue = True

	for looping in range(5) :
		if temp_continue == False :
			break

		elif temp_continue == True :
			data_p = Product.get_all_product_shop(app_id,token,shop_id,str(looping+1))
			# frappe.msgprint(str(data_p['data'][0]['basic']))
			if data_p['data'] == None:
				frappe.msgprint("kosong")
			else:
				frappe.msgprint("ada isinya")
				frappe.msgprint(str(data_p['data']))
				for i in data_p['data']:
					name = frappe.get_value("Marketplace Item Tokopedia",{"product_id": i['basic']['productID']}, "name")
					if name:
						frappe.msgprint(str(i['basic']['productID'])+"Product Id sudah ada")
					else:
						if len(i['variant']) > 0:
							# ada variant
							variant = Product.get_all_variants_by_idproduct(app_id,i['basic']['productID'],token)
							doci = frappe.new_doc('Marketplace Item Tokopedia')
							doci.type = "Template"
							doci.item_name = i['basic']['name']
							doci.shop = shop
							doci.product_id = i['basic']['productID']
							doci.etalase = i['menu']['id']

							if len(i['categoryTree']) == 3:
								doci.id_parent = i['categoryTree'][0]['id']
								doci.child1 = i['categoryTree'][1]['id']
								doci.child2 = i['categoryTree'][2]['id']
								id_cat = i['categoryTree'][2]['id']
							else :
								doci.id_parent = i['categoryTree'][0]['id']
								doci.child1 = i['categoryTree'][1]['id']
								id_cat = i['categoryTree'][1]['id']

							if i['basic']['condition'] == 1:
								doci.condition_item ='NEW'
							else :
								doci.condition_item ='USED'

							if i['basic']['status'] == 1:
								doci.status_item ='LIMITED'
							elif i['basic']['status'] == 2:
								doci.status_item ='UNLIMITED'
							elif i['basic']['status'] == 3:
								doci.status_item ='EMPTY'

							if i['basic']['mustInsurance'] == True:
								doci.is_must_insurance = 1
							else :
								doci.is_must_insurance = 0

							doci.min_order = i['extraAttribute']['minOrder']

							if len(variant['data']['variant']) > 1:
								attb1 = frappe.get_value("Item Attribute",{"name" : ["like", "%"+variant['data']['variant'][0]['unit_name']+"|"+variant['data']['variant'][0]['name']+"%"]}, "name")
								attb2 = frappe.get_value("Item Attribute",{"name" : ["like", "%"+variant['data']['variant'][1]['unit_name']+"|"+variant['data']['variant'][1]['name']+"%"]}, "name")
								if not attb1 or not attb2:
									create_product_variant(id_cat)
								doci.variant_1 = attb1
								doci.variant_2 = attb2
								for v1 in variant['data']['variant'][0]['option']:
									row=doci.append('table_variant_1', {})
									attb_val1 = frappe.get_value("Item Attribute Value",{"attribute_value" : ["like", "%"+v1['value']+"%"],"parent": attb1}, "attribute_value")
									if attb_val1:
										id_val1 = attb_val1.split("|")
										row.id= id_val1[0]
									else:
										row.id = v1['id']
									row.value = v1['value']

								for v2 in variant['data']['variant'][1]['option']:
									row=doci.append('table_variant_2', {})
									attb_val2 = frappe.get_value("Item Attribute Value",{"attribute_value" : ["like", "%"+v2['value']+"%"],"parent": attb2}, "attribute_value")
									if attb_val2:
										id_val2 = attb_val2.split("|")
										row.id= id_val2[0]
									else:
										row.id = v2['id']
									row.value = v2['value']
							else:
								attb1 = frappe.get_value("Item Attribute",{"name" : ["like", "%"+variant['data']['variant'][0]['unit_name']+"|"+variant['data']['variant'][0]['name']+"%"]}, "name")
								doci.variant_1 = attb1
								if not attb1:
									create_product_variant(id_cat)
								for v1 in variant['data']['variant'][0]['option']:
									row=doci.append('table_variant_1', {})
									attb_val1 = frappe.get_value("Item Attribute Value",{"attribute_value" : ["like", "%"+v1['value']+"%"],"parent": attb1}, "attribute_value")
									if attb_val1:
										id_val1 = attb_val1.split("|")
										row.id= id_val1[0]
									else:
										row.id = v1['id']
									row.value = v1['value']

							doci.flags.ignore_permission=True
							doci.save()
							frappe.msgprint(str(i['basic']['productID'])+"Sudah DI tambahkan")
						else:
							# no variant
							doci = frappe.new_doc('Marketplace Item Tokopedia')
							doci.type = "Product"
							doci.item_name = i['basic']['name']
							doci.shop = shop
							doci.product_id = i['basic']['productID']
							doci.etalase = i['menu']['id']

							if len(i['categoryTree']) == 3:
								doci.id_parent = i['categoryTree'][0]['id']
								doci.child1 = i['categoryTree'][1]['id']
								doci.child2 = i['categoryTree'][2]['id']
							else :
								doci.id_parent = i['categoryTree'][0]['id']
								doci.child1 = i['categoryTree'][1]['id']

							if i['basic']['condition'] == 1:
								doci.condition_item ='NEW'
							else :
								doci.condition_item ='USED'

							if i['basic']['status'] == 1:
								doci.status_item ='LIMITED'
							elif i['basic']['status'] == 2:
								doci.status_item ='UNLIMITED'
							elif i['basic']['status'] == 3:
								doci.status_item ='EMPTY'

							if i['basic']['mustInsurance'] == True:
								doci.is_must_insurance = 1
							else :
								doci.is_must_insurance = 0

							doci.min_order = i['extraAttribute']['minOrder']

							doci.flags.ignore_permission=True
							doci.save()

							frappe.msgprint(str(i['basic']['productID'])+"Sudah DI tambahkan")
				
@frappe.whitelist()
def crate_product2(id_product,data_item):
	#frappe.msgprint("test Lutfi")
	data_i = frappe.db.get_list('Item',filters={'name': id_product},fields=['*'])
	data_item = json.loads(data_item)
	token = frappe.get_value("Tokopedia Setting",{"name": data_item['shop']}, "token")
	data = []
	for i in data_i:
		price= frappe.get_value("Item Price",{"item_code": i['item_code']}, "price_list_rate")
		stock= frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
		images=[]

		img = {
			"file_path": frappe.utils.get_url()+i['gambar_utama']
		}

		images.append(img)

		if i['gambar_depan']:
			img1 = {
				"file_path": frappe.utils.get_url()+i['gambar_depan']
			}
			images.append(img1)

		if i['gambar_atas']:
			img2 = {
				"file_path": frappe.utils.get_url()+i['gambar_atas']
			}
			images.append(img2)
		

		if i['gambar_samping']:
			img3 = {
				"file_path": frappe.utils.get_url()+i['gambar_samping']
			}
			images.append(img3)
		
		if i['gambar_detail']:
			img4 = {
				"file_path": frappe.utils.get_url()+i['gambar_detail']
			}
			images.append(img4)

		frappe.msgprint(str(images))
		


		isi ={
						"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
						"condition": data_item['condition'],
						"description": i['description'],
						"sku": data_item['sku'], #tidak boleh ada spasi
						"price": int(price),
						"status": data_item['status'],
						"stock": int(stock),
						"min_order": data_item['min_order'],
						"category_id": data_item['category_id'],
						"price_currency": data_item['price_currency'],
						"weight": int(i['weight_per_unit']),
						"weight_unit": i['weight_uom'],
						"is_free_return": data_item['is_free_return'],
						"is_must_insurance": data_item['is_must_insurance'],
						"dimension": {
							"height": float(i['height']),
							"width":  float(i['width']),
							"length":  float(i['length'])
						},
						"custom_product_logistics": data_item['custom_product_logistics'],
						"annotations": data_item['annotations'],
						"etalase": data_item['etalase'],
						"pictures": images,
						"wholesale": [],
						"preorder": {},
						"videos": []
					}
		data.append(isi)
		
		test = Product.create_product(data_item['app_id'],data_item['shop_id'],data,token)
		# frappe.msgprint(str(test['data']['success_rows_data'][0]['product_id']))
		doc = frappe.get_doc("Marketplace Item Tokopedia",data_item['name'])
		doc.product_id = test['data']['success_rows_data'][0]['product_id']
		
		doc.flags.ignore_permission=True
		doc.save()
		frappe.msgprint("Cretae data berhasil !")			

	# frappe.msgprint(str(data))

@frappe.whitelist()
def edit_product(id_product,data_item):
	# frappe.msgprint("test Lutfi edit")
	data_i = frappe.db.get_list('Item',filters={'name': id_product},fields=['*'])
	data_item = json.loads(data_item)
	token = frappe.get_value("Tokopedia Setting",{"name": data_item['shop']}, "token")
	data = []
	for i in data_i:
		price= frappe.get_value("Item Price",{"item_code": i['item_code']}, "price_list_rate")
		stock= frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
		images=[]

		img = {
			"file_path": frappe.utils.get_url()+i['gambar_utama']
		}

		images.append(img)

		if i['gambar_depan']:
			img1 = {
				"file_path": frappe.utils.get_url()+i['gambar_depan']
			}
			images.append(img1)

		if i['gambar_atas']:
			img2 = {
				"file_path": frappe.utils.get_url()+i['gambar_atas']
			}
			images.append(img2)
		

		if i['gambar_samping']:
			img3 = {
				"file_path": frappe.utils.get_url()+i['gambar_samping']
			}
			images.append(img3)
		
		if i['gambar_detail']:
			img4 = {
				"file_path": frappe.utils.get_url()+i['gambar_detail']
			}
			images.append(img4)

		frappe.msgprint(str(images))
		
		isi ={
				"id": data_item['product_id'],
				"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
				"condition": data_item['condition'],
				"description": i['description'],
				"sku": data_item['sku'], #tidak boleh ada spasi
				"price": int(price),
				"status": data_item['status'],
				"stock": int(stock),
				"min_order": data_item['min_order'],
				"category_id": data_item['category_id'],
				"price_currency": data_item['price_currency'],
				"weight": int(i['weight_per_unit']),
				"weight_unit": i['weight_uom'],
				"is_free_return": data_item['is_free_return'],
				"is_must_insurance": data_item['is_must_insurance'],
				"dimension": {
					"height": float(i['height']),
					"width":  float(i['width']),
					"length":  float(i['length'])
				},
				"custom_product_logistics": data_item['custom_product_logistics'],
				"annotations": data_item['annotations'],
				"etalase": data_item['etalase'],
				"pictures": images,
				"wholesale": [],
				"preorder": {},
				"videos": []
			}
		data.append(isi)
		
		Product.edit_product(data_item['app_id'],data_item['shop_id'],data,token)
		frappe.msgprint("edit data berhasil !")		

	# frappe.msgprint(str(data))

# @frappe.whitelist()
# def crate_product(id_product):
# 	# frappe.msgprint("masuk add proooo")
# 	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['app_id','shop_name','token','shop_id'])
# 	data_i = frappe.db.get_list('Item',filters={'name': id_product},fields=['*'])
# 	for i in data_i:
# 		etalase = frappe.db.get_list('Daftar Etalase',filters={'parent': i['name'] },fields=['*'])
# 		spek = frappe.db.get_list('Spesifikasi Tokpedia',filters={'parent': i['name'] },fields=['*'])
# 		for j in etalase:
# 			app_id = frappe.get_value("Tokopedia Setting",{"name": j['shop']}, "app_id")
# 			shop_name = frappe.get_value("Tokopedia Setting",{"name": j['shop']}, "name")
# 			# frappe.msgprint(shop_name)
# 			shop_id = frappe.get_value("Tokopedia Setting",{"name": j['shop']}, "shop_id")
# 			token = frappe.get_value("Tokopedia Setting",{"name": j['shop']}, "token")
# 			get_price = frappe.get_value("Item Price",{"price_list" : "Standard Selling","item_code": i['item_code']}, "price_list_rate")
# 			data1=[]
# 			data2=[]
# 			data3=[]
# 			d_spek=[]
# 			if j['logistic']:
# 				if ',' in j['logistic']:
# 					data1=j['logistic'].split(',')
# 					for l in data1:
# 						data2.append(l.split('-'))

# 					for log2 in data2:
# 						data3.append(int(log2[0]))
# 				else:
# 					data1.append(j['logistic'])
# 					for l in data1:
# 						data2.append(l.split('-'))

# 					for log2 in data2:
# 						data3.append(int(log2[0]))
# 			else:
# 				data3=[]

# 			if spek:
# 				for sp in spek:
# 					d_spek.append(sp['id'])

# 			frappe.msgprint(str(data3))

			
# 			if i['gambar_depan']:
# 				img1 = i['gambar_depan']
# 			else:
# 				img1 = i['gambar_utama']

# 			if i['gambar_atas']:
# 				img2 = i['gambar_atas']
# 			else:
# 				img2 = i['gambar_utama']

# 			if i['gambar_samping']:
# 				img3 = i['gambar_samping']
# 			else:
# 				img3 = i['gambar_utama']
			
# 			if i['gambar_detail']:
# 				img4 = i['gambar_detail']
# 			else:
# 				img4 = i['gambar_utama']

# 			if i['child2']:
# 				cat_id = i['child2']
# 			else:
# 				cat_id = i['child1']

# 			if i['is_free_return'] == 0:
# 				f_return = False
# 			else :
# 				f_return = True

# 			if i['is_must_insurance'] == 0:
# 				insurance = False
# 			else :
# 				insurance = True
			
# 			data =[]
# 			isi ={
# 					"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
# 					"condition": i['condition_item'],
# 					"description": i['description'],
# 					"sku": i['item_code'], #tidak boleh ada spasi
# 					"price": int(i['standard_rate']),
# 					"status": i['status_item'],
# 					"stock": int(i['opening_stock']),
# 					"min_order": int(i['min_order']),
# 					"category_id": int(cat_id),
# 					"price_currency": i['currency_item_tokopedia'],
# 					"weight": int(i['weight_per_unit']),
# 					"weight_unit": i['weight_uom'],
# 					"is_free_return": f_return,
# 					"is_must_insurance": insurance,
# 					"dimension": {
# 						"height": float(i['height']),
# 						"width":  float(i['width']),
# 						"length":  float(i['length'])
# 					},
# 					"custom_product_logistics": data3,
# 					"annotations": d_spek,
# 					"etalase": {
# 						"id": int(j['id']) #kode etalase
# 					},
# 					"pictures": [
# 						{
# 							"file_path": frappe.utils.get_url()+i['gambar_utama']
# 						},
# 						{
# 							"file_path": frappe.utils.get_url()+img1
# 						},
# 						{
# 							"file_path": frappe.utils.get_url()+img2
# 						},
# 						{
# 							"file_path": frappe.utils.get_url()+img3
# 						},
# 						{
# 							"file_path": frappe.utils.get_url()+img4
# 						}

# 						#i['image']
# 					],
# 					"wholesale": [],
# 					"preorder": {},
# 					"videos": []
# 				}
# 			data.append(isi)
# 			frappe.msgprint(i['name'])
# 			frappe.msgprint(str(data))
# 			frappe.msgprint(app_id+":"+shop_id+":"+token)
			
# 			# Product.create_product(app_id,shop_id,data,token)
# 			test = Product.create_product(app_id,shop_id,data,token)
# 			# frappe.msgprint(str(test['data']['success_rows_data'][0]['product_id']))
# 			doc = frappe.get_doc("Item",i['name'])
# 			# doc.product_id = test['data']['success_rows_data'][0]['product_id']
# 			row = doc.append('product_id_tokopedia', {})
# 			row.product_id = test['data']['success_rows_data'][0]['product_id']
# 			row.shop_id = shop_id
# 			row.shop = shop_name
			
# 			doc.flags.ignore_permission=True
# 			doc.save()
# 			frappe.msgprint("Cretae data berhasil !")

		
@frappe.whitelist()
def update_stock2(doc,method):
	app_id = ""
	if doc.stock_entry_type == "Material Receipt":
		app_id = frappe.get_value("Tokopedia Setting",{"warehouse": doc.to_warehouse}, "app_id")
		shop_id = frappe.get_value("Tokopedia Setting",{"warehouse": doc.to_warehouse}, "shop_id")
		token = frappe.get_value("Tokopedia Setting",{"warehouse": doc.to_warehouse}, "token")
	
	if doc.stock_entry_type == "Material Issue":
		app_id = frappe.get_value("Tokopedia Setting",{"warehouse": doc.from_warehouse}, "app_id")
		shop_id = frappe.get_value("Tokopedia Setting",{"warehouse": doc.from_warehouse}, "shop_id")
		token = frappe.get_value("Tokopedia Setting",{"warehouse": doc.from_warehouse}, "token")

	if app_id:
		data_stock = frappe.db.get_list('Stock Entry Detail',filters={'parent': doc.name},fields=['*'])
		# update stock
		isi =[]
		for i in data_stock:
			stock = frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
			ds = {
				"sku": i['item_code'],
				"new_stock": int(stock)
			}
			isi.append(ds)
		Price.update_stock(app_id,shop_id,token,isi)
	else:
		pass
		# frappe.msgprint("app id tidak ada")

@frappe.whitelist()
def bulk_update(data):
	data = json.loads(data)
	result = []
	for i in data:
		dataToko = frappe.get_value('Tokopedia Setting', {'shop_name': i['shop_name']}, ["shop_id","app_id","token"])
		app_id = dataToko[1]
		shop_id = dataToko[0]
		token = dataToko[2]
		isi = [{
			"sku": i['item_code'],
			"new_stock": int(i['new_stock'])
		}]
		
		updateStock = Price.update_stock(app_id = app_id,shop_id = shop_id,token = token,data = isi)
		result.append(updateStock) 
		# frappe.msgprint(str(updateStock))
	return result

@frappe.whitelist()
def update_price2(doc,method):
	app_id = frappe.get_value("Tokopedia Setting",{"price_list": doc.price_list}, "app_id")
	shop_id = frappe.get_value("Tokopedia Setting",{"price_list": doc.price_list}, "shop_id")
	token = frappe.get_value("Tokopedia Setting",{"price_list": doc.price_list}, "token")
	
	if app_id:
		data =[]
		isi ={
				"sku": doc.item_code,
				"new_price": int(doc.price_list_rate)
			}
		data.append(isi)
		Price.update_price(app_id,shop_id,token,data)
		

	# frappe.msgprint("Update Harga Berhasil !")

@frappe.whitelist()
def update_price_stock(doc,method):
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['app_id','shop_name','token','shop_id'])
	# data_i = frappe.db.get_list('Item',filters={'disabled': 0,"item_group": "Tokopedia"},fields=['*'])
	#update harga
	# for i in data_i:
	# 	shop_id = frappe.db.get_list('Shop Tokopedia',filters={'parent': i['name'] },fields=['*'])
	# 	price = frappe.get_value("Item Price",{"price_list" : "Standard Selling","item_code": i['item_code']}, "price_list_rate")
	# 	for s in shop_id:
	# 		app_id = frappe.get_value("Tokopedia Setting",{"name": s['shop']}, "app_id")
	# 		shop_id = frappe.get_value("Tokopedia Setting",{"name": s['shop']}, "shop_id")
	# 		token = frappe.get_value("Tokopedia Setting",{"name": s['shop']}, "token")
	# 		data =[]
	# 		isi ={
	# 				"sku": i['item_code'],
	# 				"new_price": int(price)
	# 			}
	# 		data.append(isi)
	# 		Price.update_price(app_id,shop_id,token,data)	
			

	# # frappe.msgprint("Update Harga Berhasil !")

	# # update stock
	# for j in data_i:
	stock = frappe.get_value("Bin",{"item_code": doc.item_code}, "actual_qty")
	item_group = frappe.get_value("Item",{"item_code": doc.item_code}, "item_group")
	# shop_id = frappe.db.get_list('Shop Tokopedia',filters={'parent': j['name'] },fields=['*'])
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['app_id','shop_name','token','shop_id'])
	if not stock:
		stock = 1
	if item_group == "Tokopedia":
		for s in datas:
			# app_id = frappe.get_value("Tokopedia Setting",{"name": s['shop']}, "app_id")
			# shop_id = frappe.get_value("Tokopedia Setting",{"name": s['shop']}, "shop_id")
			# token = frappe.get_value("Tokopedia Setting",{"name": s['shop']}, "token")
			data =[]
			isi ={
					"sku": doc.item_code,
					"new_stock": int(stock)
				}
			data.append(isi)
			# Price.update_stock(s['app_id'],s['shop_id'],s['token'],data)

		# frappe.msgprint("Update Stock Berhasil !")

@frappe.whitelist()
def confirm_order(doc,method):
	#Payment verified, order ready to process
	get_order = frappe.db.get_list('Sales Order',filters={'marketplace_id': doc.marketplace_id,"docstatus": 1,"marketplace": "Tokopedia"},fields=['*'])
	frappe.msgprint(str(get_order))
	for i in get_order:
		if i['marketplace'] == "Tokopedia":
			data = frappe.db.get_list('Sales Order Item',filters={'parent': i['name'] },fields=['*'])
			app_id = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "app_id")
			token = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "token")
			count = 0
			for j in data:
				frappe.msgprint(j['item_code'])
				stock = frappe.get_value("Bin",{"item_code": j['item_code']}, "actual_qty")
				if j['qty'] <= stock:
					frappe.msgprint("Stock Ada")
					count = count + 1
				else :
					frappe.msgprint("Stock Habis/ Kurang")

			# frappe.throw("Stock Habis/ Kurang")
			frappe.msgprint(str(count))	
			if count == len(data):
				frappe.msgprint("Terima Order")
				url = "https://fs.tokopedia.net/v1/order/"+i['marketplace_id']+"/fs/"+app_id+"/ack"
				payload={}
				headers = {
		 			'Authorization': 'Bearer '+ token
				}
				response = requests.request("POST", url, headers=headers, data=payload)
				print(response.text)
				frappe.msgprint(str(response.text))
			else:
				frappe.msgprint("Cek Stock")

@frappe.whitelist()
def confirm_order_sinv(order_id):
	#Payment verified, order ready to process
	get_order = frappe.db.get_list('Tokopedia Orders',filters={'order_id': order_id},fields=['*'])
	# frappe.msgprint(str(get_order))
	for i in get_order:
		if i['marketplace'] == "Tokopedia":
			data = frappe.db.get_list('Tokopedia Orders Item',filters={'parent': i['name'] },fields=['*'])
			app_id = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "app_id")
			token = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "token")
			count = 0
			for j in data:
				# frappe.msgprint(j['item_code'])
				stock = frappe.get_value("Bin",{"item_code": j['item_sku']}, "actual_qty")
				if j['qty'] <= stock:
					frappe.msgprint("Stock Ada")
					count = count + 1
				else :
					frappe.msgprint("Stock Habis/ Kurang")

			# frappe.throw("Stock Habis/ Kurang")
			frappe.msgprint(str(count))	
			if count == len(data):
				frappe.msgprint("Terima Order")
				url = "https://fs.tokopedia.net/v1/order/"+i['order_id']+"/fs/"+app_id+"/ack"
				payload={}
				headers = {
		 			'Authorization': 'Bearer '+ token
				}
				response = requests.request("POST", url, headers=headers, data=payload)
				print(response.text)
				frappe.msgprint(str(response.text))
			else:
				frappe.msgprint("Cek Stock")

@frappe.whitelist()
def accept_order(order_id):
	#Payment verified, order ready to process
	get_order = frappe.db.get_list('Tokopedia Orders',filters={'order_id': order_id },fields=['*'])
	for i in get_order:
		data = frappe.db.get_list('Sales Order Item',filters={'parent': i['name'] },fields=['*'])
		app_id = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "app_id")
		token = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "token")
		count = 0
		for j in data:
			frappe.msgprint(j['item_code'])
			stock = frappe.get_value("Bin",{"item_code": j['item_code']}, "actual_qty")
			if j['qty'] <= stock:
				frappe.msgprint("Stock Ada")
				count = count + 1
			else :
				frappe.msgprint("Stock Habis/ Kurang")

		# frappe.throw("Stock Habis/ Kurang")
		frappe.msgprint(str(count))	
		if count == len(data):
			frappe.msgprint("Terima Order")
			url = "https://fs.tokopedia.net/v1/order/"+i['order_id']+"/fs/"+app_id+"/ack"
			payload={}
			headers = {
	 			'Authorization': 'Bearer '+ token
			}
			response = requests.request("POST", url, headers=headers, data=payload)
			print(response.text)
			frappe.msgprint(str(response.text))
		else:
			frappe.msgprint("Cek Stock")

@frappe.whitelist()
def create_product_variant(cat):
	variant = Product.get_all_variants(cat) #v2
	# variant = Product.get_all_variants_v1(cat) # v1
	# frappe.msgprint("Test Variant"+str(variant))
	data=[]
	#frappe.msgprint(str(variant['data']['category_id']))
	for i in variant['data']['variant_details']: # v2
	# for i in variant['data']: # v1
		# frappe.msgprint(i['name']+" Tokopedia")
		for j in i['units']:
			data.append(str(i['variant_id'])+"|"+str(j['variant_unit_id'])+"|"+j['unit_name']+"|"+i['name']+" Tokopedia") # v2
			# data.append(str(i['variant_id'])+"|"+str(j['unit_id'])+"|"+j['name']+"|"+i['name']+" Tokopedia") # v1
			#frappe.msgprint(str(j['variant_unit_id']))
			get_val=frappe.get_value("Item Attribute",{"name": str(i['variant_id'])+"|"+str(j['variant_unit_id'])+"|"+j['unit_name']+"|"+i['name']+" Tokopedia"}, "name") # v2
			# get_val=frappe.get_value("Item Attribute",{"name": str(i['variant_id'])+"|"+str(j['unit_id'])+"|"+j['name']+"|"+i['name']+" Tokopedia"}, "name") # v1
			if get_val:
				pass
				#frappe.msgprint("sudah ada")
			else:
				doc = frappe.new_doc('Item Attribute')
				doc.attribute_name = str(i['variant_id'])+"|"+str(j['variant_unit_id'])+"|"+j['unit_name']+"|"+i['name']+" Tokopedia" # v2
				# doc.attribute_name = str(i['variant_id'])+"|"+str(j['unit_id'])+"|"+j['name']+"|"+i['name']+" Tokopedia" # v1
				for k in j['unit_values']: # v2
				# for k in j['values']: # v1
					#frappe.msgprint(k['value'])
					row = doc.append('item_attribute_values', {})
					row.attribute_value = str(k['variant_unit_value_id'])+'|'+k['value'] # v2
					# row.attribute_value = str(k['value_id'])+'|'+k['value'] # v1
					row.abbr = k['value']
					# row.attribute_value = k['value']
					# row.abbr = str(k['variant_unit_value_id'])

					doc.flags.ignore_permission = True
					doc.save()
					frappe.msgprint('Tambah Item atribute Sukses !!')
	return data

@frappe.whitelist()
def add_variant(var):
	var = frappe.db.get_list('Item Attribute Value',filters={'parent': var},fields=['*'])
	data_var =[]
	for v in var:
		data_var.append(v['attribute_value'])
	# frappe.msgprint(str(data_var))
	return data_var

@frappe.whitelist()
def del_market_variant(name):
	# data_variant = json.loads(data_variant)
	cek = frappe.db.get_list('Marketplace Item Tokopedia',filters={'template': name},fields=['*'],order_by='name asc')
	for c in cek:
		frappe.msgprint(c['name'])
		frappe.delete_doc('Marketplace Item Tokopedia', c['name'])
	frappe.msgprint("Market item variant berhasi di hapus")

@frappe.whitelist()
def make_market_variant(name,variant,data_variant):
	# awal
	# doc = frappe.new_doc('Marketplace Item Tokopedia')
	# doc.type = "Product Variant"
	# doc.template = name
	# doc.variasi = variant

	# doc.flags.ignore_permission = True
	# doc.save()
	# frappe.msgprint("Buat Product Variant")
	
	#coba*
	data_variant = json.loads(data_variant)
	cek = frappe.db.get_list('Marketplace Item Tokopedia',filters={'template': data_variant['name']},fields=['*'],order_by='name asc')
	data=[]
	
	if data_variant['variant_2']:
		# 2 variant
		panjang = len(data_variant['options_value_1'])*len(data_variant['options_value_2'])
		if panjang == len(cek):
			frappe.msgprint("masuk panjang variant sudah sama")
		else:
			frappe.msgprint("mauk buat baru 2 variant")
			doc = frappe.new_doc('Marketplace Item Tokopedia')
			doc.type = "Product Variant"
			doc.template = name
			doc.variasi = variant

			doc.flags.ignore_permission = True
			doc.save()
			frappe.msgprint("Buat Product Variant")
	else:
		# 1 varaint
		if len(data_variant['options_value_1']) == len(cek):
			frappe.msgprint("jumlah product varian sudah sama")
		elif cek:
			frappe.msgprint("mauk else delete yang lama")
			for c in cek:
				frappe.msgprint(c['name'])
				frappe.delete_doc('Marketplace Item Tokopedia', c['name'])
		else:
			frappe.msgprint("mauk buat baru")
			doc = frappe.new_doc('Marketplace Item Tokopedia')
			doc.type = "Product Variant"
			doc.template = name
			doc.variasi = variant

			doc.flags.ignore_permission = True
			doc.save()
			frappe.msgprint("Buat Product Variant 1variant")


			# doc = frappe.get_doc('Marketplace Item Tokopedia', c['name'])
			
			# doc.flags.ignore_permission = True
			# doc.delete()

	# 	for c in cek:
	# 		data.append(c['variasi'])

	# 	for dv in data_variant['options_value_1']:
	# 		conter=0
	# 		for d in data:
	# 			if dv == d:
	# 				conter
	# 			else:
	# 				conter=conter+1

	# 		if conter==len(data):
	# 			var_tambah = dv
	# 			frappe.msgprint(dv+"belum ada")	
		
	# 	doc = frappe.new_doc('Marketplace Item Tokopedia')
	# 	doc.type = "Product Variant"
	# 	doc.template = name
	# 	doc.variasi = var_tambah

	# 	doc.flags.ignore_permission = True
	# 	doc.save()
	# 	frappe.msgprint("Buat Product Variant")

		# for c in cek:
		# 	frappe.msgprint(c['variasi'])
		# for dv in data_variant['options_value_1']:
		# 	frappe.msgprint(str(dv))
		# 	if dv == cek['variasi']: 
		# 		doc = frappe.new_doc('Marketplace Item Tokopedia')
		# 		doc.type = "Product Variant"
		# 		doc.template = name
		# 		doc.variasi = dv

		# 		doc.flags.ignore_permission = True
		# 		doc.save()
		# 		frappe.msgprint("Buat Product Variant")

		
@frappe.whitelist()
def push_item_var(item_code,data_item,data_variant):
	frappe.msgprint("masuk sini variant")
	data_i = frappe.db.get_list('Item',filters={'name': item_code},fields=['*'])
	data_item = json.loads(data_item)
	data_variant = json.loads(data_variant)
	data_variant_link = frappe.db.get_list('Tabel Gabung Variant',filters={'parent': data_item['name']},fields=['*'],order_by='idx asc')
	token = frappe.get_value("Tokopedia Setting",{"name": data_item['shop']}, "token")
	frappe.msgprint(token)
	frappe.msgprint(str(data_variant))
	data=[]
	data_products=[]
	data_selection=[]
	data_selection2=[]
	data_options=[]
	data_options2=[]
	union_selection=[]
	conter=0

	con_opt=0
	for opt in data_variant['options_id_1']:
		options={
					"hex_code":"",
					"unit_value_id":int(opt),
					"value": data_variant['options_value_1'][con_opt]
				}
		con_opt=con_opt+1
		data_options.append(options)

	con_opt2=0
	for opt2 in data_variant['options_id_2']:
		options={
					"hex_code":"",
					"unit_value_id":int(opt2),
					"value": data_variant['options_value_2'][con_opt2]
				}
		con_opt2=con_opt2+1
		data_options2.append(options)
	
	
	frappe.msgprint(str(data_options))
	frappe.msgprint(str(data_options2))


	for sel in data_variant['variant_1']:
		selection1={
			"id":int(sel[0]),
			"unit_id":int(sel[1]),
			"options": data_options
		}
	data_selection.append(selection1)

	if data_variant['variant_2']:
		for sel2 in data_variant['variant_2']:
			selection2 = {
				"id":int(sel2[0]),
				"unit_id":int(sel2[1]),
				"options": data_options2
			}
		data_selection.append(selection2)
	

	frappe.msgprint("selesction"+str(data_selection))


	com=[]
	for gv1 in range(len(data_variant['options_id_1'])):
		for gv2 in range(len(data_variant['options_id_2'])):
			productsv= [gv1,gv2]
			com.append(productsv)
			# frappe.msgprint("combination"+str(productsv))

	
	if data_variant['variant_2']:
		# dua kombinasi
		for dv in data_variant_link:
			if dv['primary'] == 1:
				primary = True
			else:
				primary = False
			
			price= frappe.get_value("Item Price",{"item_code": dv['item_code']}, "price_list_rate")
			stock= frappe.get_value("Bin",{"item_code": dv['item_code']}, "actual_qty")
			images = frappe.get_value("Item",{"name": dv['item_code']}, "gambar_utama")
			# frappe.msgprint(str((images)))
			pictures={
				"file_path": frappe.utils.get_url()+images
			}

			products={
					"is_primary":primary,
					"status": data_item['status'],
					"price": int(price),
					"stock": int(stock),
					"sku": dv['item_code'],
					"combination":com[conter],
					"pictures": [pictures]
			}
			conter=conter+1
			data_products.append(products)
		frappe.msgprint(str(data_products))
	else: 
		# 1 combinasis
		for dv in data_variant_link:
			if dv['primary'] == 1:
				primary = True
			else:
				primary = False
			
			price= frappe.get_value("Item Price",{"item_code": dv['item_code']}, "price_list_rate")
			stock= frappe.get_value("Bin",{"item_code": dv['item_code']}, "actual_qty")
			images = frappe.get_value("Item",{"name": dv['item_code']}, "gambar_utama")
			# frappe.msgprint(str((images)))
			pictures={
				"file_path": frappe.utils.get_url()+images
			}

			products={
					"is_primary":primary,
					"status": data_item['status'],
					"price": int(price),
					"stock": int(stock),
					"sku": dv['item_code'],
					"combination":[conter],
					"pictures": [pictures]
			}
			conter=conter+1
			data_products.append(products)
		frappe.msgprint(str(data_products))

	

	for i in data_i:
		# stock= frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
		price= frappe.get_value("Item Price",{"item_code": i['item_code']}, "price_list_rate")
		stock= frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
		isi = {
				"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
				"condition": data_item['condition'],
				"description": i['description'],
				"sku": data_item['sku'], #tidak boleh ada spasi
				"price": int(price),
				"status": data_item['status'],
				"stock": int(stock),
				"min_order": data_item['min_order'],
				"category_id": data_item['category_id'],
				"price_currency": data_item['price_currency'],
				"weight": int(i['weight_per_unit']),
				"weight_unit": i['weight_uom'],
				"is_free_return": data_item['is_free_return'],
				"is_must_insurance": data_item['is_must_insurance'],
				"dimension": {
					"height": float(i['height']),
					"width":  float(i['width']),
					"length":  float(i['length'])
				},
				"custom_product_logistics": data_item['custom_product_logistics'],
				"annotations": data_item['annotations'],
				"etalase": data_item['etalase'],
				"pictures": [
					{
						"file_path": frappe.utils.get_url()+i['gambar_utama']
					}
				],
				"wholesale": [],
				"preorder": {},
				"videos": [],
				"variant":{
					"products":data_products,
					"selection":data_selection,
					"sizecharts":[]
				}
			}
		data.append(isi)
		frappe.msgprint(str(data))
		test = Product.create_product(data_item['app_id'],data_item['shop_id'],data,token)
		# frappe.msgprint(str(test['data']['success_rows_data'][0]['product_id']))
		doc = frappe.get_doc("Marketplace Item Tokopedia",data_item['name'])
		doc.product_id = test['data']['success_rows_data'][0]['product_id']
		
		doc.flags.ignore_permission=True
		doc.save()
		frappe.msgprint("Cretae data product variant berhasil !")

@frappe.whitelist()
def edit_item_var(item_code,data_item,data_variant):
	frappe.msgprint("Edit VAriant.....")
	data_i = frappe.db.get_list('Item',filters={'name': item_code},fields=['*'])
	data_item = json.loads(data_item)
	data_variant = json.loads(data_variant)
	data_variant_link = frappe.db.get_list('Tabel Gabung Variant',filters={'parent': data_item['name']},fields=['*'],order_by='idx asc')
	token = frappe.get_value("Tokopedia Setting",{"name": data_item['shop']}, "token")
	frappe.msgprint(str(data_variant))
	data=[]
	data_products=[]
	data_selection=[]
	data_selection2=[]
	data_options=[]
	data_options2=[]
	union_selection=[]
	conter=0

	con_opt=0
	for opt in data_variant['options_id_1']:
		options={
					"hex_code":"",
					"unit_value_id":int(opt),
					"value": data_variant['options_value_1'][con_opt]
				}
		con_opt=con_opt+1
		data_options.append(options)

	con_opt2=0
	for opt2 in data_variant['options_id_2']:
		options={
					"hex_code":"",
					"unit_value_id":int(opt2),
					"value": data_variant['options_value_2'][con_opt2]
				}
		con_opt2=con_opt2+1
		data_options2.append(options)
	
	
	frappe.msgprint(str(data_options))
	frappe.msgprint(str(data_options2))


	for sel in data_variant['variant_1']:
		selection1={
			"id":int(sel[0]),
			"unit_id":int(sel[1]),
			"options": data_options
		}
	data_selection.append(selection1)

	if data_variant['variant_2']:
		for sel2 in data_variant['variant_2']:
			selection2 = {
				"id":int(sel2[0]),
				"unit_id":int(sel2[1]),
				"options": data_options2
			}
		data_selection.append(selection2)
	

	frappe.msgprint("selesction"+str(data_selection))


	com=[]
	for gv1 in range(len(data_variant['options_id_1'])):
		for gv2 in range(len(data_variant['options_id_2'])):
			productsv= [gv1,gv2]
			com.append(productsv)
			# frappe.msgprint("combination"+str(productsv))

	
	if data_variant['variant_2']:
		# dua kombinasi
		for dv in data_variant_link:
			if dv['primary'] == 1:
				primary = True
			else:
				primary = False
			
			price= frappe.get_value("Item Price",{"item_code": dv['item_code']}, "price_list_rate")
			stock= frappe.get_value("Bin",{"item_code": dv['item_code']}, "actual_qty")
			images = frappe.get_value("Item",{"name": dv['item_code']}, "gambar_utama")
			# frappe.msgprint(str((images)))
			pictures={
				"file_path": frappe.utils.get_url()+images
			}

			products={
					"is_primary":primary,
					"status": data_item['status'],
					"price": int(price),
					"stock": int(stock),
					"sku": dv['item_code'],
					"combination":com[conter],
					"pictures": [pictures]
			}
			conter=conter+1
			data_products.append(products)
		frappe.msgprint(str(data_products))
	else: 
		# 1 combinasis
		for dv in data_variant_link:
			if dv['primary'] == 1:
				primary = True
			else:
				primary = False
			
			price= frappe.get_value("Item Price",{"item_code": dv['item_code']}, "price_list_rate")
			stock= frappe.get_value("Bin",{"item_code": dv['item_code']}, "actual_qty")
			images = frappe.get_value("Item",{"name": dv['item_code']}, "gambar_utama")
			# frappe.msgprint(str((images)))
			pictures={
				"file_path": frappe.utils.get_url()+images
			}

			products={
					"is_primary":primary,
					"status": data_item['status'],
					"price": int(price),
					"stock": int(stock),
					"sku": dv['item_code'],
					"combination":[conter],
					"pictures": [pictures]
			}
			conter=conter+1
			data_products.append(products)
		frappe.msgprint(str(data_products))

	

	for i in data_i:
		price= frappe.get_value("Item Price",{"item_code": i['item_code']}, "price_list_rate")
		stock= frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
		isi = {
				"id": data_item['product_id'],
				"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
				"condition": data_item['condition'],
				"description": i['description'],
				"sku": data_item['sku'], #tidak boleh ada spasi
				"price": int(price),
				"status": data_item['status'],
				"stock": int(stock),
				"min_order": data_item['min_order'],
				"category_id": data_item['category_id'],
				"price_currency": data_item['price_currency'],
				"weight": int(i['weight_per_unit']),
				"weight_unit": i['weight_uom'],
				"is_free_return": data_item['is_free_return'],
				"is_must_insurance": data_item['is_must_insurance'],
				"dimension": {
					"height": float(i['height']),
					"width":  float(i['width']),
					"length":  float(i['length'])
				},
				"custom_product_logistics": data_item['custom_product_logistics'],
				"annotations": data_item['annotations'],
				"etalase": data_item['etalase'],
				"pictures": [
					{
						"file_path": frappe.utils.get_url()+i['gambar_utama']
					}
				],
				"wholesale": [],
				"preorder": {},
				"videos": [],
				"variant":{
					"products":data_products,
					"selection":data_selection,
					"sizecharts":[]
				}
			}
		data.append(isi)
		frappe.msgprint(str(data))
		
		Product.edit_product(data_item['app_id'],data_item['shop_id'],data,token)
		frappe.msgprint("edit data berhasil !")	



@frappe.whitelist()
def add_product_variant():
	datas=frappe.db.get_list('Tokopedia Setting',filters={'enable_sync': '1'},fields=['app_id','shop_name','token','shop_id'])
	data_i = frappe.db.get_list('Item',filters={'disabled': 0,"item_group": "Tokopedia","is_sync_tokopedia": "1","has_variants":"1"},fields=['*'])
	for s in datas:
		data_pr = Product.get_all_product(s['app_id'],s['token'])
		for i in data_i:
			cek=0
			for item in data_pr['data']:
				if i['name'] == item['sku']:
					pass
				else:
					cek=cek+1
			if cek == len(data_pr['data']):
				frappe.msgprint(i['name']+"belum ada")
				data_v = frappe.db.get_list('Item',filters={"variant_of":i['name']},fields=['*'])
				get_var = frappe.db.get_list('Item Variant Attribute',filters={'parent': i['item_code']},fields=['*'])
				get_att = frappe.db.get_list('Item Variant Attribute',filters={'variant_of': i['item_code']},fields=['*'],order_by='creation asc')
				etalase = frappe.db.get_list('Daftar Etalase',filters={'parent': i['name'] },fields=['*'])
				spek = frappe.db.get_list('Spesifikasi Tokpedia',filters={'parent': i['name'] },fields=['*'])
				# get_val = frappe.db.sql("""SELECT DISTINCT attribute,attribute_value FROM `tabItem Variant Attribute` WHERE variant_of=i['item_code'] ORDER BY attribute ASC""")
				data_products=[]
				data_options=[]
				data_selection=[]
				data_stock=[]
				data_pictures=[]
				split_var=[]
				conter=0
				data_var=[]
				data_var1=[]
				data_var2=[]
				data_range=[]
				#singgele variant
				frappe.msgprint("Panjang attribute:"+str(len(get_var)))
				if len(get_var) == 1:
					frappe.msgprint("Masuk sini"+get_var[0]['attribute'])
					for var in get_att:
						# frappe.msgprint("Item code"+var['parent'])
						data_v = frappe.db.get_list('Item',filters={"item_code":var['parent']},fields=['*'])
						get_attval = frappe.get_value("Item Variant Attribute",{"parent" : var['parent']}, "attribute_value")
						get_abbr = frappe.get_value("Item Attribute Value",{"parent" : get_var[0]['attribute'], "attribute_value": get_attval}, "abbr")
						split_var=get_var[0]['attribute'].split("|")
						for j in data_v:
							if j['is_primary'] == 1:
								primary = True
							else:
								primary = False


							pictures={
									"file_path": frappe.utils.get_url()+j['gambar_utama']
								}

							products={
										"is_primary":primary,
										"status": j['status_item'],
										"price": int(j['standard_rate']),
										"stock":int(j['opening_stock']),
										"sku": j['item_code'],
										"combination":[conter],
										"pictures":[pictures]
									}
							data_products.append(products)
							data_stock.append(int(j['opening_stock']))
							tot_stock=sum(data_stock)
							conter=conter+1


							options={
										"hex_code":"",
										"unit_value_id":int(get_abbr),
										"value":get_attval
									}
							data_options.append(options)

					selection={
								"id":int(split_var[0]),
								"unit_id":int(split_var[1]),
								"options":data_options
							}
					data_selection.append(selection)
					frappe.msgprint(str(data_selection))

					for e in etalase:
						app_id = frappe.get_value("Tokopedia Setting",{"name": e['shop']}, "app_id")
						shop_id = frappe.get_value("Tokopedia Setting",{"name": e['shop']}, "shop_id")
						token = frappe.get_value("Tokopedia Setting",{"name": e['shop']}, "token")
						data1=[]
						data2=[]
						data3=[]
						d_spek=[]
						data =[]
						if e['logistic']:
							if ',' in e['logistic']:
								data1=e['logistic'].split(',')
								for l in data1:
									data2.append(l.split('-'))

								for log2 in data2:
									data3.append(int(log2[0]))
							else:
								data1.append(e['logistic'])
								for l in data1:
									data2.append(l.split('-'))

								for log2 in data2:
									data3.append(int(log2[0]))
						else:
							data3=[]

						if spek:
							for sp in spek:
								d_spek.append(sp['id'])

						if i['child2']:
							cat_id = i['child2']
						else:
							cat_id = i['child1']

						if i['child2']:
							cat_id = i['child2']
						else:
							cat_id = i['child1']

						if i['is_free_return'] == 0:
							f_return = False
						else :
							f_return = True

						if i['is_must_insurance'] == 0:
							insurance = False
						else :
							insurance = True

								
						isi ={
								"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
								"condition": i['condition_item'],
								"description": i['description'],
								"sku": i['item_code'], #tidak boleh ada spasi
								"price": int(i['standard_rate']),
								"status": i['status_item'],
								"stock": tot_stock,
								"min_order": int(i['min_order']),
								"category_id": int(cat_id),
								"price_currency": i['currency_item_tokopedia'],
								"weight": int(i['weight_per_unit']),
								"weight_unit": i['weight_uom'],
								"is_free_return": f_return,
								"is_must_insurance": insurance,
								"dimension": {
									"height": float(i['height']),
									"width":  float(i['width']),
									"length":  float(i['length'])
								},
								"custom_product_logistics": data3,
								"annotations": d_spek,
								"etalase": {
									"id": int(e['id']) #kode etalase
								},
								"pictures": [
									{
										"file_path": frappe.utils.get_url()+i['gambar_utama']
									}
								],
								"wholesale": [],
								"preorder": {},
								"videos": [],
								"variant":{
									"products":data_products,
									"selection":data_selection,
									"sizecharts":[]
								}
							}

						data.append(isi)
						frappe.msgprint(str(data))
						test = Product.create_product(app_id,shop_id,data,token)
						Product.create_product(app_id,shop_id,data,token)
						# frappe.msgprint(str(test['data']['success_rows_data'][0]['product_id']))
						# doc = frappe.get_doc("Item",i['name'])
						# doc.product_id = test['data']['success_rows_data'][0]['product_id']

						# doc.flags.ignore_permission=True
						# doc.save()
						frappe.msgprint("Cretae data berhasil !")

				elif len(get_var) == 2:
					frappe.msgprint("Masuki sini panjang dua")
					# dua variant
					for attb in get_att:
						data_var.append(attb['attribute_value'])
					frappe.msgprint(str(data_var))
					
					for var in get_var:
						get_abbr = frappe.db.get_list('Item Attribute Value',filters={'parent': var['attribute'], 'attribute_value':('in',(data_var))},fields=['*'])
						data_range.append(len(get_abbr))
						for abbr in get_abbr:
							options={
									"hex_code":"",
									"unit_value_id":int(abbr['abbr']),
									"value":abbr['attribute_value']
								}
							data_var1.append(options)
							if len(data_var1) == len(get_abbr):
								data_var2.append(data_var1)
								data_var1=[]
						split_var.append(var['attribute'].split("|"))
					frappe.msgprint(str(data_var2))
					frappe.msgprint(str(data_range))
					
					conter_var=0
					for sv in split_var:
						selection={
								"id":int(sv[0]),
								"unit_id":int(sv[1]),
								"options":data_var2[conter_var]
							}
						conter_var=conter_var+1
						data_selection.append(selection)
					#frappe.msgprint(str(data_selection))	
								
					data_com=[]
					for com1 in range(data_range[0]):
						for com2 in range(data_range[1]):
							data_com.append(str(com1)+','+str(com2))
					
					data_com2=[]
					for c1 in data_com:
						data_com2.append(c1.split(','))

					con1=[]
					con2=[]
					for c2 in data_com2:
						con1.append(c2[0])
						con2.append(c2[1])

					conter_ref=len(data_v)-1
					# frappe.msgprint("conter ref :"+str(conter_ref))
					for j in data_v:
						if j['is_primary'] == 1:
							primary = True
						else:
							primary = False


						pictures={
								"file_path": frappe.utils.get_url()+j['gambar_utama']
							}

						products={
									"is_primary":primary,
									"status": j['status_item'],
									"price": int(j['standard_rate']),
									"stock":int(j['opening_stock']),
									"sku": j['item_code'],
									"combination":[int(con1[conter]),int(con2[conter])],
									"pictures":[pictures]
								}
						data_products.append(products)
						data_stock.append(int(j['opening_stock']))
						tot_stock=sum(data_stock)
						conter=conter+1
						conter_ref=conter_ref-1
						# frappe.msgprint("conter ref :"+str(conter_ref))

					for e in etalase:
						app_id = frappe.get_value("Tokopedia Setting",{"name": e['shop']}, "app_id")
						shop_id = frappe.get_value("Tokopedia Setting",{"name": e['shop']}, "shop_id")
						token = frappe.get_value("Tokopedia Setting",{"name": e['shop']}, "token")
						data1=[]
						data2=[]
						data3=[]
						d_spek=[]
						data =[]
						if e['logistic']:
							if ',' in e['logistic']:
								data1=e['logistic'].split(',')
								for l in data1:
									data2.append(l.split('-'))

								for log2 in data2:
									data3.append(int(log2[0]))
							else:
								data1.append(e['logistic'])
								for l in data1:
									data2.append(l.split('-'))

								for log2 in data2:
									data3.append(int(log2[0]))
						else:
							data3=[]

						if spek:
							for sp in spek:
								d_spek.append(sp['id'])

						if i['child2']:
							cat_id = i['child2']
						else:
							cat_id = i['child1']

						if i['child2']:
							cat_id = i['child2']
						else:
							cat_id = i['child1']

						if i['is_free_return'] == 0:
							f_return = False
						else :
							f_return = True

						if i['is_must_insurance'] == 0:
							insurance = False
						else :
							insurance = True

								
						isi ={
								"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
								"condition": i['condition_item'],
								"description": i['description'],
								"sku": i['item_code'], #tidak boleh ada spasi
								"price": int(i['standard_rate']),
								"status": i['status_item'],
								"stock": tot_stock,
								"min_order": int(i['min_order']),
								"category_id": int(cat_id),
								"price_currency": i['currency_item_tokopedia'],
								"weight": int(i['weight_per_unit']),
								"weight_unit": i['weight_uom'],
								"is_free_return": f_return,
								"is_must_insurance": insurance,
								"dimension": {
									"height": float(i['height']),
									"width":  float(i['width']),
									"length":  float(i['length'])
								},
								"custom_product_logistics": data3,
								"annotations": d_spek,
								"etalase": {
									"id": int(e['id']) #kode etalase
								},
								"pictures": [
									{
										"file_path": frappe.utils.get_url()+i['gambar_utama']
									}
								],
								"wholesale": [],
								"preorder": {},
								"videos": [],
								"variant": {
									"products":data_products,
									"selection":data_selection,
									"sizecharts":[]
								}
							}

						data.append(isi)
						frappe.msgprint(str(data_selection))
						frappe.msgprint(str(data_products))
						frappe.msgprint(str(data))
						Product.create_product(app_id,shop_id,data,token)
						# test = Product.create_product(app_id,shop_id,data,token)
						# #Product.create_product(app_id,shop_id,data,token)
						# frappe.msgprint(str(test['data']['success_rows_data'][0]['product_id']))
						# doc = frappe.get_doc("Item",i['name'])
						# doc.product_id = test['data']['success_rows_data'][0]['product_id']

						# doc.flags.ignore_permission=True
						# doc.save()
						frappe.msgprint("Cretae data berhasil !")
			
			elif cek < len(data_pr['data']):
				frappe.msgprint(i['name']+"sudah ada di toko")

@frappe.whitelist()
def make_so(order_id):
	#Payment verified, order ready to process
	get_order = frappe.db.get_list('Tokopedia Orders',filters={'order_id': order_id },fields=['*'])
	# get_order = frappe.db.get_list('Tokopedia Orders',filters={'order_status': "Payment verified, order ready to process" },fields=['*'])
	for i in get_order:
		cust = frappe.get_value("Customer",{"name": i['customer_name'] + ' - (' + i['customer'] +')'}, "name")
		if cust:
			frappe.msgprint(i['customer_name'] + ' - (' + i['customer'] +')'+" sudah ada")
		else:
			docc = frappe.new_doc('Customer')
			docc.customer_name = i['customer_name'] + ' - (' + i['customer'] +')'
			docc.customer_type = 'Individual'

			docc.flags.ignore_permission=True
			docc.save()
			frappe.msgprint("buat customer"+i['customer_name'])

			doc = frappe.new_doc('Address')
			doc.address_title = i['customer_name'] + ' - (' + i['customer'] +')'
			doc.address_type = 'Personal'
			doc.is_primary_address = 1
			doc.address_line1 = i['recipient_address']

			doc.city = i['recipient_city']

			row = doc.append('links', {})
			row.link_doctype =  'Customer'
			row.link_name = i['customer_name'] + ' - (' + i['customer'] +')'

			doc.flags.ignore_permission=True
			doc.save()
			frappe.msgprint("buat alamt"+i['customer_name'])

		get_item = frappe.db.get_list('Tokopedia Orders Item',filters={'parent': i['name'] },fields=['*'])
		cek_so = frappe.get_value("Sales Order",{"marketplace_id": i['name']}, "name")
		if cek_so:
			frappe.msgprint("SO "+i['name']+" Sudah Ada !")
		else:
			today = date.today()
			doc = frappe.new_doc('Sales Order')
			doc.customer = i['customer_name'] + ' - (' + i['customer'] +')'
			doc.order_type = 'Sales'
			doc.delivery_date = add_days(today, +3)
			doc.marketplace = 'Tokopedia'
			doc.shop_name = i['shop_name']
			doc.marketplace_id = i['name']

			for j in get_item:
				row = doc.append('items', {})
				row.item_code = j['item_sku']
				row.qty = j['qty']
			
			doc.flags.ignore_permission=True
			doc.save()
			frappe.msgprint("Buat So "+ i['name'])

@frappe.whitelist()
def make_dn(order_id):
	get_order = frappe.db.get_list('Tokopedia Orders',filters={'order_id': order_id },fields=['*'])
	for i in get_order:
		# cust = frappe.get_value("Customer",{"name": i['customer_name'] + ' - (' + i['customer'] +')'}, "name")
		# if cust:
		# 	frappe.msgprint(i['customer_name'] + ' - (' + i['customer'] +')'+" sudah ada")
		# else:
		# 	docc = frappe.new_doc('Customer')
		# 	docc.customer_name = i['customer_name'] + ' - (' + i['customer'] +')'
		# 	docc.customer_type = 'Individual'

		# 	docc.flags.ignore_permission=True
		# 	docc.save()
		# 	frappe.msgprint("buat customer"+i['customer_name'])

		# 	doc = frappe.new_doc('Address')
		# 	doc.address_title = i['customer_name'] + ' - (' + i['customer'] +')'
		# 	doc.address_type = 'Personal'
		# 	doc.is_primary_address = 1
		# 	doc.address_line1 = i['recipient_address']

		# 	doc.city = i['recipient_city']

		# 	row = doc.append('links', {})
		# 	row.link_doctype =  'Customer'
		# 	row.link_name = i['customer_name'] + ' - (' + i['customer'] +')'

		# 	doc.flags.ignore_permission=True
		# 	doc.save()
		# 	frappe.msgprint("buat alamt"+i['customer_name'])

		get_item = frappe.db.get_list('Tokopedia Orders Item',filters={'parent': i['name'] },fields=['*'])
		cek_dn = frappe.get_value("Delivery Note",{"marketplace_id": i['name']}, "name")
		if cek_dn:
			frappe.msgprint("DN "+i['name']+" Sudah Ada !")
		else:
			today = date.today()
			doc = frappe.new_doc('Delivery Note')
			doc.customer = i['customer_name'] + ' - (' + i['customer'] +')'
			#doc.order_type = 'Sales'
			# doc.delivery_date = add_days(today, +2)
			doc.marketplace = 'Tokopedia'
			doc.shop_name = i['shop_name']
			doc.marketplace_id = i['name']

			for j in get_item:
				row = doc.append('items', {})
				row.item_code = j['item_sku']
				row.qty = j['qty']
			
			doc.flags.ignore_permission=True
			doc.save()
			frappe.msgprint("Buat DN "+ i['name'])

@frappe.whitelist()
def make_sinv_dn(doc,method):
	get_order = frappe.db.get_list('Tokopedia Orders',filters={'order_id': doc.marketplace_id},fields=['*'])
	dn = frappe.get_value("Delivery Note",{"marketplace_id": doc.marketplace_id}, "name")
	cek = frappe.get_value("Sales Invoice",{"marketplace_id": doc.marketplace_id}, "name")
	if cek:
		frappe.msgprint("Sinv"+order_id+"sudah ada")
	else:
		for i in get_order:
			request_pick_up(i['name'])
			get_item = frappe.db.get_list('Delivery Note Item',filters={'parent': dn },fields=['*'])
			cek_sinv = frappe.get_value("Sales Invoice",{"marketplace_id": i['order_id']}, "name")
			if cek_sinv:
				frappe.msgprint("SINV "+i['name']+" Sudah Ada !")
			else:
				today = date.today()
				docsinv = frappe.new_doc('Sales Invoice')
				docsinv.customer = doc.customer
				#doc.order_type = 'Sales'
				docsinv.due_date = add_days(today, +2)
				docsinv.marketplace = 'Tokopedia'
				docsinv.shop_name = i['shop_name']
				docsinv.marketplace_id = i['name']
				# docsinv.update_stock = 1
				docsinv.kurir = i['shipping_carrier']

				for j in get_item:
					row = docsinv.append('items', {})
					row.item_code = j['item_code']
					row.qty = j['qty']
				
				docsinv.flags.ignore_permission=True
				docsinv.save()
				frappe.msgprint("Buat SINV "+ i['name'])

@frappe.whitelist()
def make_sinv(order_id):
	get_order = frappe.db.get_list('Tokopedia Orders',filters={'order_id': order_id },fields=['*'])
	cek = frappe.get_value("Sales Invoice",{"marketplace_id": order_id}, "name")
	if cek:
		frappe.msgprint("Sinv"+order_id+"sudah ada")
	else:
		for i in get_order:
			cust = frappe.get_value("Customer",{"name": i['customer_name'] + ' - (' + i['customer'] +')'}, "name")
			if cust:
				frappe.msgprint(i['customer_name'] + ' - (' + i['customer'] +')'+" sudah ada")
			else:
				docc = frappe.new_doc('Customer')
				docc.customer_name = i['customer_name'] + ' - (' + i['customer'] +')'
				docc.customer_type = 'Individual'

				docc.flags.ignore_permission=True
				docc.save()
				frappe.msgprint("buat customer"+i['customer_name'])

				doc = frappe.new_doc('Address')
				doc.address_title = i['customer_name'] + ' - (' + i['customer'] +')'
				doc.address_type = 'Personal'
				doc.is_primary_address = 1
				doc.address_line1 = i['recipient_address']

				doc.city = i['recipient_city']

				row = doc.append('links', {})
				row.link_doctype =  'Customer'
				row.link_name = i['customer_name'] + ' - (' + i['customer'] +')'

				doc.flags.ignore_permission=True
				doc.save()
				frappe.msgprint("buat alamt"+i['customer_name'])

			get_item = frappe.db.get_list('Tokopedia Orders Item',filters={'parent': i['name'] },fields=['*'])
			cek_sinv = frappe.get_value("Sales Invoice",{"marketplace_id": i['name']}, "name")
			if cek_sinv:
				frappe.msgprint("SINV "+i['name']+" Sudah Ada !")
			else:
				today = date.today()
				doc = frappe.new_doc('Sales Invoice')
				doc.customer = i['customer_name'] + ' - (' + i['customer'] +')'
				#doc.order_type = 'Sales'
				doc.due_date = add_days(today, +2)
				doc.marketplace = 'Tokopedia'
				doc.shop_name = i['shop_name']
				doc.marketplace_id = i['name']
				doc.update_stock = 1
				doc.kurir = i['shipping_carrier']

				for j in get_item:
					row = doc.append('items', {})
					row.item_code = j['item_sku']
					row.qty = j['qty']
				
				doc.flags.ignore_permission=True
				doc.save()
				frappe.msgprint("Buat SINV "+ i['name'])

@frappe.whitelist()
def request_pick_up(order_id):
	#Payment verified, order ready to process
	get_order = frappe.db.get_list('Sales Order',filters={'marketplace_id': order_id },fields=['*'])
	for i in get_order:
		data = frappe.db.get_list('Sales Order Item',filters={'parent': i['name'] },fields=['*'])
		app_id = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "app_id")
		shop_id = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "shop_id")
		token = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "token")
		count = 0
		for j in data:
			frappe.msgprint(j['item_code'])
			stock = frappe.get_value("Bin",{"item_code": j['item_code']}, "actual_qty")
			if j['qty'] <= stock:
				frappe.msgprint("Stock Ada")
				count = count + 1
			else :
				frappe.msgprint("Stock Habis/ Kurang")

		# frappe.throw("Stock Habis/ Kurang")
		frappe.msgprint(str(count))	
		if count == len(data):
			frappe.msgprint("Request Pick Up")
			# url = "https://fs.tokopedia.net/inventory/v1/fs/"+app_id+"/pick-up"
			# payload = json.dumps({
			# 	"order_id": order_id,
			# 	"shop_id": shop_id
			# })
			# headers = {
	 	# 		'Authorization': 'Bearer '+ token
			# }
			# response = requests.request("POST", url, headers=headers, data=payload)
			# print(response.text)
			# frappe.msgprint(str(response.text))
		else:
			frappe.msgprint("Cek Stock")

@frappe.whitelist()
def request_pick_up_sinv(doc,method):
	if doc.order_via not in "Shopee Tokopedia Bukalapak":
		return
	#Payment verified, order ready to process
	get_order = frappe.db.get_list('Tokopedia Orders',filters={'order_id': doc.marketplace_id },fields=['*'])
	cek_shop = frappe.get_value("Tokopedia Setting",{"name": doc.shop_name}, "make_sinv")
	if cek_shop == 1:
		for i in get_order:
			data = frappe.db.get_list('Tokopedia Orders Item',filters={'parent': i['name'] },fields=['*'])
			app_id = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "app_id")
			shop_id = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "shop_id")
			token = frappe.get_value("Tokopedia Setting",{"name": i['shop_name']}, "token")
			count = 0
			for j in data:
				frappe.msgprint(j['item_sku'])
				stock = frappe.get_value("Bin",{"item_code": j['item_sku']}, "actual_qty")
				if j['qty'] <= stock:
					frappe.msgprint("Stock Ada")
					count = count + 1
				else :
					frappe.msgprint("Stock Habis/ Kurang")

			# frappe.throw("Stock Habis/ Kurang")
			frappe.msgprint(str(count))	
			if count == len(data):
				frappe.msgprint("Request Pick Up")
				# url = "https://fs.tokopedia.net/inventory/v1/fs/"+app_id+"/pick-up"
				# payload = json.dumps({
				# 	"order_id": order_id,
				# 	"shop_id": shop_id
				# })
				# headers = {
		 	# 		'Authorization': 'Bearer '+ token
				# }
				# response = requests.request("POST", url, headers=headers, data=payload)
				# print(response.text)
				# frappe.msgprint(str(response.text))
			else:
				frappe.msgprint("Cek Stock")				

			


		
