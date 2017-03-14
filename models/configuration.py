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
		'make' : fields.many2one('make','Make',required=True,onchange='onchange_make(make)'),
		'model_of_car':fields.char('Model',size=50,required=True),
		}

	def onchange_taskid(self, cr, uid, ids, make_of_car, context=None):
		res = {'value': {}}
		if make_of_car:
			part = self.pool.get('make').browse(
				cr, uid, make_of_car, context)
			# print part.atm.id
			res['value'].update({'model_of_car': part.model_of_car})
			# res['value'].update({'atm_surv': part.atm.id})
			# res['value'].update({'surveyor_surv': part.surveyor.id})

			# res['value'].update({'customer_surv': part.customer.id})
			# res['value'].update({'visit_tm': part.visit_time})
			# res['value'].update({'state': part.state.id})

		return res
model()

class derivative(osv.osv):

	_name = 'derivative'
	_rec_name = 'derivative'
	_columns = {
		'make' : fields.many2one('make','Make',required=True),
		'model':fields.many2one('model','Model',required=True),
		"derivative":fields.char('Derivative',size=50,required=True),
		}
derivative()