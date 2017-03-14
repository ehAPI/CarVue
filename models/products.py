from openerp.osv import fields, osv

class products(osv.osv):

	_name = 'products'
	_columns = {
			'code':fields.char('Code'),
	}

products()
