from validations.check_unexpected_use import CheckUnexpectedUse

CONTROL_FILE_NAME = './sheets/control.csv'
CONTROL_SKIP_HEADER = False
CONTROL_FILE_SEPARATOR = ';'
CONTROL_FILE_ID_COLUMN = 0
CONTROL_FILE_USED_COLUMN = 2
CONTROL_FILE_USED_CONDITION = lambda x: 'x' == x.lower()

RECEIPT_FILE_NAME = './sheets/receipt.csv'
RECEIPT_SKIP_HEADER = True
RECEIPT_FILE_SEPARATOR = ','
RECEIPT_FILE_ID_COLUMN = 0
RECEIPT_FILE_PRICE_COLUMN = 1
RECEIPT_FILE_USED_CONDITION = lambda price: float(price) > 0

class Unit:
	def __init__(self, id, used, price=0):
		self.id = id
		self.used = used
		self.price = price



# reading your control file and indexing what resources you are using

controlfile = open(CONTROL_FILE_NAME, 'r')
lines = [l for l in controlfile]
if CONTROL_SKIP_HEADER:
	lines = lines[1:]
controlfile.close()
control_units = []

for line in lines:
	columns = line.split(CONTROL_FILE_SEPARATOR)
	print 
	control_units += [
		Unit(
			columns[CONTROL_FILE_ID_COLUMN], 
			CONTROL_FILE_USED_CONDITION(columns[CONTROL_FILE_USED_COLUMN])
		)
	]

# reading your receipt of what you are being charged for

receiptfile = open(RECEIPT_FILE_NAME, 'r')
lines = [l for l in receiptfile]
if RECEIPT_SKIP_HEADER:
	lines = lines[1:]
receiptfile.close()
charged_units = []

for line in lines:
	columns = line.split(RECEIPT_FILE_SEPARATOR)
	charged_units += [
		Unit(
			columns[RECEIPT_FILE_ID_COLUMN], 
			RECEIPT_FILE_USED_CONDITION(columns[RECEIPT_FILE_PRICE_COLUMN]), 
			columns[RECEIPT_FILE_PRICE_COLUMN]
		)
	]

# declare list of validations

validations = [CheckUnexpectedUse]

# validate

for v in validations:
	print('\n\n\n-----------------starting validation: %s-----------------' % v.name())
	v.verify(control_units, charged_units)
	print('-----------------finished validation: %s-----------------' % v.name())