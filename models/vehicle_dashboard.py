from openerp.osv import fields, osv
import datetime
import time

class vehicle_dashboard(osv.osv):

	_name = 'vehicle.dashboard'
	_rec_name = 'registration'
	_columns = {
		'registration' : fields.char('Registration',required=True),
		'make' : fields.many2one('make','Make',required=True),
		'model' : fields.many2one('model','Model',required=True),
		'derivative' : fields.many2one('derivative','Derivative'),
		'age' : fields.integer('Age'),
		'colour' : fields.char('Colour'),
		'odometer' : fields.float('Odometer Reading'),
		'odo_unit' : fields.selection([('miles','Miles'),('km','Kilometers')],'Odometer Unit'),
		'model_year': fields.selection([(num, str(num)) for num in range(1901,(datetime.datetime.now().year)+1)], 'Model Year'),
		'reg_date' : fields.date('Reg Date'),
		'vin' : fields.char('VIN'),
		'date_of_manufacture' : fields.char('Date of Manufacture'),
		'paint_code' : fields.char('Paint Code'),
		'trim' : fields.char('Trim'),
		'fuel' : fields.selection([('petrol','Petrol'),
									('diesel','Diesel'),
									('electric','Electric'),
									('hybrid','Hybrid'),
									('lpg','LPG'),
									('cng','CNG'),
									('other','Other')],'Fuel'),
		'door_plan' : fields.char('Door Plan'),
		'gear_box' : fields.char('Gear Box'),
		'gear_box_no' : fields.char('Gear Box No.'),
		'co2emissions' : fields.char('CO2 Emissions'),
		'engine_no' : fields.char('Engine No.'),
		'engine_code' : fields.char('Engine Code'),
		'engine_size' : fields.char('Engine Size'),
		'power' : fields.char('Power'),
		'key_no' : fields.char('Key No.'),
		'radio_no' : fields.char('Radio No.'),
		'mot_due_date' : fields.date('MOT Due Date'),
		'service_due_date' : fields.date('Service Due Date'),
		'warranty_ends' : fields.date('Warranty Ends'),
		'notes' : fields.text('Notes'),
		'contacts' : fields.char('Contacts'),
		}

vehicle_dashboard()
