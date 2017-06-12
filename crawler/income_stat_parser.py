# -*- coding: UTF-8 -*-
import xlrd

book = xlrd.open_workbook('../data/mean.xls')

for sheet_index, sheet_name in enumerate(book.sheet_names()):

	csv_name = '{0}/{1}可支配所得.csv'.format('../data', sheet_name.encode('utf8'))
	csv_file = open(csv_name, 'w')

	sheet_entity = book.sheet_by_index(sheet_index)

	for row_index in range(sheet_entity.nrows):

		cells = sheet_entity.row(row_index)
		# Heads are in row 3
		if row_index == 2:
			value = [ cell.value.encode('utf8') for cell in cells ]
			value.append('\n')
			csv_file.write(','.join(value))
		# 2 means type is number
		elif cells[0].ctype == 2:
			value = [ str(cell.value) if cell.ctype == 2 else '0'  for cell in cells ]
			value.append('\n')
			csv_file.write(','.join(value))
		else:
			pass

	csv_file.close()




