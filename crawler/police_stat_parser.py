# -*- coding: UTF-8 -*-
import lxml.html

paths = ['../data/cod0{}.html'.format(str(i)) for i in range(1, 31) ]

for path in paths:

	try:
		f = open(path, 'r', encoding='big5')
		html = ''.join(f.readlines())
		html = lxml.html.fromstring(html)

		tables  = html.cssselect('table')[1:]

		for it, table in enumerate(tables):

			trs = table.cssselect('tr')
			crimes = trs[0].cssselect('th')
			cities = trs[1].cssselect('th')
			crimes = [crime.text for crime in crimes]
			city   = [city.text for city in cities][1]

			output = open('../data/{0}-{1}.tsv'.format(city, str(it)), 'w')

			# Buiid csv headers
			crimes[0] = '時間'
			output.write('\t'.join(crimes))
			output.write('\n')

			for tr in trs[2:]:
				# data = [ d.text if d.text != ' - ' else str(0) for d in tr ]
				data = [ d.text.replace(',','').strip() if d.text != ' - ' else str(0) for d in tr ]
				output.write('\t'.join(data))
				output.write('\n')

			output.close()

	except Exception as e:
		print(e)
		pass
	
