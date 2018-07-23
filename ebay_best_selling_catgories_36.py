import datetime
from ebaysdk.finding import Connection as finding
import requests
import csv
import sys
from bs4 import BeautifulSoup

category_codes = []
category_description = []
try:
    with open('us_category_ids.csv','r') as filein:
        reader = csv.reader(filein, delimiter =',')
        for row in reader:
            category_codes.append(row[0])
            category_description.append(row[1])
except FileNotFoundError as e:
    print(e)
    print(e.response.dict())
try:
    api = finding(appid='XXX-XXXXXX-XXXXX--XXXXX', config_file=None)
    filetextResults = 'ebay_best_sellers_by_category.txt'
    fileResults = open(filetextResults,'w')
    fileResults.close()
    print('The program is starting to harvets data...be patient')
    datetime_before = datetime.datetime.now()
    rang = 20
    for i in range(rang):
        if not (i%1):
            percent_complete = ((i*1)/rang)
            print('%.1f complete'%percent_complete)
        fileResults = open(filetextResults,'a')
        categorycode = category_codes[i].strip()
        categoryname = category_description[i].strip()
        Dictionary_ApiRequest = {
            'keywords': ' ',
            'categoryId': categorycode,
            'itemFilter': [
                {'name':'condition',
                 'value':'New'},
                {'name': 'LocatedIn',
                 'value': 'US'},
                {'name':'SoldItemsOnly',
                 'value':True},
                ]}
        response = api.execute('findCompletedItems',Dictionary_ApiRequest)
        soup = BeautifulSoup(response.content,'lxml')
        try: totalentries = soup.totalentries.text
        except:continue
        itemdetails = '\t'.join([categorycode,categoryname,totalentries])
        fileResults.write(itemdetails + '\n')
        fileResults.close()
    datetime_after = datetime.datetime.now()
    print('Your patience is highly appreciated. This is the end of data acquisition')
    time_difference = datetime_after - datetime_before
    print('Time taken to harvest the data '+ str(time_difference))
except ConnectionError as e:
    print(e)
    print(e.response.dict())


