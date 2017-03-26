from openerp.osv import fields, osv
# from datetime import datetime

class customer(osv.osv):

	_inherit = 'res.partner'

	# def _default_account_receivable(self, cr, uid, context=None):
	# 	cid = self.pool.get('account.account').search(cr, uid, [('type', '=', 'receivable')], context=context)
	# 	return cid[0]

	# def _default_account_payable(self, cr, uid, context=None):
	# 	cid = self.pool.get('account.account').search(cr, uid, [('type', '=', 'payable')], context=context)
	# 	return cid[0]
	
	# _defaults ={
	# 	'property_account_receivable':_default_account_receivable,
	# 	'property_account_payable':_default_account_payable,
		# 'last_reconciliation_date':lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
	# }

customer()
