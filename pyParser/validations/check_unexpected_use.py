CURRENCY = 'BRL'

class CheckUnexpectedUse:
	@staticmethod
	def name():
		return 'check unexpected use of resource'

	@staticmethod
	def verify(control_units, charged_units):
		control_units_map = {cou.id: cou for cou in control_units}
		charged_units_map = {chu.id: chu for chu in charged_units}
		for chu in charged_units:
			if not chu.id in control_units_map:
				print('could not find id %s in control units' % (chu.id))
			if chu.used and (not chu.id in control_units_map or not control_units_map[chu.id].used):
				print('you are being unexpectedly charged for id %s for %s %s' % (chu.id, CURRENCY, chu.price))
