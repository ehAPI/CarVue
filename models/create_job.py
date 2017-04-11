from openerp.osv import fields, osv
import time 
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

class create_job(osv.osv):

	_name = "job.order"
	_rec_name="code"
	# def arrived_function(self,cr,uid,ids,context=None):
	# 	obj = self.browse(cr, uid, ids)
	# 	if obj.status=='arrived':
	# 		return True
	# 	else:
	# 		return False
			
	_columns = {
		"notes":fields.text("Notes"),
		"code" : fields.char("Number",readonly=True),
		"status":fields.selection([("prov","Provisional"),
			("due","Due In"),("arrived","Arrived")],"Status"),
		"due_in":fields.datetime("Due In", required=True),
		"due_out":fields.datetime("Due Out", required=True),
		"child_ids": fields.many2one("res.partner","Customer", required=True, domain=[("active","=",True)]), # force "active_test" domain to bypass _search() override
		"advisor":fields.many2one("res.users","Advisor", required=True,ondelete="set null"),
		"technician":fields.many2one("res.users","Technician", required=True,ondelete="set null"),
		"veh":fields.many2one("vehicle.dashboard","Vehicle", required=True,ondelete="set null", domain='[("child_ids","=",child_ids)]'),
		"bay" :fields.selection([("parking","Parking"),("ramp1","Ramp 1"),("ramp2","Ramp 2")],"Bay"),
		"reference": fields.char("Reference"),
		"mile":fields.integer("Mileage In"),
		# "is_arrived":fields.function(arrived_function,type='boolean',string="Is Arrived",method=True, store = False, multi=False),
		"image":fields.binary("Image",filters="*.png,*.gif"),
	}
	
	def status_provisional(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{"status":"prov"},context=context)
		return True

	def status_duein(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{"status":"due"},context=context)
		return True

	def status_arrived(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{"status":"arrived"},context=context)
		return True

	def status_in(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{"status":"in"},context=context)
		return True

	def status_paused(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{"status":"paused"},context=context)
		return True

	def status_part(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{"status":"part"},context=context)
		return True	

	def status_parts(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{"status":"parts"},context=context)
		return True

	def status_awaiting(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{"status":"awaiting"},context=context)
		return True	

	def status_cleaning(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{"status":"cleaning"},context=context)
		return True	

	def status_cust(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{"status":"cust"},context=context)
		return True	

	def status_work(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{"status":"work"},context=context)
		return True	

	def create(self,cr,uid,vals,context=None):
		if vals.get("code","/")=="/":
			vals["code"]=self.pool.get("ir.sequence").get(cr,uid,"job.order") or "/"
		return super(create_job,self).create(cr,uid,vals,context=context)

	def repairs_action(self, cr, uid, ids, context=None):
		# self.write(cr,uid,ids,{"status":"arrived"},context=context)
		obj = self.browse(cr, uid, ids)
		assert len(ids) == 1, "This option should only be used for a single id at a time."
		ctx = dict()
		ctx.update({
			"default_model": "sale.order",
			"default_partner_id": obj.child_ids.id,
			"default_due_in" : obj.due_in,
			"default_due_out" : obj.due_out,
			"default_veh" : obj.veh.id,
			"default_advisor" : obj.advisor.id,
			"default_technician" : obj.technician.id,
			"default_notes" : obj.notes,
			"default_job_id" : obj.code,
		})
		return {
			"type": "ir.actions.act_window",
			"view_type": "form",
			"view_mode": "form",
			"res_model": "sale.order",
			"context": ctx,
		}

	def on_change_due_in(self,cr,uid,ids,due_in,context=None):
		duein = datetime.strptime(due_in,"%Y-%m-%d %H:%M:%S")
		due_out=(duein + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
		res={
		"value" : {"due_out":due_out}
		}
		return res

	def unlink(self, cr, uid, ids, context=None):
		sale_orders = self.read(cr, uid, ids, ['state'], context=context)
		unlink_ids = []
		for s in sale_orders:
			if s['state'] in ['draft', 'cancel']:
				unlink_ids.append(s['id'])
				

			else:
				raise osv.except_osv(_('Invalid Action!'), _('In order to delete a confirmed sales order, you must cancel it before!'))

		return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)	

	# def unlink(self, cr, uid, ids, context=None):
 #        sale_orders = self.read(cr, uid, ids, ['state'], context=context)
 #        unlink_ids = []
 #        for s in sale_orders:
 #            if s['state'] in ['draft', 'cancel']:
 #                unlink_ids.append(s['id'])
	# 			obj = self.browse(cr, uid, ids)
	# 			assert len(ids) == 1, 'This option should only be used for a single id at a time.'
	# 			return {
	# 				'type': 'ir.actions.act_window',
	# 				'view_mode': 'tree,kanban,form',
	# 				'domain':"[('veh.registration', '=',%s)]" %(obj.registration),
	# 				'res_model': 'job.order',
	# 			}

 #            else:
 #                raise osv.except_osv(_('Invalid Action!'), _('In order to delete a confirmed sales order, you must cancel it before!'))

 #        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)	

	# def fields_view_get(self, cr, uid, view_id=None, view_type="form", context=True, toolbar=False, submenu=False):
	# 	result = super(create_job, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
	# 	if view_type=="form":
	# 		current_id=context.get("active_id", False)
	# 		my_state=self.browse(cr,uid,current_id).status
	# 		if my_state=="arrived":
	# 			# modify_edit_str="edit='false'"
	# 			result["arch"]='<form string="Jobs" edit="false" version="8.0">\
	# 				<header>\
	# 					<button name="status_provisional" type="object" String="Provisional" attrs="{"invisible": [("status","in",("prov","due","arrived"))]}" class="oe_highlight"/>\
	# 					<button name="status_duein" type="object" String="Due In" attrs="{"invisible": [("status","in",("due","arrived"))]}" class="oe_highlight"/>\
	# 					<field name="status" widget="statusbar" \
	# 						statusbar_visible="prov,due"/>\
	# 				</header>\
	# 				<sheet>\
	# 					<field name="image" widget="image" class="oe_left oe_avatar" options="{"size": [100, 100]}" nolabel="1"/>\
	# 					<div class="oe_title oe_left">\
	# 						<h2>\
	# 							<field name="code" nolabel="1"/>\
	# 						</h2>\
	# 					</div>\
	# 					<div class="oe_right oe_button_box">\
	# 						<button class="oe_right oe_box oe_highlight" name="repairs_action"  type="object" String="Arrived" groups="car_vue.group_car_vue_admin,car_vue.group_car_vue_manager" attrs="{"invisible": [("status","in",("arrived"))]}"/>\
	# 					</div>\
	# 					<group>\
	# 						<group string = "CUSTOMER">\
	# 							<field name="child_ids" nolabel="1"/>\
	# 						</group>\
	# 						<group string = "VEHICLE">	\
	# 								<field name="veh" nolabel="1"/>\
	# 						</group>\
	# 						<group string="Job Card">\
	# 							<field name="due_in" on_change="on_change_due_in(due_in)"/>\
	# 							<field name="due_out"/>\
	# 							<field name="advisor"/>\
	# 							<field name="technician"/>\
	# 							<field name="notes"/>\
	# 						</group>\
	# 					</group>\
	# 				</sheet>\
	# 			</form>'
	# 		else:
	# 			pass
	# 	return result


	# def test_fields_view_get(self,cr,uid):
	# 	idea_obj = self.pool.get('job.order')
	# 	form_view = idea_obj.fields_view_get(cr,uid)

	_defaults={
		"due_in": lambda *a:datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
		"due_out": lambda *a:(datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
		"status":"prov",
	}

create_job()