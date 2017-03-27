{
    "name" : "CarVue",
	"version": "1.0",
	"author":"ehAPI Technologies LLC",
	"website":"http://www.ehapi.com",
	"category":"Tools",
	"depends":["base","board",'mail','email_template',"report",'sale','stock','purchase'],
	"description":"CarVue module for ehAPI",

	"data": ["views/create_job_view.xml",
			 "views/vehicle_dashboard_view.xml",
			 "views/contacts_view.xml",
			 "security/car_vue_security_view.xml",
			 "security/ir.model.access.csv",
			 "views/configuration_view.xml",

			 "report/report_saleorder.xml",
			 # "report_print.xml",

			 "views/invoices_view.xml",
			 # "views/products_view.xml",
			 "views/car_vue_sequence.xml"],

    # 'qweb': ['static/src/xml/base.xml',], 
     
	"installable": True

}