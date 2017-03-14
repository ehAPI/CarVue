{
    "name" : "CarVue",
	"version": "1.0",
	"author":"ehAPI Technologies LLC",
	"website":"http://www.ehapi.com",
	"category":"Tools",
	"depends":["base","board",'mail','email_template',"report",'sale'],
	"description":"CarVue module for ehAPI",

	"data": ["wizard/sale_make_invoice_advance.xml",
			 "wizard/sale_line_invoice.xml",
			 "views/create_job_view.xml",
			 "views/customer_view.xml",
			 "views/vehicle_dashboard_view.xml",
			 "views/sales_order_view.xml",
			 # "views/sales_item_view.xml",
			 "views/products_view.xml"],

    # 'qweb': ['static/src/xml/base.xml',], 
     
	"installable": True

}