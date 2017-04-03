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
	'advisor':fields.many2one('res.users','Advisor',ondelete='set null'),
	'technician':fields.many2one('res.users','Technician',ondelete='set null'),
	'bay' :fields.selection([('parking','Parking'),('ramp1','Ramp 1'),('ramp2','Ramp 2')],'Bay'),
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

	def action_quotation_send(self, cr, uid, ids, context=None):
		'''  Override to use a modified template that includes a portal signup link '''
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

	def wkf_send_rfq(self, cr, uid, ids, context=None):
		'''  Override to use a modified template that includes a portal signup link '''
		action_dict = super(purchase_order, self).wkf_send_rfq(cr, uid, ids, context=context)
		try:
			if context.get('send_rfq', False):
				template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'car_vue', 'email_template_edi_purchase')[1]
			else:
				template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'car_vue', 'email_template_edi_purchase_done')[1]
		
			# assume context is still a dict, as prepared by super
			ctx = action_dict['context']
			ctx['default_template_id'] = template_id
			ctx['default_use_template'] = True
		except Exception:
			pass
		return action_dict	
		
	



	# def wkf_send_rfq(self, cr, uid, ids, context=None):
	# 	'''
	# 	This function opens a window to compose an email, with the edi purchase template message loaded by default
	# 	'''
	# 	if not context:
	# 		context= {}
	# 	ir_model_data = self.pool.get('ir.model.data')
	# 	try:
	# 		if context.get('send_rfq', False):
	# 			template_id = ir_model_data.get_object_reference(cr, uid, 'car_vue', 'email_template_edi_purchase')[1]
	# 		else:
	# 			template_id = ir_model_data.get_object_reference(cr, uid, 'car_vue', 'email_template_edi_purchase_done')[1]
	# 	except ValueError:
	# 		template_id = False
	# 	try:
	# 		compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
	# 	except ValueError:
	# 		compose_form_id = False 
	# 	ctx = dict(context)
	# 	ctx.update({
	# 		'default_res_id': ids[0],
	# 		'default_use_template': True,
	# 		'default_template_id': template_id,
	# 		'default_composition_mode': 'comment',
	# 	})
	# 	return {
	# 		'name': _('Compose Email'),
	# 		'type': 'ir.actions.act_window',
	# 		'view_type': 'form',
	# 		'view_mode': 'form',
	# 		'res_model': 'mail.compose.message',
	# 		'views': [(compose_form_id, 'form')],
	# 		'view_id': compose_form_id,
	# 		'target': 'new',
	# 		'context': ctx,
	# 	}	

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
			'advisor': order.advisor.id,
			}
		invoice_vals.update(self._inv_get(cr, uid, order, context=context))
		return invoice_vals

sale_order()