import re
import xlrd
import numpy  as np
import pandas as pd

LOW_INCOME_INPUT_PATH  = '/'.join(['..', '全國低收入與中低收入戶統計', '1.1.1+低收入戶戶數及人數105Q3.xls'])
LOW_INCOME_OUTPUT_PATH = '/'.join(['..', '全國低收入與中低收入戶統計', 'low_income_tw.csv'])

LOWMID_INCOME_INPUT_PATH  = '/'.join(['..', '全國低收入與中低收入戶統計', '1.1.5+中低收入戶戶數及人數.xls'])
LOWMID_INCOME_OUTPUT_PATH = '/'.join(['..', '全國低收入與中低收入戶統計', 'midlow_income_tw.csv'])

CITY_RE  = re.compile('(?P<name>[\u4e00-\u9fff]{1}\s*[\u4e00-\u9fff]{1}\s*(縣|市))')
TOTAL_RE = re.compile('總\s*計')
END_RE   = re.compile('資料來源')

# The latest status the gov released.
CURRENT_LOW_INCOME_YEAR = 2016
CURRENT_LOW_INCOME_SEASON = 3

def check_low_income_before_2003(year):

	if year < 2003:
		return True
	else:
		return False

def parse_low_income_sheet(year, location, cells):

	columns_order = [
		'total_house', 'total_house_male', 'total_house_female', 
		'total_people', 'total_people_male', 'total_people_female', 
		'class_1_house', 'class_1_house_male', 'class_1_house_female', 
		'class_1_people', 'class_1_people_male', 'class_1_people_female', 
		'class_2_house', 'class_2_house_male', 'class_2_house_female', 
		'class_2_people', 'class_2_people_male', 'class_2_people_female', 
		'class_3_house', 'class_3_house_male', 'class_3_house_female', 
		'class_3_people', 'class_3_people_male', 'class_3_people_female', 
		'rate_of_house' , 'rate_of_people' 
	]

	low_income_data['year'].append(year)
	low_income_data['location'].append(location)

	read_col = 0
	for cell in cells:
		if cell.ctype == 2 or cell.value == '':
			column_name = columns_order[read_col]
			cell_value = cell.value if cell.ctype == 2 else 0
			low_income_data[column_name].append(cell_value)
			
			if read_col < len(columns_order)-1:
				read_col += 1
			else:
				break


		
# Table before 2003 does not calculate different gender
def parse_low_income_sheet_before_2003(year, location, cells):

	columns_order = [
		'total_house','class_1_house','class_2_house', 'class_3_house',
		'total_people','class_1_people','class_2_people', 'class_3_people',
		'rate_of_house','rate_of_people' 
	]

	low_income_data['year'].append(year)
	low_income_data['location'].append(location)

	read_col = 0
	for cell in cells:
		if cell.ctype == 2 or cell.value == '':
			column_name = columns_order[read_col]
			cell_value = cell.value if cell.ctype == 2 else 0
			low_income_data[column_name].append(cell_value)

			if read_col < len(columns_order)-1:
				read_col += 1
			else:
				break

	low_income_data['total_house_male'].append(0)
	low_income_data['total_house_female'].append(0)
	low_income_data['total_people_male'].append(0)
	low_income_data['total_people_female'].append(0)
	low_income_data['class_1_house_male'].append(0)
	low_income_data['class_2_house_male'].append(0)
	low_income_data['class_3_house_male'].append(0)
	low_income_data['class_1_house_female'].append(0)
	low_income_data['class_2_house_female'].append(0)
	low_income_data['class_3_house_female'].append(0)
	low_income_data['class_1_people_male'].append(0)
	low_income_data['class_2_people_male'].append(0)
	low_income_data['class_3_people_male'].append(0)
	low_income_data['class_1_people_female'].append(0)
	low_income_data['class_2_people_female'].append(0)
	low_income_data['class_3_people_female'].append(0)


