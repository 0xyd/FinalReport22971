# -*- coding: UTF-8 -*-
import time
import urllib
import requests

# ZONE_CODE = {
# 	'cod03': 1, # 台北市
# 	'cod06': 1, # 台中市
# 	'cod04': 1, # 桃園市
# 	'cod09': 1, # 台南市
# 	'cod012': 1, # 高雄市
# 	'cod015': 1, # 宜蘭縣
# 	'cod016': 1, # 新竹縣
# 	'cod017': 1, # 苗栗縣
# 	'cod018': 1, # 彰化縣
# 	'cod019': 1, # 南投縣
# 	'cod020': 1, # 雲林縣
# 	'cod021': 1, # 嘉義縣
# 	'cod' 
# }

STAT_URL = 'http://statis.moi.gov.tw/micst/stmain.jsp?'

def get_data(city_code):

	query_para = {
		'sys': 220,
		'ym' : 8901,
		'ymt': 10512,
		'kind': 21,
		'type':  1,
		'funid': 'c0620102',
		'cycle': 41,
		'outmode' : 0,
		'compmode': 0,
		'outkind' : 1,
		'fldspc'  : '2,4,7,4,12,5,18,4,23,5,29,8,38,33,'
	}
	query_para[city_code] = 1
	url = STAT_URL + urllib.urlencode(query_para)

	try:
		r   = requests.get(url)
	except requests.exceptions.ChunkedEncodingError:
		print('%s request is fail' % city_code)
		return None

	if r.status_code == 200:
		return r.text
	else:
		print('No stat data')


if __name__ == '__main__':

	city_code = [ 'cod0'+str(i) for i in range(8, 9)]

	for code in city_code:
		data = get_data(code)
		if data:
			print('%s is get' % code)
			file_name = '../data/%s.html' % code
			f = open(file_name, 'w')
			f.write(data.encode('big5'))
			f.close()
		else:
			print('%s is not found' % code)







