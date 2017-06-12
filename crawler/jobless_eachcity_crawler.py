import urllib
import requests

URL = 'http://win.dgbas.gov.tw/dgbas04/bc4/manpower/year/year_t24-t71.asp?'
OUTPUT_PATH = '../data/各縣市每年度失業者年齡層'

def crawl(year):

	q = {
		'table': 36,
		'yearb': year,
		'yeare': year,
		'out'  : 1
	}
	q = urllib.parse.urlencode(q)
	url = URL + q
	r   = requests.get(url)
	file_name = '民國{0}年各縣市失業者年齡層.html'.format(str(year))

	return (file_name, r.text)


def output_file(file_name, data):

	file_name = '/'.join(['..', 'data', OUTPUT_PATH, file_name])
	file = open(file_name, 'w', encoding='utf8')
	file.write(data)
	file.close()

if __name__ == '__main__':

	# Crawl 
	for year in range(82, 100):
		file_name, data = crawl(year)
		output_file(file_name, data)

	for year in range(100, 104):
		file_name, data = crawl(year)
		output_file(file_name, data)

	for year in range(104, 106):
		file_name, data = crawl(year)
		output_file(file_name, data)


		








