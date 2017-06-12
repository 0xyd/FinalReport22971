# -*- coding: UTF-8 -*-
import re
import unittest
import lxml.html

class TestCrawlerAndParser(unittest.TestCase):

	def test_crawler_result(self):

		code_table = open('../data/code_table.txt', 'w')

		# 桃園縣、台中縣、台南縣、高雄縣已不復見
		citie_names = set([
			'臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市',
			'基隆市', '新竹市', '嘉義市', '新竹縣', '苗栗縣', '彰化縣',
			'南投縣', '雲林縣', '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣',
			'臺東縣', '澎湖縣', '金門縣', '連江縣', '桃園縣', '高雄縣',
			'臺中縣', '臺南縣'])
		collected_cities = set([])
		paths = [ '../data/cod0' + str(i) + '.html' for i in range(1, 31)]

		for path in paths:	
			try:
				f = open(path, 'r', encoding='big5')
				html_text = ''.join(f.readlines())
				html  = lxml.html.fromstring(html_text)
				table = html.cssselect('table')[1]
				tr    = table.cssselect('tr')[1]
				th    = tr.cssselect('th')[1]
				city_name = th.text
				city_name = re.search('(?P<name>[\u4e00-\u9fff]+)', city_name).group('name')
				collected_cities.add(city_name)

				code_table.write('{0}\t{1}\n'.format(path, city_name))
			except IOError as e:
				pass

		for miss_citiy in citie_names.difference(collected_cities):
			print('City %s is missed. ' % miss_citiy)

		self.assertEqual(citie_names.difference(collected_cities), set())
		code_table.close()


if __name__ == '__main__':
	
	unittest.main()
			
