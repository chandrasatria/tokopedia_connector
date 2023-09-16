// Copyright (c) 2021, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tokopedia Setting', {
	refresh: function(frm) {

	},
	add_etalase(frm){
		frappe.msgprint('cek123')
		frappe.call({
                 method: "tokopedia_connector.tokopedia_connector.tokopedia.get_etalase2",
                 args: {
                    app_id: cur_frm.doc.app_id,
                    shop_id: cur_frm.doc.shop_id,
                    token: cur_frm.doc.token
                 },
                 callback: function(r) {
        
                }
        });
	}
});

