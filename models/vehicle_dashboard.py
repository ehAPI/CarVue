from openerp.osv import fields, osv
import datetime
import time

class vehicle_dashboard(osv.osv):

	_name = 'vehicle.dashboard'
	_rec_name = 'registration'

	def __count_jobs(self, cr, uid, ids, name, arg, context=None):
		result = {}
		for obj in self.browse(cr, uid, ids, context=context):
			jobs = self.pool.get('job.order').search(cr,uid,[('veh','=',obj.registration)])
			result[obj.id] = len(jobs)
		return result

	_columns = {
		'code': fields.char('Code',readonly=True),
		'registration' : fields.char('Registration',required=True),	
		'make' : fields.many2one('make','Make',required=True),
		'model' : fields.many2one('model','Model',required=True, domain="[('make','=',make)]"),
		'derivative' : fields.many2one('derivative','Derivative', domain="[('model','=',model)]"),
		'age' : fields.integer('Age'),
		#'assign_to':fields.many2one('res.users','Assign To', required=True, domain="[('role','=','Surveyor')]"),
		
		# 'child_ids': fields.many2one('res.user','Owner', required=True, ondelete='set null'), #force "active_test" domain to bypass _search() override
		'child_ids': fields.many2one('res.partner','Owner', domain=[('active','=',True)],required=True), #force "active_test" domain to bypass _search() override
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
		'jobs_count' : fields.function(__count_jobs,type='integer',string="Jobs",method=True, store = False, multi=False),
		'contacts' : fields.char('Contacts'),
		'image': fields.binary("Image",
            help="This field holds the image used as avatar for this contact, limited to 1024x1024px")

		# 'image_medium': fields.function(_get_image, fnct_inv=_set_image,
  #           string="Medium-sized image", type="binary", multi="_get_image",
  #           store={
  #               'res.partner': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
  #           },
  #           help="Medium-sized image of this contact. It is automatically "\
  #                "resized as a 128x128px image, with aspect ratio preserved. "\
  #                "Use this field in form views or some kanban views."),
		}

	_sql_constraints = [
		('registration_unique', 'unique(registration)','Registration No. must be UNIQUE !!!'),
	]


	# @api.multi
 #    def _get_image(self, name, args):
 #        return dict((p.id, tools.image_get_resized_images(p.image)) for p in self)

 #    @api.one
 #    def _set_image(self, name, value, args):
 #        return self.write({'image': tools.image_resize_image_big(value)})

	def create(self,cr,uid,vals,context=None):
		if vals.get('code','/')=='/':
			vals['code']=self.pool.get('ir.sequence').get(cr,uid,'vehicle.dashboard') or '/'
		return super(vehicle_dashboard,self).create(cr,uid,vals,context=context)

	def jobs_button(self, cr, uid, ids, context=None):
		obj = self.browse(cr, uid, ids)
		assert len(ids) == 1, 'This option should only be used for a single id at a time.'
		return {
			'type': 'ir.actions.act_window',
			'view_mode': 'tree,kanban,form',
			'domain':"[('veh.registration', '=',%s)]" %(obj.registration),
			'res_model': 'job.order',
		}

vehicle_dashboard()