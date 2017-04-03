from openerp.osv import fields, osv
import time 
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

class purchase(osv.osv):
	_inherit="purchase.order"
	
	def wkf_send_rfq(self, cr, uid, ids, context=None):
		'''  Override to use a modified template that includes a portal signup link '''
		action_dict = super(purchase, self).wkf_send_rfq(cr, uid, ids, context=context)
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

purchase()
