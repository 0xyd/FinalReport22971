import re
import os
import csv

import numpy as np
import pandas as pd

PATH = '../警政署各縣市犯罪統計資料/'

if __name__ == '__main__':

	file_names = os.listdir(PATH)
	city_re    = re.compile('^(?P<name>[\u4e00-\u9fff]+(\(\d+年改制前\))*)\-\d+.tsv$')
	orders     = [
		'時間', '縣市',
		'一般及機車竊盜', '汽車竊盜', '贓物',	'賭博',	'重傷害',	 '一般傷害',	'詐欺背信', '妨害自由', '故意殺人', 
		'過失致死', '駕駛過失', '妨害家庭及婚姻',	 '妨害風化', '強制性交', '共同強制性交',	'對幼性交', '性交猥褻', '重大恐嚇取財',
		'一般恐嚇取財', '擄人勒贖',	 '侵占',	'偽造文書印文', '第一級毒品', '第二級毒品', '第三級毒品', '第四級毒品',
		'毀棄損壞', '妨害公務', '妨害電腦使用', '強盜', '搶奪', '內亂', '重利',	 '竊佔',	'偽造有價證券',
		'妨害秩序', '違反藥事法',	'違反國家總動員法', '違反森林法', '違反著作權法', '違反專利法', '違反商標法',	'公共危險', '侵害墳墓屍體',
		'妨害名譽', '違反就業服務法', '違反選罷法', '妨害秘密', '遺棄', '違反貪污治罪條例', '瀆職', '懲治走私條例', '妨害兵役'	,
		'偽造貨幣',	'偽造度量衡',	'偽證',	'誣告',	'湮滅證據',	'藏匿頂替', '脫逃', '違反槍砲彈藥刀械管制條例', '其他_x', '其他_y'
	]

	count_table = 0
	crime_main_dataframe = None
	crime_sub_dataframe  = None
	dataframe_collection = {}

	for file_name in file_names:

		try:
			city = city_re.search(file_name)
			city_name = city.group('name')

			# Initialise the data frame which will be used to merge another
			if city and count_table == 0:
				crime_main_dataframe = pd.read_csv(PATH+file_name, delimiter='\t')
				
			elif city:
				crime_sub_dataframe  = pd.read_csv(PATH+file_name, delimiter='\t')
				crime_main_dataframe = \
					pd.merge(crime_main_dataframe, crime_sub_dataframe, on='時間')

			count_table += 1
			
			# Each city has 7 tables of crimes...
			if count_table == 7:

				# Add the city name in the table
				row_number = crime_main_dataframe.shape[0]
				city_names  = np.array([city_name]*row_number)
				crime_main_dataframe['縣市'] = pd.Series(city_names)

				# Reinitialise the dataframe setting.
				dataframe_collection[city_name] = crime_main_dataframe
				crime_main_dataframe = None
				crime_sub_dataframe  = None
				count_table = 0

		except AttributeError:
			pass

	# Merge all dataframe into one big table
	mother_table = None
	dataframe_collection = [df for df in dataframe_collection.values()]
	mother_dataframe = pd.concat(dataframe_collection)
	mother_dataframe = mother_dataframe[orders] # Reoganise the table order following the order

	# Create total stat of each year.
	for year in range(89 ,106):

		year_re = '^{0}年$'.format(str(year))
		year_stat = mother_dataframe.loc[mother_dataframe['時間'].str.contains(year_re)]

		order = orders[0]
		row_number = year_stat[order].size
		col_number = len(orders)
		total_year_stat = year_stat.iloc[0:row_number, 2:col_number].as_matrix().sum(axis=0).reshape(1, col_number-2)
		total_year_df   = pd.DataFrame(total_year_stat, columns=orders[2:])
		total_year_df['時間'] = pd.Series(['{0}年'.format(str(year))])
		total_year_df['縣市'] = pd.Series(['全國'])
		total_year_df = total_year_df[orders]

		mother_dataframe = pd.concat([mother_dataframe, total_year_df])

	# Sum up all data in each row
	orders.append('總計')
	total_rows, total_columns = mother_dataframe.shape
	sum_row_stat = mother_dataframe.iloc[0:total_rows, 2:total_columns].sum(axis=1)
	mother_dataframe['總計'] = pd.Series(sum_row_stat)
	mother_dataframe = mother_dataframe[orders]
	
	month_stat_table = mother_dataframe.loc[mother_dataframe['時間'].str.contains(r'\d+年\s*\d+月')]
	month_stat_table.to_csv(PATH + 'month_crimes.csv', columns=orders)
	year_stat_table  = mother_dataframe.loc[mother_dataframe['時間'].str.contains(r'^\d+年$')]
	year_stat_table.to_csv(PATH + 'year_crimes.csv', columns=orders)





	