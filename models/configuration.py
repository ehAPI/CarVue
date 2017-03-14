from openerp.osv import fields, osv

class make(osv.osv):

	_name = 'make'
	_columns = {
		'make_of_car' : fields.char('Make',required=True),
		}
make()


class model(osv.osv):

	_name = 'model'
	_columns = {
		'make' : fields.many2one('make','Make',required=True,onchange=),
		'model_of_car':fields.char('make','Model',required=True),
		}
model()

class derivative(osv.osv):

	_name = 'derivative'
	_columns = {
		'make' : fields.many2one('make','Make',required=True,onchange=),
		'model':fields.many2one('model','Model',required=True,onchange=),
		"derivative":fields.char('Derivative',required=True),
		}
derivative()