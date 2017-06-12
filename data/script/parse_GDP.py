import xlrd
import numpy  as np
import pandas as pd

PATH = '/'.join(['..', '全國GDP與人均所得', 'table(022).xls'])
book = xlrd.open_workbook(PATH)
stat_data = book.sheet_by_index(1)

output_original_gdp = '/'.join(['..', '全國GDP與人均所得', 'origin_gdp.csv'])
output_year_gdp = '/'.join(['..', '全國GDP與人均所得', 'year_gdp.csv'])

col_orders = [
	'year', 'population', 'exchange_rate', 'economy_growth',
	'gdp_nt_dollar(unit: million)', 'gdp_us_dollar(unit: million)', 'gdp_avg_nt_dollar', 'gdp_avg_us_dollar',
	'gni_nt_dollar(unit: million)', 'gni_us_dollar(unit: million)', 'gni_avg_nt_dollar', 'gni_avg_us_dollar',
	'ni_nt_dollar', 'ni_us_dollar', 'avg_income_nt_dollar', 'avg_income_us_dollar']

years = []
population = []
exchange_rate  = []
economy_growth = []
gdp_nt_dollar  = []
gdp_us_dollar  = []
gdp_avg_nt_dollar = []
gdp_avg_us_dollar = []
gni_nt_dollar  = []
gni_us_dollar  = []
gni_avg_nt_dollar = []
gni_avg_us_dollar = []
ni_nt_dollar  = []
ni_us_dollar  = []
avg_income_nt_dollar = []
avg_income_us_dollar = []

for row_index in range(4, stat_data.nrows-4):

	cells = stat_data.row(row_index)
	years.append(cells[0].value)
	population.append(cells[1].value)
	exchange_rate.append(cells[2].value)
	economy_growth.append(cells[3].value)
	gdp_nt_dollar.append(cells[4].value)
	gdp_us_dollar.append(cells[5].value)
	gdp_avg_nt_dollar.append(cells[6].value)
	gdp_avg_us_dollar.append(cells[7].value)
	gni_nt_dollar.append(cells[8].value )
	gni_us_dollar.append(cells[9].value)
	gni_avg_nt_dollar.append(cells[10].value)
	gni_avg_us_dollar.append(cells[11].value)
	ni_nt_dollar.append(cells[12].value)
	ni_us_dollar.append(cells[13].value)
	avg_income_nt_dollar.append(cells[14].value)
	avg_income_us_dollar.append(cells[15].value)

years = np.array(years)
population   = np.array(population)
exchange_rate = np.array(exchange_rate)
economy_growth = np.array(economy_growth)
gdp_nt_dollar  = np.array(gdp_nt_dollar)
gdp_us_dollar  = np.array(gdp_us_dollar)
gdp_avg_nt_dollar = np.array(gdp_avg_nt_dollar)
gdp_avg_us_dollar = np.array(gdp_avg_us_dollar)
gni_nt_dollar = np.array(gni_nt_dollar)
gni_us_dollar = np.array(gni_us_dollar)
gni_avg_nt_dollar = np.array(gni_avg_nt_dollar)
gni_avg_us_dollar = np.array(gni_avg_us_dollar)
ni_nt_dollar  = np.array(ni_nt_dollar)
ni_us_dollar  = np.array(ni_us_dollar)
avg_income_nt_dollar = np.array(avg_income_nt_dollar)
avg_income_us_dollar = np.array(avg_income_us_dollar)

gdp_df = pd.DataFrame(
	{
		'year': years,
		'population': population,
		'exchange_rate': exchange_rate,
		'economy_growth' : economy_growth,
		'gdp_nt_dollar(unit: million)'  : gdp_nt_dollar,
		'gdp_us_dollar(unit: million)'  : gdp_us_dollar,
		'gdp_avg_nt_dollar' : gdp_avg_nt_dollar,
		'gdp_avg_us_dollar' : gdp_avg_us_dollar,
		'gni_nt_dollar(unit: million)'  : gni_nt_dollar,
		'gni_us_dollar(unit: million)'  : gni_us_dollar,
		'gni_avg_nt_dollar' : gni_avg_nt_dollar,
		'gni_avg_us_dollar' : gni_avg_us_dollar,
		'ni_nt_dollar'  : ni_nt_dollar,
		'ni_us_dollar'  : ni_us_dollar,
		'avg_income_nt_dollar' : avg_income_nt_dollar,
		'avg_income_us_dollar' : avg_income_us_dollar
	})
gdp_df.to_csv(output_original_gdp,cols = col_orders)

year_gdp_df = gdp_df.loc[gdp_df['year'].str.contains(r'\d+年')]
year_gdp_df.to_csv(output_year_gdp, cols=col_orders)

	
