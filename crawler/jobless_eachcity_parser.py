import lxml.html

PATH = '../data/各縣市每年度失業者年齡層/'
OUTPUT = 'jobless_age_disb.csv'

def access_data(year):

	file = '民國{}年各縣市失業者年齡層.html'.format(str(year))
	string = open(PATH+file, 'r')
	string = string.readlines()
	string = ''.join(string)
	html_doc = lxml.html.fromstring(string)
	
	return html_doc.cssselect('table')[1]

def access_rows(para):

	# The start index is 3.
	for index in range(3, 3+len(para['locations'])):

		elements = []
		data_row = para['data_rows'][index]
		data_cols = data_row.cssselect('td')
		loc_index = index - 3
		loc_name  = para['locations'][loc_index]
		
		# access column data
		col_data = access_cols(data_cols)
		col_data = [ '0' if col_d == '       -' else col_d for col_d in col_data ]
		elements = [ str(year), loc_name ]
		elements += col_data

		para['csv_file'].write(','.join(elements))
		para['csv_file'].write('\n')

def access_cols(row_data):

	data = []

	cols = [
		1, 2, 3, 7, 8, 9, 10, 11, 12, 16, #10
		17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 
		31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45
	]
	
	for col in cols:
		d = row_data[col].cssselect('font')[0].text_content()
		data.append(d)

	return data

if __name__ == '__main__':

	csv_file = open(PATH+OUTPUT, 'w')

	# Build headers:
	heads = [
		'year', 'loc', 'total', 'male', 'female', 
		'15-19', '15-19m', '15-19f', 
		'20-24', '20-24m', '20-24f', 
		'25-29', '25-29m', '25-29f',
		'30-34', '30-34m', '30-34f',
		'35-39', '35-39m', '35-39f',
		'40-44', '40-44m', '40-44f',
		'45-49', '45-49m', '45-49f',
		'50-54', '50-54m', '50-54f',
		'55-59', '55-59m', '55-59f',
		'60-64', '60-64m', '60-64f',
		'65-', '65-m', '65-f'
	]
	
	csv_file.write(','.join(heads))
	csv_file.write('\n')

	for year in range(82, 100):

		locations  = [
			'臺灣地區', '北部區域', '臺北市', '基隆市', '新竹市',
			'臺北縣', '宜蘭縣', '桃園縣', '新竹縣', '中部區域',
			'臺中市', '苗栗縣', '臺中縣', '彰化縣', '南投縣',
			'雲林縣', '南部區域', '高雄市', '嘉義市', '臺南市',
			'嘉義縣', '臺南縣', '高雄縣', '屏東縣', '澎湖縣',
			'東部區域', '臺東縣', '花蓮縣'
		]

		data_table = access_data(year)
		data_rows  = data_table.cssselect('tr')
		
		para = {
			'csv_file' : csv_file,
			'locations': locations,
			'data_rows': data_rows
		}
		
		access_rows(para)
		
	for year in range(100, 104):
		
		locations = [
			'臺灣地區', '北部區域', '新北市(100年五都改制)', '臺北市', '基隆市',
			'新竹市', '宜蘭縣', '桃園縣', '新竹縣', '中部區域',
			'臺中市(100年五都改制)', '苗栗縣', '彰化縣','南投縣','雲林縣',
			'南部區域','臺南市(100年五都改制)', '高雄市(100年五都改制)', '嘉義市', '嘉義縣',
			'屏東縣', '澎湖縣', '東部區域', '臺東縣', '花蓮縣'
		]

		data_table = access_data(year)
		data_rows  = data_table.cssselect('tr')
		para = {
			'csv_file' : csv_file,
			'locations': locations,
			'data_rows': data_rows
		}
		
		access_rows(para)

	for year in range(104, 106):

		locations = [
			'臺灣地區','北部區域','新北市','臺北市','桃園市(103年升格)',
			'基隆市','新竹市','宜蘭縣','新竹縣','中部區域',
			'臺中市','苗栗縣','彰化縣','南投縣','雲林縣',
			'南部區域','臺南市','高雄市','嘉義市','嘉義縣',
			'屏東縣','澎湖縣','東部區域','臺東縣','花蓮縣'
		]

		data_table = access_data(year)
		data_rows  = data_table.cssselect('tr')
		para = {
			'csv_file' : csv_file,
			'locations': locations,
			'data_rows': data_rows
		}
		
		access_rows(para)


			