def parse_mid_lowincome(year, location, rows):

	columns_order = [
		'total_house', 'total_house_male', 'total_house_female',
		'total_people','total_people_male','total_people_female',
		'total_people_below12','total_people_below12_male','total_people_below12_female',
		'total_people_between12_17', 'total_people_between12_17_male', 'total_people_between12_17_female',
		'total_people_between18_64', 'total_people_between18_64_male', 'total_people_between18_64_female',
		'total_people_over65', 'total_people_over65_male', 'total_people_over65_female'
	]

	midlow_income_data['year'].append(year)
	midlow_income_data['location'].append(location)

	col_pointer = 0
	for i in range(0, len(rows[0])):
		for j in range(0, len(rows)):

			if rows[j][i].ctype == 2:
				column_name = columns_order[col_pointer]
				midlow_income_data[column_name].append(rows[j][i].value)
				col_pointer += 1

		if col_pointer >= len(columns_order):
			break

## Parse Low income
low_income_book = xlrd.open_workbook(LOW_INCOME_INPUT_PATH)
low_income_data = {
	'year': [],
	'location': [],
	'total_house': [],
	'total_house_male': [],
	'total_house_female': [],
	'total_people': [],
	'total_people_male': [],
	'total_people_female': [],	
	'class_1_house': [],
	'class_2_house': [],
	'class_3_house': [],
	'class_1_house_male': [],
	'class_2_house_male': [],
	'class_3_house_male': [],
	'class_1_house_female': [],
	'class_2_house_female': [],
	'class_3_house_female': [],
	'class_1_people': [],
	'class_2_people': [],
	'class_3_people': [],
	'class_1_people_male': [],
	'class_2_people_male': [],
	'class_3_people_male': [],
	'class_1_people_female': [],
	'class_2_people_female': [],
	'class_3_people_female': [],
	'rate_of_house' : [],
	'rate_of_people': []
}

for sheet_number in range(1, low_income_book.nsheets):

	sheet = low_income_book.sheet_by_index(sheet_number)
	year  = re.match('\d+', sheet.name)
	year  = year.group()
		
	is_before_2003 = check_low_income_before_2003(int(year))
	is_last_q_data = False

	if year == str(CURRENT_LOW_INCOME_YEAR):
		regex_string = '中華民國\d+年第{0}季'.format(str(CURRENT_LOW_INCOME_SEASON))
		last_q_table_name_re = re.compile(regex_string)
	# 2006 and the years before using '年底' instead of 第4季
	elif int(year) == 2005 or int(year) == 2006:
		last_q_table_name_re = re.compile('中華民國\d+年底')
	elif int(year) > 2006:
		last_q_table_name_re = re.compile('中華民國\d+年第4季')
	# 2004 is an exceptinal year using 九十三年十二月底
	elif int(year) == 2004:
		last_q_table_name_re = re.compile('中華民國九十三年十二月底')
	# Only 2005 and 2006 years follow the below format
	else:
		last_q_table_name_re = re.compile('中華民國[八九]*十[一二三四五六七八九]*年底')

	for row_number in range(0, sheet.nrows):
			
		cells = sheet.row(row_number)

		if last_q_table_name_re.search(cells[0].value):
			is_last_q_data = True

		if is_last_q_data:
			locality_name = cells[0].value
			# city_match = city_re.search(locality_name)
			city_match = CITY_RE.search(locality_name)
			# if end_re.search(cells[0].value):
			if END_RE.search(cells[0].value):
				break
			elif city_match and is_before_2003:
				locality_name = city_match.group('name')
				parse_low_income_sheet_before_2003(year, locality_name, cells)
			elif city_match:
				locality_name = city_match.group('name')
				parse_low_income_sheet(year, locality_name, cells)
			elif TOTAL_RE.search(locality_name) and is_before_2003:
				locality_name = '全國'
				parse_low_income_sheet_before_2003(year, locality_name, cells)
			elif TOTAL_RE.search(locality_name):
				locality_name = '全國'
				parse_low_income_sheet(year, locality_name, cells)

