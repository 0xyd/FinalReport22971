import re
import xlrd
import numpy  as np
import pandas as pd

PATH = '/'.join(['..', '全國人口統計', '縣市人口按性別及五齡組.xls'])
book = xlrd.open_workbook(PATH)

START_YEAR = 105
END_YEAR   = 90

population_collection = {
	'year': [],
	'locality'  : [],
	'population': []
}

orders = ['year', 'locality', 'population']


for sheet_number in range(0,START_YEAR-END_YEAR+1):

	year = START_YEAR - sheet_number
	sheet = book.sheet_by_index(sheet_number)

	for row in range(0, sheet.nrows):

		cells = sheet.row(row)
		city_name = re.sub('\s', '', cells[0].value)
		city_name = re.search(r'^[\u4e00-\u9fff]{2}(市|縣)$', city_name)
		
		if city_name:
			city_name = city_name.group()
			population_collection['year'].append(year)
			population_collection['locality'].append(city_name)
			population_collection['population'].append(sheet.cell(row-1, 2).value)

population_dataframe  = pd.DataFrame(population_collection)
population_dataframe.to_csv('../全國人口統計/各縣市人口統計.csv', columns=orders)









