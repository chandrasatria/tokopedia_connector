frappe.ui.form.on('Marketplace Item Tokopedia', {
    refresh(frm) {
        // your code here
        
        cur_frm.set_query("etalase", function() {
                return {
                    filters: {
                        'name_shop': cur_frm.doc.shop
                    }
                }
        });

        /*cur_frm.set_query("item_code", function() {
                return {
                    filters: {
                        'item_group': cur_frm.doc.shop+" Tokopedia"
                    }
                }
        });*/

        cur_frm.set_query("child1", function() {
                return {
                    filters: {
                        'id_parent': cur_frm.doc.id_parent
                    }
                }
        });
            
        cur_frm.set_query("child2", function() {
            return {
                filters: {
                    'parent': cur_frm.doc.child1
                }
            }
        });

        cur_frm.set_query("template", function() {
            return {
                filters: {
                    'type': "Template"
                }
            }
        });

        frm.fields_dict['menu_etalase'].grid.get_field('id').get_query = function(doc, cdt, cdn) {
        var child = locals[cdt][cdn];
        // console.log(child);
            return {    
                filters:[
                    ['name_shop', '=', cur_frm.doc.shop]
                ]
            }
        }

        cur_frm.cscript.add_etalase = function(doc) {
            let field = [];
            field.push({
                label: "List Etalase",
                fieldname: 'etalase',
                fieldtype: 'Link',
                options: 'List Etalase',
                filters: {
                    'name_shop' : cur_frm.doc.shop
                }
            });
            let d = new frappe.ui.Dialog({
                    title: 'Etalase',
                    fields: field,
                    primary_action_label: 'Submit',
                    primary_action(values) {
                        console.log(values);
                   
                        var child = cur_frm.add_child("menu_etalase");
            
                        child.id = values['etalase']
                        cur_frm.refresh_field("menu_etalase")
                        d.hide();
                    }

                });
                
            d.show();
        }

        cur_frm.cscript.add_logistic = function(doc) {
            frappe.call({method:'tokopedia_connector.tokopedia_connector.api.logistic.logistic.get_active_courier',
                        args: {
                            app_id: cur_frm.doc.app_id,
                            token: cur_frm.doc.token,
                            shop_id: cur_frm.doc.shop_id,
                        },callback: function(r) {
                            //console.log(r)
                            let data=[]
                            let field = [];
                            // let dataSudahAda = e.view.cur_frm.selected_doc.logistic
                            for (let i = 0;i < r.message.data.Shops[0].ShipmentInfos.length;i++) {
                                data.push(r.message.data.Shops[0].ShipmentInfos[i].ShipmentID+"|"+r.message.data.Shops[0].ShipmentInfos[i].ShipmentName)
                                //console.log(data)
                            }
                            //frappe.msgprint(data)
                          
                            field.push({
                                label: "List Logistic",
                                fieldname: 'logistic',
                                fieldtype: 'Select',
                                options: data
                            });
           
                            let d = new frappe.ui.Dialog({
                                        title: 'Logistic Tokopedia ',
                                        fields: field,
                                        primary_action_label: 'Submit',
                                        primary_action(values) {
                                            console.log(values);
                                            
                                            let dataValue = values['logistic']
                                            let coba =[]
                                            coba = dataValue.split("|")

                                            var child = cur_frm.add_child("list_logistic_market");
                                
                                            child.id = coba[0]
                                            child.logistic_name = coba[1]
                                            cur_frm.refresh_field("list_logistic_market")

                                            d.hide();
                                        }

                                    });
                                    
                            d.show();
                        }                      
                });
        }

        cur_frm.cscript.speksifikasi = function(doc) {
            frappe.call({
                    method: "tokopedia_connector.tokopedia_connector.api.product.product.get_product_annotation", 
                    args: {
                        cat: cur_frm.doc.child2
                    },
                    callback: function(r) {
                        let dataField = []
                        
                        for (let i = 0; i < r.message.data.length; i++) {
                            console.log(r.message.data[i].variant)
                            let value =[]
                            for(let j = 0; j < r.message.data[i].values.length; j++){
                                //console.log(r.message.data[i].values[j].name)
                                value.push(r.message.data[i].values[j].id+"|"+r.message.data[i].values[j].name)
                            }
                        console.log(value)
                        dataField.push({
                            label: r.message.data[i].variant,
                            fieldname: 'field_' + i,
                            fieldtype: 'Select',
                            options: value
                        })
                        }
                        let hasil=[]
                        let d = new frappe.ui.Dialog({
                            title: 'Tokopedia Spek',
                            fields: dataField,
                            primary_action_label: 'Submit',
                            primary_action(values) {
                                console.log(values)
                                for (let i = 0; i < r.message.data.length; i++) {
                                    console.log(r.message.data[i].variant)
                                    let dataValue = values["field_"+[i]]
                                    let coba =[]
                                    if (dataValue){
                                        coba = dataValue.split("|")
                                        console.log(coba,"<<<<coba")
                                        var child = cur_frm.add_child("spesifikasi_tokpedia");
                                        
                                        child.variant = r.message.data[i].variant
                                        child.id = coba[0]
                                        child.name1 = coba[1]
                                        cur_frm.refresh_field("spesifikasi_tokpedia")
                                    }
                                }
                                d.hide();
                            }
                        });
                        d.show();
                        
                    }
            })
        }

        cur_frm.cscript.ada_varian = function(doc) {
        let cat = ""
        if(cur_frm.doc.child2){
            cat = cur_frm.doc.child2
        }else{
            cat = cur_frm.doc.child1
        }
        frappe.call({
                method: "tokopedia_connector.tokopedia_connector.tokopedia.create_product_variant", 
                args: {
                    cat: cat
                },
                callback: function(r) {
                    console.log(r.message)
                    let dataField = []
                    let value =[]
                    dataField.push({
                        label: 'Variant 1',
                        fieldname: 'field_variant1',
                        fieldtype: 'Select',
                        options: r.message
                    },
                    {
                        label: 'Variant 2',
                        fieldname: 'field_variant2',
                        fieldtype: 'Select',
                        options: r.message
                    })

                    let d = new frappe.ui.Dialog({
                        title: 'Tokopedia Variasi',
                        fields: dataField,
                        primary_action_label: 'Submit',
                        primary_action(values) {
                            console.log(values)
                            cur_frm.set_value('variant_1', values.field_variant1);
                            cur_frm.set_value('variant_2', values.field_variant2);
                            d.hide();
                        }
                    });
                    d.show();
                }
            })
        }

        cur_frm.cscript.add_variant_1 = function(doc) {
        frappe.call({
                method: "tokopedia_connector.tokopedia_connector.tokopedia.add_variant", 
                args: {
                    var: cur_frm.doc.variant_1
                },
                callback: function(r) {
                    // console.log(r.message)
                    let dataField = []
                    // let value =[]
                    dataField.push({
                        label: 'Value Variant',
                        fieldname: 'value_var',
                        fieldtype: 'Select',
                        options: r.message
                    })

                    let d = new frappe.ui.Dialog({
                        title: 'Value Variant',
                        fields: dataField,
                        primary_action_label: 'Submit',
                        primary_action(values) {
                            console.log(values)
                            let dataValue = values.value_var
                            let coba =[]
                            coba = dataValue.split("|")
                            var child = cur_frm.add_child("table_variant_1");
                                    
                            child.id =  coba[0]
                            child.value = coba[1]
                            cur_frm.refresh_field("table_variant_1")

                            d.hide();
                        }
                    });
                    d.show();
                }
            })
        }

        cur_frm.cscript.add_variant_2 = function(doc) {
        frappe.call({
                method: "tokopedia_connector.tokopedia_connector.tokopedia.add_variant", 
                args: {
                    var: cur_frm.doc.variant_2
                },
                callback: function(r) {
                    // console.log(r.message)
                    let dataField = []
                    // let value =[]
                    dataField.push({
                        label: 'Value Variant',
                        fieldname: 'value_var',
                        fieldtype: 'Select',
                        options: r.message
                    })

                    let d = new frappe.ui.Dialog({
                        title: 'Value Variant',
                        fields: dataField,
                        primary_action_label: 'Submit',
                        primary_action(values) {
                            console.log(values)
                            let dataValue = values.value_var
                            let coba =[]
                            coba = dataValue.split("|")
                            var child = cur_frm.add_child("table_variant_2");
                                    
                            child.id =  parseInt(coba[0])
                            child.value = coba[1]
                            cur_frm.refresh_field("table_variant_2")

                            d.hide();
                        }
                    });
                    d.show();
                }
            })
        }

        cur_frm.cscript.push_product = function(doc) {
            frappe.call({
                method: "tokopedia_connector.tokopedia_connector.tokopedia.crate_product2",
                args: {
                        id_product: cur_frm.doc.item_code,
                        data_item: data_item
                }, 
                callback: function(r) {}
            });
        }

        cur_frm.cscript.edit_product = function(doc) {
            frappe.call({
                method: "tokopedia_connector.tokopedia_connector.tokopedia.edit_product",
                args: {
                        // id_product: cur_frm.doc.item_code,
                        id_product: cur_frm.doc.product_id, 
                        data_item: cur_frm.doc
                        // data_item: data_item
                }, 
                callback: function(r) {}
            });
        }

        
        cur_frm.cscript.gabung_variant = function(doc) {
            frappe.msgprint("Gabung !!")
            if(cur_frm.doc.variant_2){
                frappe.msgprint("2 variant")
                if (!cur_frm.doc.tabel_gabung_variant){
                    frappe.msgprint("awal 2 variant")
                    for (let i = 0;i < cur_frm.doc.table_variant_1.length;i++){
                        for (let j = 0;j < cur_frm.doc.table_variant_2.length;j++){
                            //console.log(cur_frm.doc.table_variant_1[i].value)
                            var child = cur_frm.add_child("tabel_gabung_variant");
                                            
                            child.variant_1 =  cur_frm.doc.table_variant_1[i].value
                            child.variant_2 =  cur_frm.doc.table_variant_2[j].value
                           
                            cur_frm.refresh_field("tabel_gabung_variant")
                        }
                    }
                }
                // sudah ada isinya
                let panjang = cur_frm.doc.table_variant_1.length * cur_frm.doc.table_variant_2.length
                if(panjang == cur_frm.doc.tabel_gabung_variant.length){
                    frappe.msgprint("jumlah Item varint suadh sama")
                }else{
                    cur_frm.clear_table("tabel_gabung_variant")
                    cur_frm.refresh_fields();
                    for (let i = 0;i < cur_frm.doc.table_variant_1.length;i++){
                        for (let j = 0;j < cur_frm.doc.table_variant_2.length;j++){
                            //console.log(cur_frm.doc.table_variant_1[i].value)
                            var child = cur_frm.add_child("tabel_gabung_variant");
                                            
                            child.variant_1 =  cur_frm.doc.table_variant_1[i].value
                            child.variant_2 =  cur_frm.doc.table_variant_2[j].value
                           
                            cur_frm.refresh_field("tabel_gabung_variant")
                        }
                    }
                }
            } else {
                frappe.msgprint("coba 1 variant")
                if (!cur_frm.doc.tabel_gabung_variant){
                    frappe.msgprint("awal 1 variant")
                    for (let i = 0;i < cur_frm.doc.table_variant_1.length;i++){
                        var child = cur_frm.add_child("tabel_gabung_variant");
                        child.variant_1 =  cur_frm.doc.table_variant_1[i].value
                        cur_frm.refresh_field("tabel_gabung_variant")
                    }
                }
                // sudah ada isinya
                if (cur_frm.doc.table_variant_1.length == cur_frm.doc.tabel_gabung_variant.length){
                    frappe.msgprint("jumlahnya sudah sama")
                }else{
                    cur_frm.clear_table("tabel_gabung_variant")
                    cur_frm.refresh_fields();
                    for (let i = 0;i < cur_frm.doc.table_variant_1.length;i++){
                        var child = cur_frm.add_child("tabel_gabung_variant");
                        child.variant_1 =  cur_frm.doc.table_variant_1[i].value
                        cur_frm.refresh_field("tabel_gabung_variant")
                    }
                }
            }
        }

        /*frm.fields_dict['tabel_gabung_variant'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            console.log(child);
            return {    
                filters:[
                    ['item_group', '=', cur_frm.doc.shop+" Tokopedia"]
                ]
            }
        }*/

        
        cur_frm.cscript.delete_produt_variant = function(doc) {
           frappe.confirm(
                'Are you sure to Delete this product variant?',
                function(){
                     frappe.call({
                        method: "tokopedia_connector.tokopedia_connector.tokopedia.del_market_variant",
                        args: {
                                name: cur_frm.doc.name
                        }, 
                        callback: function(r) {}
                    });
                    //cur_frm.set_value("product_id","")
                },
                function(){
                    // frappe.msgprint("jika no")
                }
            )

           
        }

        cur_frm.cscript.push_product_variant = function(doc) {
            frappe.call({
                method: "tokopedia_connector.tokopedia_connector.tokopedia.push_item_var",
                args: {
                        item_code: cur_frm.doc.item_code,
                        data_item: data_item,
                        data_variant: variant_item
                }, 
                callback: function(r) {}
            });
        }

        cur_frm.cscript.edit_product_variant = function(doc) {
            frappe.call({
                method: "tokopedia_connector.tokopedia_connector.tokopedia.edit_item_var",
                args: {
                        item_code: cur_frm.doc.item_code,
                        data_item: data_item,
                        data_variant: variant_item
                }, 
                callback: function(r) {}
            });
        }

        cur_frm.cscript.delete_product = function(doc) {
           frappe.confirm(
                'Are you sure to Delete this product in tokopedia market?',
                function(){
                     frappe.call({
                        method: "tokopedia_connector.tokopedia_connector.api.product.product.delete_product",
                        args: {
                                app_id: cur_frm.doc.app_id,
                                shop_id: cur_frm.doc.shop_id,
                                product_id: cur_frm.doc.product_id,
                                shop: cur_frm.doc.shop
                        }, 
                        callback: function(r) {
                        	cur_frm.set_value("product_id","")
                        }
                    });
                },
                function(){
                    // frappe.msgprint("jika no")
                }
            )
           //cur_frm.set_value("product_id","")
           
        }
	}

})