// Copyright (c) 2021, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Push and Pull Item Tokopedia', {
	refresh: function(frm) {
		cur_frm.cscript.get_product = function(doc){
			frappe.call({
            method: "tokopedia_connector.tokopedia_connector.tokopedia.get_product",
            args: {
            	shop: cur_frm.doc.shop
            }, 
            callback: function(r) {
                
            }
        	})
		}
		
		cur_frm.cscript.add_and_update_product = function(doc){
			frappe.call({
            method: "tokopedia_connector.tokopedia_connector.tokopedia.crate_product", 
            callback: function(r) {
                
            }
        	})
		}
	}
});
