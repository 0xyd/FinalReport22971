長庚大學期末專題：民貧，則奸邪生？
================

主題：民貧，則奸邪生？
======================

假設：大環境不景氣會導致犯罪的氾濫
----------------------------------

自古以來，我們都必然斷定犯罪皆始於貧窮，所以有『饑寒起盜心』之諺。明朝末年的連年饑荒，農民無法耕作，且賦稅、徭役亦重。農民不堪謀生的壓力，聚集成了流寇在各地打劫作亂，最後揭竿而起，滅亡了大明。除了大明朝以外，俄國七月革命，無產階級結束了沙俄時代，俄國因此成為蘇維埃。我們可知，古今中外不乏因為經濟景況惡化造成社會的大幅動蕩，最終導致政權崩塌的例子。

從歷史的經驗來觀察：經濟情況的惡化、民不聊生時，社會就會有許多騷亂，小則治安敗壞，民不敢出戶；大則流血暴動，國家政權被顛覆。故此，我們的假設就是大環境的不佳，將會促成犯罪的滋長。

資料介紹與其格式
----------------

1.  資料名稱：警政署各縣市犯罪統計 資料格式：html 資料內容：警政署統計的犯罪共有62個項目，只要是被逮捕的犯罪嫌疑人都會被統計。年度從民國89年到民國105年。

2.  資料名稱：衛福部低收入戶統計 資料格式：xls 資料內容：衛福部針對低收入戶戶數、人數、所佔比例與性別的統計，並且針對不同類型的低收入戶作統計。除了全國的資料，各年度的資料中也包含各縣市低收入戶的統計數據。年度表單都有針對各縣市四個季的統計表。

3.  資料名稱：衛福部中低收入戶統計 資料格式：xls 資料內容：衛福部從2011年開始統計中都收入戶，有人數、戶數、男女人數以及針對個年齡層的統計。

4.  資料名稱：內政部戶政司 資料格式：xls 資料內容：內政部戶政司統計民國63年到民國105年各縣市人數統計與性別人數。

5.  資料名稱：行政院主計處薪資與生產力統計 資料格式：xls 資料內容：主計處提供該年度GDP、經濟成長率與平均每人所得。

資料爬蟲與解析器(使用Python以利未來系統運用)
--------------------------------------------

### 警政署各縣市犯罪統計爬蟲

``` python
import time
import urllib
import requests

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
```

### 警政署各縣市犯罪統計HTML解析器

``` python
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
```

### 警政署資料合併

``` python
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
        '一般及機車竊盜', '汽車竊盜', '贓物',    '賭博',   '重傷害',   '一般傷害',    '詐欺背信', '妨害自由', '故意殺人', 
        '過失致死', '駕駛過失', '妨害家庭及婚姻',   '妨害風化', '強制性交', '共同強制性交',  '對幼性交', '性交猥褻', '重大恐嚇取財',
        '一般恐嚇取財', '擄人勒贖',    '侵占',  '偽造文書印文', '第一級毒品', '第二級毒品', '第三級毒品', '第四級毒品',
        '毀棄損壞', '妨害公務', '妨害電腦使用', '強盜', '搶奪', '內亂', '重利',    '竊佔',  '偽造有價證券',
        '妨害秩序', '違反藥事法',    '違反國家總動員法', '違反森林法', '違反著作權法', '違反專利法', '違反商標法',    '公共危險', '侵害墳墓屍體',
        '妨害名譽', '違反就業服務法', '違反選罷法', '妨害秘密', '遺棄', '違反貪污治罪條例', '瀆職', '懲治走私條例', '妨害兵役'    ,
        '偽造貨幣', '偽造度量衡',    '偽證',   '誣告',   '湮滅證據', '藏匿頂替', '脫逃', '違反槍砲彈藥刀械管制條例', '其他_x', '其他_y'
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
```

### 衛福部低收入戶xls統計解析器

``` python
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
```

### 主計處GDP解析器

``` python
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
```

### 戶政人口資料解析器

``` python
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
```

探索式分析結果
--------------

### 台灣犯罪總數趨勢圖

![台灣犯罪總數趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/台灣犯罪案件趨勢圖.png)

![犯罪案件總數與財產犯罪](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/台灣犯罪總數與財產犯罪趨勢圖.png)

![犯罪案件總數與侵害個人法益犯罪](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/台灣犯罪總數與侵害個人法益犯罪趨勢圖.png)

![犯罪案件總數與毒品案件](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/台灣犯罪總數與毒品犯罪趨勢圖.png)

![犯罪案件總數與公共危險案件](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/台灣犯罪總數與公共危險犯罪趨勢圖.png)

![台灣平均收入趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/台灣平均所得趨勢圖.png)

![全國低收入戶成長趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/台灣低收入戶人數趨勢.png)

![全國中低收入戶趨勢圖](https://github.com/yudazilian/FinalReport22971/blob/master/images/台灣中低收入戶趨勢圖.png)

![各縣市犯罪人口佔全國犯罪人口比例](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/台灣各縣市犯罪人口佔總犯罪人口比例圖.png)

![各縣市四大類型犯罪人口佔全國四大類型犯罪人口比例](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/台灣各縣市四大類犯罪人口比例圖.png)

![所得與犯罪](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/2015年各縣市平均所得與犯罪人數組圖.png)

![五都縣市合併前後犯罪人數的變化](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/五都縣市合併前後犯罪人數的變化.png)

![台北縣改制新北市犯罪人數與低收入戶人數趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/台北縣改制新北市犯罪人數與低收入戶人數趨勢圖.png)

![台中縣市合併前後犯罪人數與低收入戶人數的變化](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/Screen%20Shot%202017-06-12%20at%203.55.35%20PM.png)

![臺南縣市合併前後犯罪人數與低收入戶人數的變化](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/Screen%20Shot%202017-06-12%20at%203.55.50%20PM.png)

![高雄縣市合併前後犯罪人數與低收入戶人數趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/高雄縣市合併前後犯罪人數與低收入戶人數趨勢圖.png)

![104年全國前五高犯罪率城市](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/民國104年全國前五高犯罪率城市.png)

![基隆市犯罪人數與低收入戶數趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/基隆市犯罪人數與低收入戶數趨勢圖.png)

![宜蘭縣犯罪人數與低收入戶數趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/宜蘭縣犯罪人數與低收入戶數趨勢圖.png)

![花蓮縣犯罪人數與低收入戶數趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/花蓮縣犯罪人數與低收入戶數趨勢圖.png)

![台東縣犯罪人數與低收入戶數趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/台東縣犯罪人數與低收入戶數趨勢圖.png)

![台北市犯罪人數與低收入戶數趨勢圖](https://github.com/yudazilian/FinalReport22971/blob/master/images/台北市犯罪人數與低收入戶數趨勢圖.png)

![民國90-104年基隆市失業率與犯罪率趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/民國90-104年基隆市失業率與犯罪率趨勢圖.png)

![民國90-104年宜蘭縣失業率與犯罪率趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/民國90-104年宜蘭縣失業率與犯罪率趨勢圖.png)

![民國90-104年花蓮縣失業率與犯罪率趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/民國90-104年花蓮縣失業率與犯罪率趨勢圖.png)

![民國90-104年台東縣失業率與犯罪率趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/民國90-104年台東縣失業率與犯罪率趨勢圖.png)

![民國90-104年台北市失業率與犯罪率趨勢圖](https://raw.githubusercontent.com/yudazilian/FinalReport22971/master/images/民國90-104年台北市失業率與犯罪率趨勢圖.png)
