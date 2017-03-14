from openerp.osv import fields, osv

class customer(osv.osv):

	_name = 'customer'
	_columns = {
			'name':fields.char('Name'),
	}

customer()
