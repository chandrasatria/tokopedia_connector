# -*- coding: utf-8 -*-
# Copyright (c) 2021, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from tokopedia_connector.tokopedia_connector.api.order.order import Order
from tokopedia_connector.tokopedia_connector.tokopedia import Tokopedia
import json
from tokopedia_connector.tokopedia_connector.api.product.product import Product
from tokopedia_connector.tokopedia_connector.api.campaign.campaign import Campaign
from datetime import date
from frappe.utils import flt, rounded, add_months,add_days, nowdate, getdate
import time
import datetime
import subprocess


class MarketplaceItemTokopedia(Document):
	def on_update(self):
		frappe.msgprint("on_update")
		# insert no variant
		if self.type == 'Product' and not self.product_id:
			frappe.msgprint("insert no variant")
			cek_bagi = frappe.db.get_list('Marketplace Item Tokopedia',filters={'item_code': self.item_code},fields=['*'])
			banding = 0
			for cb in cek_bagi:
				banding = banding + cb['bobot']
			bs = 100 - banding
			if banding <= 100:
				data_i = frappe.db.get_list('Item',filters={'name': self.item_code},fields=['*'])
				token = frappe.get_value("Tokopedia Setting",{"name": self.shop}, "token")
				data = []

				cat_id=0
				if self.child2:
					cat_id = int(self.child2)
				else:
					cat_id = int(self.child1)

				if self.is_free_return == 1:
					f_return = True
				else:
					f_return = False

				if self.is_must_insurance == 1:
					insurance = True
				else:
					insurance = False

				logistic=[]	
				if self.get('list_logistic_market'):
					# frappe.msgprint("tes 123")
					for log in self.get('list_logistic_market'):
						logistic.append(int(log.id))
				else:
					logistic=[]

				d_spek=[]	
				if self.get('spesifikasi_tokpedia'):
					# frappe.msgprint("tes 123")
					for spek in self.get('spesifikasi_tokpedia'):
						d_spek.append(spek.id)
				else:
					d_spek=[]

				for i in data_i:
					price= frappe.get_value("Item Price",{"item_code": i['item_code']}, "price_list_rate")
					stock= frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
					if self.bobot == 0:
						bagi = stock
					else:
						bagi = stock * self.bobot / 100
					if not stock:
						bagi = 1
					
					images=[]

					if '/files' in i['gambar_utama']:
						img = {
							"file_path": frappe.utils.get_url()+i['gambar_utama']
						}
					else:
						img = {
							"file_path": i['gambar_utama']
						}

					images.append(img)

					if i['gambar_depan']:
						if '/files' in i['gambar_depan']:
							img1 = {
								"file_path": frappe.utils.get_url()+i['gambar_depan']
							}
						else:
							img1 = {
								"file_path": i['gambar_depan']
							}
						images.append(img1)

					if i['gambar_atas']:
						if '/files' in i['gambar_atas']:
							img2 = {
								"file_path": frappe.utils.get_url()+i['gambar_atas']
							}
						else:
							img2 = {
								"file_path": i['gambar_atas']
							}
						images.append(img2)
					

					if i['gambar_samping']:
						if '/files' in i['gambar_samping']:
							img3 = {
								"file_path": frappe.utils.get_url()+i['gambar_samping']
							}
						else:
							img3 = {
								"file_path": i['gambar_samping']
							}
						images.append(img3)
					
					if i['gambar_detail']:
						if '/files' in i['gambar_detail']:
							img4 = {
								"file_path": frappe.utils.get_url()+i['gambar_detail']
							}
						else:
							img4 = {
								"file_path": i['gambar_detail']
							}
						images.append(img4)

					frappe.msgprint(str(images))

					if self.new_name == 1:
						name = self.item_name
					else:
						name = i['item_name']

					isi ={
							"name": name, # karakter tidak boleh labih dari 70 tidak boleh sama
							"condition": self.condition_item,
							"description": i['description'],
							"sku": self.item_code, #tidak boleh ada spasi
							"price": int(price),
							"status": self.status_item,
							"stock": int(bagi),
							"min_order": self.min_order,
							"category_id": cat_id,
							"price_currency": self.currency_item_tokopedia,
							"weight": int(i['weight_per_unit']),
							"weight_unit": i['weight_uom'],
							"is_free_return": f_return,
							"is_must_insurance": insurance,
							"dimension": {
								"height": float(i['height']),
								"width":  float(i['width']),
								"length":  float(i['length'])
							},
							"custom_product_logistics": logistic,
							"annotations": d_spek,
							"etalase": {
								"id" : int(self.etalase)
							},
							"pictures": images,
							"wholesale": [],
							"preorder": {},
							"videos": []
						}
					
					data.append(isi)
					
					test = Product.create_product(self.app_id,self.shop_id,data,token)
					self.product_id = test['data']['success_rows_data'][0]['product_id']

					self.flags.ignore_permission=True
					self.save()
				else:
					frappe.throw("bobot lebih "+str(abs(bs))+" dari 100")
		
		if self.type == 'Template' and not self.product_id:
			frappe.msgprint("coba inser variant")
			data_i = frappe.db.get_list('Item',filters={'name': self.item_code},fields=['*'])
			token = frappe.get_value("Tokopedia Setting",{"name": self.shop}, "token")
			data=[]
			data_products=[]
			data_selection=[]
			data_selection2=[]
			data_options=[]
			data_options2=[]
			union_selection=[]
			conter=0

			con_opt=0
			for opt1 in self.get('table_variant_1'):
				options={
						"hex_code":"",
						"unit_value_id":int(opt1.id),
						"value": opt1.value
						}
				con_opt=con_opt+1
				data_options.append(options)

			con_opt2=0
			for opt2 in self.get('table_variant_2'):
				options={
							"hex_code":"",
							"unit_value_id":int(opt2.id),
							"value": opt2.value
						}
				con_opt2=con_opt2+1
				data_options2.append(options)
			
			
			frappe.msgprint(str(data_options))
			frappe.msgprint(str(data_options2))

			variant_1= self.variant_1.split('|')
			frappe.msgprint(str(variant_1))

			
			selection1={
				"id":int(variant_1[0]),
				"unit_id":int(variant_1[1]),
				"options": data_options
			}
			data_selection.append(selection1)

			if self.variant_2:
				variant_2= self.variant_2.split('|')
				
				selection2 = {
					"id":int(variant_2[0]),
					"unit_id":int(variant_2[1]),
					"options": data_options2
				}
				
				data_selection.append(selection2)
			

			frappe.msgprint("selesction"+str(data_selection))
			# frappe.msgprint("cbbb"+str(len(self.table_variant_1)))
			com=[]
			for gv1 in range(len(self.table_variant_1)):
				for gv2 in range(len(self.table_variant_2)):
					productsv= [gv1,gv2]
					com.append(productsv)
					# frappe.msgprint("combination"+str(productsv))

			
			if self.variant_2:
				# dua kombinasi
				for dv in self.get('tabel_gabung_variant'):
					if dv.primary == 1:
						primary = True
					else:
						primary = False
					
					price= frappe.get_value("Item Price",{"item_code": dv.item_code}, "price_list_rate")
					stock= frappe.get_value("Bin",{"item_code": dv.item_code}, "actual_qty")
					if not stock:
						stock=1
					else:
						stock
					images = frappe.get_value("Item",{"name": dv.item_code}, "gambar_utama")
					# frappe.msgprint(str((images)))
					if '/files' in images:
						pictures={
							"file_path": frappe.utils.get_url()+images
						}
					else:
						pictures={
							"file_path": images
						}

					products={
							"is_primary":primary,
							"status": self.status_item,
							"price": int(price),
							"stock": int(stock),
							"sku": dv.item_code,
							"combination":com[conter],
							"pictures": [pictures]
					}
					conter=conter+1
					data_products.append(products)
				frappe.msgprint(str(data_products))
			else: 
				# 1 combinasis
				for dv in self.get('tabel_gabung_variant'):
					if dv.primary == 1:
						primary = True
					else:
						primary = False
					
					price= frappe.get_value("Item Price",{"item_code": dv.item_code}, "price_list_rate")
					stock= frappe.get_value("Bin",{"item_code": dv.item_code}, "actual_qty")
					images = frappe.get_value("Item",{"name": dv.item_code}, "gambar_utama")
					# frappe.msgprint(str((images)))
					
					if '/files' in images:
						pictures={
							"file_path": frappe.utils.get_url()+images
						}
					else:
						pictures={
							"file_path": images
						}

					products={
							"is_primary":primary,
							"status": self.status_item,
							"price": int(price),
							"stock": int(stock),
							"sku": dv.item_code,
							"combination":[conter],
							"pictures": [pictures]
					}
					conter=conter+1
					data_products.append(products)
				frappe.msgprint(str(data_products))

			cat_id=0
			if self.child2:
				cat_id = int(self.child2)
			else:
				cat_id = int(self.child1)

			if self.is_free_return == 1:
				f_return = True
			else:
				f_return = False

			if self.is_must_insurance == 1:
				insurance = True
			else:
				insurance = False

			logistic=[]	
			if self.get('list_logistic_market'):
				# frappe.msgprint("tes 123")
				for log in self.get('list_logistic_market'):
					logistic.append(int(log.id))
			else:
				logistic=[]

			d_spek=[]	
			if self.get('spesifikasi_tokpedia'):
				# frappe.msgprint("tes 123")
				for spek in self.get('spesifikasi_tokpedia'):
					d_spek.append(spek.id)
			else:
				d_spek=[]

			for i in data_i:
				price= frappe.get_value("Item Price",{"item_code": i['item_code']}, "price_list_rate")
				stock= frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
				if not stock:
					stock=1
				else:
					stock
				if not price:
					price = 0
				
				if '/files' in i['gambar_utama']:
					images = {
						"file_path": frappe.utils.get_url()+i['gambar_utama']
					}
				else:
					images = {
						"file_path": i['gambar_utama']
					}

				isi = {
						"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
						"condition": self.condition_item,
						"description": i['description'],
						"sku": self.item_code, #tidak boleh ada spasi
						"price": int(price),
						"status": self.status_item,
						"stock": int(stock),
						"min_order": self.min_order,
						"category_id": cat_id,
						"price_currency": self.currency_item_tokopedia,
						"weight": int(i['weight_per_unit']),
						"weight_unit": i['weight_uom'],
						"is_free_return": f_return,
						"is_must_insurance": insurance,
						"dimension": {
							"height": float(i['height']),
							"width":  float(i['width']),
							"length":  float(i['length'])
						},
						"custom_product_logistics": logistic,
						"annotations": d_spek,
						"etalase": {
							"id": int(self.etalase)
						},
						"pictures": [images],
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
				
				test = Product.create_product(self.app_id,self.shop_id,data,token)
				self.product_id = test['data']['success_rows_data'][0]['product_id']
				self.flags.ignore_permission=True
				self.save()
				frappe.msgprint("add variant berhasil")		


		# ecit variant
		if self.type == 'Template' and self.product_id and self.item_code:
			frappe.msgprint("edit VAraiant")
			data_i = frappe.db.get_list('Item',filters={'name': self.item_code},fields=['*'])
			token = frappe.get_value("Tokopedia Setting",{"name": self.shop}, "token")
			data=[]
			data_products=[]
			data_selection=[]
			data_selection2=[]
			data_options=[]
			data_options2=[]
			union_selection=[]
			conter=0

			con_opt=0
			for opt1 in self.get('table_variant_1'):
				options={
						"hex_code":"",
						"unit_value_id":int(opt1.id),
						"value": opt1.value
						}
				con_opt=con_opt+1
				data_options.append(options)

			con_opt2=0
			for opt2 in self.get('table_variant_2'):
				options={
							"hex_code":"",
							"unit_value_id":int(opt2.id),
							"value": opt2.value
						}
				con_opt2=con_opt2+1
				data_options2.append(options)
			
			
			frappe.msgprint(str(data_options))
			frappe.msgprint(str(data_options2))

			variant_1= self.variant_1.split('|')
			frappe.msgprint(str(variant_1))

			
			selection1={
				"id":int(variant_1[0]),
				"unit_id":int(variant_1[1]),
				"options": data_options
			}
			data_selection.append(selection1)

			if self.variant_2:
				variant_2= self.variant_2.split('|')
				
				selection2 = {
					"id":int(variant_2[0]),
					"unit_id":int(variant_2[1]),
					"options": data_options2
				}
				
				data_selection.append(selection2)
			

			frappe.msgprint("selesction"+str(data_selection))
			# frappe.msgprint("cbbb"+str(len(self.table_variant_1)))
			com=[]
			for gv1 in range(len(self.table_variant_1)):
				for gv2 in range(len(self.table_variant_2)):
					productsv= [gv1,gv2]
					com.append(productsv)
					# frappe.msgprint("combination"+str(productsv))

			
			if self.variant_2:
				# dua kombinasi
				for dv in self.get('tabel_gabung_variant'):
					if dv.primary == 1:
						primary = True
					else:
						primary = False
					
					price= frappe.get_value("Item Price",{"item_code": dv.item_code}, "price_list_rate")
					stock= frappe.get_value("Bin",{"item_code": dv.item_code}, "actual_qty")
					if not stock:
						stock = 1 
					images = frappe.get_value("Item",{"name": dv.item_code}, "gambar_utama")
					frappe.msgprint(str((images)))
					
					if '/files' in images:
						pictures={
							"file_path": frappe.utils.get_url()+images
						}
					else:
						pictures={
							"file_path": images
						}

					products={
							"is_primary":primary,
							"status": self.status_item,
							"price": int(price),
							"stock": int(stock),
							"sku": dv.item_code,
							"combination":com[conter],
							"pictures": [pictures]
					}
					conter=conter+1
					data_products.append(products)
				frappe.msgprint(str(data_products))
			else: 
				# 1 combinasis
				for dv in self.get('tabel_gabung_variant'):
					if dv.primary == 1:
						primary = True
					else:
						primary = False
					
					price= frappe.get_value("Item Price",{"item_code": dv.item_code}, "price_list_rate")
					stock= frappe.get_value("Bin",{"item_code": dv.item_code}, "actual_qty")
					if not stock:
						stock = 1
					images = frappe.get_value("Item",{"name": dv.item_code}, "gambar_utama")
					# frappe.msgprint(str((images)))
					
					if '/files' in images:
						pictures={
							"file_path": frappe.utils.get_url()+images
						}
					else:
						pictures={
							"file_path": images
						}


					#frappe.msgprint("Picture ::"+str(pictures))

					products={
							"is_primary":primary,
							"status": self.status_item,
							"price": int(price),
							"stock": int(stock),
							"sku": dv.item_code,
							"combination":[conter],
							"pictures": [pictures]
					}
					conter=conter+1
					data_products.append(products)
				frappe.msgprint(str(data_products))

			cat_id=0
			if self.child2:
				cat_id = int(self.child2)
			else:
				cat_id = int(self.child1)

			if self.is_free_return == 1:
				f_return = True
			else:
				f_return = False

			if self.is_must_insurance == 1:
				insurance = True
			else:
				insurance = False

			logistic=[]	
			if self.get('list_logistic_market'):
				# frappe.msgprint("tes 123")
				for log in self.get('list_logistic_market'):
					logistic.append(int(log.id))
			else:
				logistic=[]

			d_spek=[]	
			if self.get('spesifikasi_tokpedia'):
				# frappe.msgprint("tes 123")
				for spek in self.get('spesifikasi_tokpedia'):
					d_spek.append(spek.id)
			else:
				d_spek=[]

			for i in data_i:
				price= frappe.get_value("Item Price",{"item_code": i['item_code']}, "price_list_rate")
				stock= frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
				if not stock:
					stock = 1
				if not price:
					price = 0
				
				if '/files' in i['gambar_utama']:
					images = {
						"file_path": frappe.utils.get_url()+i['gambar_utama']
					}
				else:
					images = {
						"file_path": i['gambar_utama']
					}

				isi = {
						"id": int(self.product_id),
						"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
						"condition": self.condition_item,
						"description": i['description'],
						"sku": self.item_code, #tidak boleh ada spasi
						"price": int(price),
						"status": self.status_item,
						"stock": int(stock),
						"min_order": self.min_order,
						"category_id": cat_id,
						"price_currency": self.currency_item_tokopedia,
						"weight": int(i['weight_per_unit']),
						"weight_unit": i['weight_uom'],
						"is_free_return": f_return,
						"is_must_insurance": insurance,
						"dimension": {
							"height": float(i['height']),
							"width":  float(i['width']),
							"length":  float(i['length'])
						},
						"custom_product_logistics": logistic,
						"annotations": d_spek,
						"etalase": {
							"id": int(self.etalase)
						},
						"pictures": [images],
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
				
				Product.edit_product(self.app_id,self.shop_id,data,token)
				frappe.msgprint("edit data berhasil !")	
			
		# edit no variant
		if self.type == 'Product' and self.product_id and self.item_code:
			cek_bagi = frappe.db.get_list('Marketplace Item Tokopedia',filters={'item_code': self.item_code},fields=['*'])
			banding = 0
			for cb in cek_bagi:
				banding = banding + cb['bobot']
			bs = 100 - banding
			if banding <= 100:
				data_i = frappe.db.get_list('Item',filters={'name': self.item_code},fields=['*'])
				token = frappe.get_value("Tokopedia Setting",{"name": self.shop}, "token")
				data = []
				
				cat_id=0
				if self.child2:
					cat_id = int(self.child2)
				else:
					cat_id = int(self.child1)

				if self.is_free_return == 1:
					f_return = True
				else:
					f_return = False

				if self.is_must_insurance == 1:
					insurance = True
				else:
					insurance = False

				logistic=[]	
				if self.get('list_logistic_market'):
					# frappe.msgprint("tes 123")
					for log in self.get('list_logistic_market'):
						logistic.append(int(log.id))
				else:
					logistic=[]

				d_spek=[]	
				if self.get('spesifikasi_tokpedia'):
					# frappe.msgprint("tes 123")
					for spek in self.get('spesifikasi_tokpedia'):
						d_spek.append(spek.id)
				else:
					d_spek=[]

				for i in data_i:
					price= frappe.get_value("Item Price",{"item_code": i['item_code']}, "price_list_rate")
					stock= frappe.get_value("Bin",{"item_code": i['item_code']}, "actual_qty")
					if self.bobot == 0:
						bagi = stock
					else:
						bagi = stock * self.bobot / 100
					if not stock:
						bagi = 1
					
					images=[]

					if '/files' in i['gambar_utama']:
						img = {
							"file_path": frappe.utils.get_url()+i['gambar_utama']
						}
					else:
						img = {
							"file_path": i['gambar_utama']
						}

					images.append(img)

					if i['gambar_depan']:
						if '/files' in i['gambar_depan']:
							img1 = {
								"file_path": frappe.utils.get_url()+i['gambar_depan']
							}
						else:
							img1 = {
								"file_path": i['gambar_depan']
							}
						images.append(img1)

					if i['gambar_atas']:
						if '/files' in i['gambar_atas']:
							img2 = {
								"file_path": frappe.utils.get_url()+i['gambar_atas']
							}
						else:
							img2 = {
								"file_path": i['gambar_atas']
							}
						images.append(img2)
					

					if i['gambar_samping']:
						if '/files' in i['gambar_samping']:
							img3 = {
								"file_path": frappe.utils.get_url()+i['gambar_samping']
							}
						else:
							img3 = {
								"file_path": i['gambar_samping']
							}
						images.append(img3)
					
					if i['gambar_detail']:
						if '/files' in i['gambar_detail']:
							img4 = {
								"file_path": frappe.utils.get_url()+i['gambar_detail']
							}
						else:
							img4 = {
								"file_path": i['gambar_detail']
							}
						images.append(img4)

					frappe.msgprint(str(images))

					isi ={
							"id": int(self.product_id),
							"name": i['item_name'], # karakter tidak boleh labih dari 70 tidak boleh sama
							"condition": self.condition_item,
							"description": i['description'],
							"sku": self.item_code, #tidak boleh ada spasi
							"price": int(price),
							"status": self.status_item,
							"stock": int(bagi),
							"min_order": self.min_order,
							"category_id": cat_id,
							"price_currency": self.currency_item_tokopedia,
							"weight": int(i['weight_per_unit']),
							"weight_unit": i['weight_uom'],
							"is_free_return": f_return,
							"is_must_insurance": insurance,
							"dimension": {
								"height": float(i['height']),
								"width":  float(i['width']),
								"length":  float(i['length'])
							},
							"custom_product_logistics": logistic,
							"annotations": d_spek,
							"etalase": {
								"id" : int(self.etalase)
							},
							"pictures": images,
							"wholesale": [],
							"preorder": {},
							"videos": []
						}
					
					data.append(isi)

					# start = int(time.mktime(datetime.datetime.strptime(str(self.start_time_unix), "%Y-%m-%d %H:%M:%S").timetuple()))
					# end = int(time.mktime(datetime.datetime.strptime(str(self.end_time_unix), "%Y-%m-%d %H:%M:%S").timetuple()))
					
					# slash_price = []
					# slash = {
					# 	"product_id": int(self.product_id),
					# 	"discounted_price": self.discounted_price,
					# 	"discount_percentage": self.discount_percentage,
					# 	"start_time_unix": start,
					# 	"end_time_unix": end,
					# 	"max_order": self.max_order 
					# }
					# slash_price.append(slash)

					# Campaign.add_slash_price(self.app_id,self.shop_id,token,slash_price)
					Product.edit_product(self.app_id,self.shop_id,data,token)
					frappe.msgprint("edit data berhasil !")
					frappe.msgprint("bobot yang kurang "+str(bs)+" dari 100")
			else:
				frappe.throw("bobot lebih "+str(abs(bs))+" dari 100")
			
			# Tokopedia.edit_product_coba(self.item_code,data_item)
		

		
	# 	if self.type == 'Template':
	# 		frappe.msgprint("On Update")
			# tokopedia_connector.tokopedia.edit_item_var(item_code,data_item,data_variant)
		# data_i = frappe.db.get_list('Item',filters={'name': self.item_code},fields=['*'])
		# data_variant_link = frappe.db.get_list('Tabel Gabung Variant',filters={'parent': self.name},fields=['*'],order_by='idx asc')
		# token = frappe.get_value("Tokopedia Setting",{"name": self.shop}, "token")
		# data=[]
		# data_products=[]
		# data_selection=[]
		# data_selection2=[]
		# data_options=[]
		# data_options2=[]
		# union_selection=[]
		# conter=0

		# con_opt=0
		# for opt1 in self.get('table_variant_1'):
		# 	options={
		# 			"hex_code":"",
		# 			"unit_value_id":int(opt1.id),
		# 			"value": opt1.value
		# 			}
		# 	con_opt=con_opt+1
		# 	data_options.append(options)

		# con_opt2=0
		# for opt2 in self.get('table_variant_2'):
		# 	options={
		# 				"hex_code":"",
		# 				"unit_value_id":int(opt2.id),
		# 				"value": opt2.value
		# 			}
		# 	con_opt2=con_opt2+1
		# 	data_options2.append(options)
		
		
		# frappe.msgprint(str(data_options))
		# frappe.msgprint(str(data_options2))

		# variant_1= self.variant_1.split('|')
		# variant_2= self.variant_2.split('|')
		# frappe.msgprint(str(variant_1))

		# for sel in variant_1:
		# 	frappe.msgprint(sel[0])
		# 	selection1={
		# 		"id":int(sel[0]),
		# 		"unit_id":int(sel[1]),
		# 		"options": data_options
		# 	}
		# data_selection.append(selection1)

		# if self.variant_2:
		# 	for sel2 in variant_2:
		# 		selection2 = {
		# 			"id":int(sel2[0]),
		# 			"unit_id":int(sel2[1]),
		# 			"options": data_options2
		# 		}
		# 	data_selection.append(selection2)
		

		# frappe.msgprint("selesction"+str(data_selection))

