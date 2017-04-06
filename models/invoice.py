from openerp.osv import fields, osv

class account_invoices(osv.osv):
	_inherit='account.invoice'
	_columns={
	'notes':fields.text('Notes'),
	'due_in':fields.datetime('Due In'),
	'due_out':fields.datetime('Due Out'),
	'veh':fields.many2one('vehicle.dashboard','Vehicle',ondelete='set null', domain="[('child_ids','=',partner_id)]"),
	'advisor':fields.many2one('res.users','Advisor',ondelete='set null'),
	'technician':fields.many2one('res.users','Technician',ondelete='set null'),
	'bay' :fields.selection([('parking','Parking'),('ramp1','Ramp 1'),('ramp2','Ramp 2')],'Bay'),
	'reference': fields.char('Reference'),
	'mile':fields.integer('Mileage In'),
	'status':fields.selection([('in','In Progress'),
			('paused','Paused'),
			('part','Parts On Order'),
			('parts','Parts Arrived'),
			('awaiting','Awaiting Authority'),
			('cleaning','Cleaning'),
			('cust','Customer Contacted'),
			('work','Work Completed')],'Status'),
	}

	def action_invoice_sent(self, cr, uid, ids, context=None):
		'''  Override to use a modified template that includes ehapi closing '''
		action_dict = super(account_invoices, self).action_invoice_sent(cr, uid, ids, context=context)
		try:
			template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'car_vue', 'email_template_edi_invoice')[1]
			# assume context is still a dict, as prepared by super
			ctx = action_dict['context']
			ctx['default_template_id'] = template_id
			ctx['default_use_template'] = True
		except Exception:
			pass
		return action_dict

account_invoices()
