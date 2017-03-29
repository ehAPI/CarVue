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
		'notes':fields.text('Notes'),
		'code' : fields.char('Number',readonly=True),
		'status':fields.selection([('prov','Provisional'),
			('due','Due In')],'Status'),
		# 'status':fields.selection([('prov','Provisional'),
		# 	('due','Due In'),
		# 	('arr','Arrived'),
		# 	('in','In Progress'),
		# 	('paused','Paused'),
		# 	('part','Parts On Order'),
		# 	('parts','Parts Arrived'),
		# 	('awaiting','Awaiting Authority'),
		# 	('cleaning','Cleaning'),
		# 	('cust','Customer Contacted'),
		# 	('work','Work Completed')],'STATUS'),
		'due_in':fields.datetime('Due In'),
		'due_out':fields.datetime('Due Out'),
		'child_ids': fields.many2one('res.partner','Contact', domain=[('active','=',True)]), # force "active_test" domain to bypass _search() override
		'advisor':fields.many2one('res.users','Advisor',ondelete='set null'),
		'technician':fields.many2one('res.users','Technician',ondelete='set null'),
		'veh':fields.many2one('vehicle.dashboard','Vehicle',ondelete='set null', domain="[('child_ids','=',child_ids)]"),
		'bay' :fields.selection([('parking','Parking'),('ramp1','Ramp 1'),('ramp2','Ramp 2')],'Bay'),
		'reference': fields.char('Reference'),
		'mile':fields.integer('Mileage In'),
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

	def create(self,cr,uid,vals,context=None):
		if vals.get('code','/')=='/':
			vals['code']=self.pool.get('ir.sequence').get(cr,uid,'create.job') or '/'
		return super(create_job,self).create(cr,uid,vals,context=context)

	def repairs_action(self, cr, uid, ids, context=None):
		obj = self.browse(cr, uid, ids)

		assert len(ids) == 1, 'This option should only be used for a single id at a time.'
		
		ctx = dict()
		ctx.update({
			'default_model': 'sale.order',
			'default_partner_id': obj.child_ids.id,
			'default_due_in' : obj.due_in,
			'default_due_out' : obj.due_out,
			'default_advisor' : obj.advisor.id,
			'default_notes' : obj.notes,
		})
		return {
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'sale.order',
			'context': ctx,
		}

	def on_change_due_in(self,cr,uid,ids,due_in,context=None):
		duein = datetime.strptime(due_in,'%Y-%m-%d %H:%M:%S')
		due_out=(duein + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
		res={
		'value' : {'due_out':due_out}
		}
		return res

	_defaults={
		'due_in': lambda *a:datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
		'due_out': lambda *a:(datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
	}

create_job()

