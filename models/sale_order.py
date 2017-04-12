from openerp.osv import fields, osv
import time 
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

class sale_order(osv.osv):

	_inherit="sale.order"
	_columns = {
	'notes':fields.text('Notes'),
	'due_in':fields.datetime('Due In'),
	'due_out':fields.datetime('Due Out'),
	'veh':fields.many2one('vehicle.dashboard','Vehicle',ondelete='set null', domain="[('child_ids','=',partner_id)]"),
	'advisor':fields.many2one('res.users','Advisor',ondelete='set null'),
	'technician':fields.many2one('res.users','Technician',ondelete='set null'),
	'bay' :fields.selection([('parking','Parking'),('ramp1','Ramp 1'),('ramp2','Ramp 2')],'Bay'),
	'mile':fields.integer('Mileage In'),
	'job_id': fields.char('Job ID',readonly=True),
	'status':fields.selection([('in','In Progress'),
			('paused','Paused'),
			('part','Parts On Order'),
			('parts','Parts Arrived'),
			('awaiting','Awaiting Authority'),
			('cleaning','Cleaning'),
			('cust','Customer Contacted'),
			('work','Work Completed'),
			('cancel','Cancelled')],'Status'),
	"code" : fields.char("Number",readonly=True),

	}

	_defaults={
		'status': 'in'
	}

	def action_quotation_send(self, cr, uid, ids, context=None):
		'''  Override to use a modified template that includes a ehapi closing and additional table '''
		action_dict = super(sale_order, self).action_quotation_send(cr, uid, ids, context=context)
		try:
			template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'car_vue', 'email_template_edi_sale')[1]
			# assume context is still a dict, as prepared by super
			ctx = action_dict['context']
			ctx['default_template_id'] = template_id
			ctx['default_use_template'] = True
		except Exception:
			pass
		return action_dict

	def action_cancel(self, cr, uid, ids, context=None):
		if context is None:
			context = {}
		sale_order_line_obj = self.pool.get('sale.order.line')
		account_invoice_obj = self.pool.get('account.invoice')
		procurement_obj = self.pool.get('procurement.order')
		for sale in self.browse(cr, uid, ids, context=context):
			for inv in sale.invoice_ids:
				if inv.state not in ('draft', 'cancel'):
					raise osv.except_osv(
						('Cannot cancel this sales order!'),
						('First cancel all invoices attached to this sales order.'))
				inv.signal_workflow('invoice_cancel')
			procurement_obj.cancel(cr, uid, sum([l.procurement_ids.ids for l in sale.order_line],[]))
			sale_order_line_obj.write(cr, uid, [l.id for l in  sale.order_line],
					{'state': 'cancel'})
			obj = self.pool.get('job.order').search(cr,uid,[('code','=',sale.job_id)],context=context)
			self.pool.get('job.order').write(cr,uid,obj,{'status':'cancel'},context=context)
		self.write(cr, uid, ids, {'state': 'cancel'})
		self.write(cr, uid, ids, {'status': 'cancel'})
		
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

	def _prepare_invoice(self, cr, uid, order, lines, context=None):
		if context is None:
			context = {}
		journal_ids = self.pool.get('account.journal').search(cr, uid,
			[('type', '=', 'sale'), ('company_id', '=', order.company_id.id)],
			limit=1)
		if not journal_ids:
			raise osv.except_osv(_('Error!'),
				_('Please define sales journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
		invoice_vals = {
			'name': order.client_order_ref or '',
			'origin': order.name,
			'type': 'out_invoice',
			'reference': order.client_order_ref or order.name,
			'account_id': order.partner_id.property_account_receivable.id,
			'partner_id': order.partner_invoice_id.id,
			'journal_id': journal_ids[0],
			'invoice_line': [(6, 0, lines)],
			'currency_id': order.pricelist_id.currency_id.id,
			'comment': order.note,
			'payment_term': order.payment_term and order.payment_term.id or False,
			'fiscal_position': order.fiscal_position.id or order.partner_id.property_account_position.id,
			'date_invoice': context.get('date_invoice', False),
			'company_id': order.company_id.id,
			'user_id': order.user_id and order.user_id.id or False,
			'section_id' : order.section_id.id,
			'due_in': order.due_in,
			'due_out': order.due_out,
			'bay': order.bay,
			'mile': order.mile,
			'technician': order.technician.id,
			'notes': order.notes,
			'veh': order.veh.id,
			'advisor': order.advisor.id,
			}
		invoice_vals.update(self._inv_get(cr, uid, order, context=context))
		return invoice_vals


	def create(self, cr, uid, vals, context=None):
		# new_id=super(sale_order,self).create(cr,uid,vals,context)

		job_id=vals.get('job_id','/')
		arrived_jobs = self.pool.get('job.order').search(cr,uid,[('code','=',job_id)],context=context)
		self.pool.get('job.order').write(cr,uid,arrived_jobs,{'status':'arrived'},context=context)

		return super(sale_order,self).create(cr,uid,vals,context)
		# return new_id

	def unlink(self, cr, uid, ids, context=None):
		sale_orders = self.read(cr, uid, ids, ['state','job_id'], context=context)
		unlink_ids = []
		for s in sale_orders:
			if s['state'] in ['draft', 'cancel']:
				unlink_ids.append(s['id'])

				#######################
				obj = self.pool.get('job.order').search(cr,uid,[('code','=',s['job_id'])],context=context)
				self.pool.get('job.order').write(cr,uid,obj,{'status':'due'},context=context)
				#######################

				#######################
				# job = self.pool.get('job.order').read(cr,uid,ids,['status','code'],context=context)
				# jobs_to_due=[]
				# for o in job:
				# 	if o['code']==s['job_id']:
				# 		jobs_to_due.append(o['id'])
				# 		job[o.id].update({'status':'due'})
				# self.pool.get('job.order').write(cr,uid,jobs_to_due,{'status':'due'},context=context)
				#######################
				
				#######################
				# obj = self.pool.get('job.order').browse(cr,uid,ids,context=context)
				# jobs_to_due=[]
				# for o in obj:
				# 	if o.code==s['job_id']:
				# 		jobs_to_due.append(o.id)
				# self.pool.get('job.order').write(cr,uid,jobs_to_due,{'status':'due'},context=context)
				#######################
				
			else:
				raise osv.except_osv(('Invalid Action!'), ('In order to delete a confirmed sales order, you must cancel it before!'))

		return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

sale_order()