from openerp.osv import fields, osv
import time 
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

class create_job(osv.osv):

	_name = 'create.job'
	_rec_name='code'
	_columns = {
		# 'new':fields.char('New Job Card'),
		# 'name':fields.one2many('res.partner','CONTACTS',ondelete='set null'),
		'notes':fields.text('NOTES'),

		'code' : fields.char('NUMBER',readonly=True),
		'status':fields.selection([('prov','Provitional'),
			('due','Due In'),
			('arr','Arrived'),
			('in','In Progress'),
			('paused','Paused'),
			('part','Parts On Order'),
			('parts','Parts Arrived'),
			('awaiting','Awaiting Authority'),
			('cleaning','Cleaning'),
			('cust','Customer Contacted'),
			('work','Work Completed')],'STATUS'),
		'due_in':fields.datetime('DUE IN'),
		'due_out':fields.datetime('DUE OUT'), 
        'child_ids': fields.many2one('res.partner','CONTACT',domain=[('active','=',True)]), # force "active_test" domain to bypass _search() override
		'advisor':fields.many2one('res.users','ADVISOR',ondelete='set null'),
		'technician':fields.many2one('res.users','TECHNICIAN',ondelete='set null'),
		'veh':fields.many2one('vehicle.dashboard','VEHICLE',ondelete='set null'),
		'bay' :fields.selection([('parking','Parking'),('ramp1','Ramp 1'),('ramp2','Ramp 2')],'Bay'),
		'reference': fields.char('Reference'),
		'mile':fields.integer('Mileage In'),
		# 'name' : fields.one2many('res.partner','chn','Chapter'),    
	}


	def status_provisional(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'prov'},context=context)
		return True

	def status_duein(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'due'},context=context)
		return True

	def status_arr(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'arr'},context=context)
		return True

	def status_in(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'in'},context=context)
		return True

	def status_paused(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'paused'},context=context)
		return True

	def status_part(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'part'},context=context)
		return True	

	def status_parts(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'parts'},context=context)
		return True

	def status_awaiting(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'awaiting'},context=context)
		return True	

	def status_cleaning(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'cleaning'},context=context)
		return True	

	def status_cust(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'cust'},context=context)
		return True	

	def status_work(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'work'},context=context)
		return True	

	# def save(self,cr,uid,ids,context=None):
	# 	_inherit = 'sale.order'

	# 	return True	

	def create(self,cr,uid,vals,context=None):
		if vals.get('code','/')=='/':
			vals['code']=self.pool.get('ir.sequence').get(cr,uid,'create.job') or '/'
		return super(create_job,self).create(cr,uid,vals,context=context)

	# def onchange_due_in(self,cr,uid,ids,due_in,context=None):
	# 	res={'value':{}}
	# 	due_in = self.pool.get('create.job').browse(cr,uid,due_in)
	# 	res['value'].update({'due_out':(due_in.due_in + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')})
	# 		# 'sla_end_date':due_in.sla_end_date,
	# 		# 'country':due_in.country.id})

	# 	return res
	
	_defaults={
		'due_in': lambda *a:datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
    	'due_out': lambda *a:(datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
	}

create_job()





