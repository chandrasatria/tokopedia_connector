// Copyright (c) 2021, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Get Status Order', {
	refresh: function(frm) {
		cur_frm.cscript.get_order_status = function(doc) {
            frappe.call({
                method: "tokopedia_connector.tokopedia_connector.tokopedia.get_data_manual",
                args: {
                        date: cur_frm.doc.date
                }, 
                callback: function(r) {
                    
                }
            })
        }
	}
});