order = [
	'year', 'location',
	'total_house', 'total_house_male', 'total_house_female', 'total_people', 'total_people_male', 'total_people_female', 
	'class_1_house', 'class_1_house_male', 'class_1_house_female', 'class_1_people', 'class_1_people_male', 'class_1_people_female', 
	'class_2_house', 'class_2_house_male', 'class_2_house_female', 'class_2_people', 'class_2_people_male', 'class_2_people_female', 
	'class_3_house', 'class_3_house_male', 'class_3_house_female', 'class_3_people', 'class_3_people_male', 'class_3_people_female', 
	'rate_of_house', 'rate_of_people' 
	]


low_income_dataframe = pd.DataFrame(low_income_data)
low_income_dataframe.to_csv(LOW_INCOME_OUTPUT_PATH, cols=order) 

## Parse Mid-low income
CURRENT_MIDLOW_INCOME_YEAR = 2017
CURRENT_MIDLOW_INCOME_SEASON = 1

midlow_income_book = xlrd.open_workbook(LOWMID_INCOME_INPUT_PATH)
midlow_income_data = {
	'year': [],
	'location': [],
	'total_house': [],
	'total_house_male': [],
	'total_house_female': [],
	'total_people': [],
	'total_people_male': [],
	'total_people_female': [],
	'total_people_below12': [],
	'total_people_below12_male': [],
	'total_people_below12_female': [],
	'total_people_between12_17': [],
	'total_people_between12_17_male': [],
	'total_people_between12_17_female': [],
	'total_people_between18_64': [],
	'total_people_between18_64_male': [],
	'total_people_between18_64_female': [],
	'total_people_over65': [],
	'total_people_over65_male': [],
	'total_people_over65_female': []
}

for sheet_number in range(1, midlow_income_book.nsheets):

	sheet = midlow_income_book.sheet_by_index(sheet_number)
	year  = re.match('\d+', sheet.name)
	year  = year.group()
	regex_string = '中華民國\d+年第4季'
	
	if year == str(CURRENT_MIDLOW_INCOME_YEAR):
		regex_string = '中華民國\d+年第{0}季'.format(str(CURRENT_MIDLOW_INCOME_SEASON))
		latest_q_table_re = re.compile(regex_string)
	else:
		latest_q_table_re = re.compile(regex_string)

	row_number = 0
	row_max_number   = sheet.nrows
	is_latest_q_data = False

	while row_number < row_max_number:

		cells = sheet.row(row_number)

		if latest_q_table_re.search(cells[0].value):
			is_latest_q_data = True

		if is_latest_q_data:

			rows = []
			location = '一個地方'
			should_parse = False
			total_search_result = TOTAL_RE.search(cells[0].value)
			city_search_result  = CITY_RE.search(cells[0].value)

			if END_RE.search(cells[0].value):
				break
			elif city_search_result:
				location = city_search_result.group('name')
				location = re.sub('\s+','', location)
				should_parse = True
			elif total_search_result:
				location = '全國'
				should_parse = True

			if should_parse:	
				rows.append(cells)
				rows.append(sheet.row(row_number+1))
				rows.append(sheet.row(row_number+2))
				parse_mid_lowincome(year, location, rows)
				row_number += 3
				continue
		
		row_number += 1

order = [
	'year', 'location',
	'total_house', 'total_house_male', 'total_house_female',
	'total_people','total_people_male','total_people_female',
	'total_people_below12','total_people_below12_male','total_people_below12_female',
	'total_people_between12_17', 'total_people_between12_17_male', 'total_people_between12_17_female',
	'total_people_between18_64', 'total_people_between18_64_male', 'total_people_between18_64_female',
	'total_people_over65', 'total_people_over65_male', 'total_people_over65_female'
]

midlow_income_dataframe = pd.DataFrame(midlow_income_data)
midlow_income_dataframe.to_csv(LOWMID_INCOME_OUTPUT_PATH, cols=order)

	





