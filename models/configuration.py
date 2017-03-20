from openerp.osv import fields, osv

class make(osv.osv):

	_name = 'make'
	_rec_name = 'make_of_car'
	_columns = {
		'make_of_car' : fields.char('Make',size=50,required=True),
		}
make()


class model(osv.osv):

	_name = 'model'
	_rec_name = 'model_of_car'
	_columns = {
		'make' : fields.many2one('make','Make',required=True),
		'model_of_car':fields.char('Model',size=50,required=True),
		}

model()


class derivative(osv.osv):

	_name = 'derivative'
	_rec_name = 'derivative'
	_columns = {

		'make' : fields.many2one('make','Make',required=True,),
		'model':fields.many2one('model','Model',required=True, domain="[('make','=',make)]"),
		"derivative":fields.char('Derivative',size=50,required=True),
		}
derivative()