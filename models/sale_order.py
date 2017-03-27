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
			'reference': order.reference,
			'mile': order.mile,
			'technician': order.technician.id,
			'notes': order.notes,
			'advisor': order.advisor.id,
			}
		invoice_vals.update(self._inv_get(cr, uid, order, context=context))
		return invoice_vals

sale_order()