#!/usr/bin/env python
# -*- coding: utf-8 -*-
	
from lxml import html  
import json
import pickle 
import requests
import json,re
import email
import smtplib
from dateutil import parser as dateparser
from time import sleep

import progressbar



def ParseReviews(AsinList):

		bar = progressbar.ProgressBar(maxval=len(AsinList), \
    		widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		# Added Retrying 	
		reviewDict = {}
		nameDict = {}
		bar.start()
		count = 0
		    		
		for asin in AsinList:

			count = count + 1
			bar.update(count)
			
			amazon_url  = 'http://www.amazon.co.uk/dp/'+asin

			headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
			page = requests.get(amazon_url,headers = headers)
			page_response = page.text
			parser = html.fromstring(page_response)

			XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]//text()'
			XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'

			raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
			
			reviewTotal = parser.xpath(XPATH_AGGREGATE)
			
			if not reviewTotal:
				reviewTotal = 0

			else: 
				reviewTotal = int(reviewTotal[0].partition(' ')[0])

			
				
			
			product_name = ''.join(raw_product_name).strip()	

			reviewDict[asin] = reviewTotal	
			nameDict[asin] = product_name

		bar.finish()
		return {'Reviews':reviewDict, 'Names':nameDict}
			
def ReadAsin():
	
	#Add your own ASINs here 
	AsinList = ['B06WRNBF65',
	'B01N639B7G',
	'B01N8VON88',
	'B01MYM7MFX',
	'B01MYM7NE5',
	'B01N2G9RO3',
	'B01N1EQUFD',
	'B01N0D9LRT',
	'B01N8VONM3',
	'B01N6398XV',
	'B01MQIG1SQ',
	'B01N51UI90',
	'B01N1EQUW4',
	'B01N40BVY4',
	'B01MQIG0BR',
	'B01N8ZSVSA',
	'B01N51UI4G',
	'B01N40BUUH',
	'B01MTMXTB7',
	'B01MTMXNB6',
	'B01MTMXMY6',
	'B01N1EQGVO',
	'B01N2G9L83',
	'B01N51U5X6',
	'B01MYM7DE3',
	'B01MRJVDUT',
	'B01N40BM4E',
	'B01N8VO277',
	'B01MTMXO7X',
	'B01N638V0H',
	'B01MXKNVJE',
	'B01MTMX79X',
	'B01N8RLIDW',
	'B01N637RF7',
	'B01MSLGB1B',
	'B01N8ZPZI9',
	'B01N2G945F',
	'B01MYM6ZGB',
	'B01N2G92TI',
	'B01MQIFB04',
	'B01MTMX2R6',
	'B01MQIFDJO',
	'B01N8RLD6W',
	'B01N1EQ21V',
	'B01MRJUTYN',
	'B01N40AK5P',
	'B01N0D8GBX',
	'B01MSLFSZE',
	'B01N6382FP',
	'B01N638259',
	'B01MSLFTQD',
	'B01N2G8O16',
	'B01MQIF0Y9',
	'B01N8VNKWC',
	'B01N8VNFXW',
	'B01N0D80VJ',
	'B01N928RR8',
	'B01MSLFJW2',
	'B01N1EOZCB',
	'B01MSLFG1Q',
	'B01MRJU19B',
	'B01N637O7W',
	'B01MSLFHRR',
	'B01MSLFGHY',
	'B01N637QTC',
	'B01N40A9FS',
	'B01MQIEOOT',
	'B01N51SDST',
	'B01N8ZQX4M',
	'B01N1EOV92',
	'B01N2G7U41',
	'B01N92CCR6',
	'B01MXKMJX8',
	'B01N636867',
	'B01N6378YF',
	'B01MXKMMJE',
	'B01MRJTLZV',
	'B01N0D5PV1',
	'B01MXF7OUN',
	'B01MQH7MFC',
	'B01MXJDW5D',
	'B01N07ROX8',
	'B01N03NRB9',
	'B01N03NRY7',
	'B01MRINCZ3',
	'B01N03NUZS',
	'B01N0BXEKR',
	'B01N03NRA4',
	'B01N3UT7SX',
	'B01N3MLA3C',
	'B01N8QDTBC',
	'B01N07RWUP',
	'B01MTLQ9UY',
	'B01MXJ0M5R',
	'B01MQH7PNX',
	'B01N8Q0CH4',
	'B01N07RVPZ',
	'B01N3M7KQ4',
	'B01N0BK61D',
	'B01MRI9WBY',
	'B01N07EJZ6',
	'B01N3QDCP5',
	'B01N07EPH4',
	'B01N8XG0JJ',
	'B01MXJ0QSI',
	'B01MQGUA6J',
	'B01MQH7HD4',
	'B01MXF7OV0',
	'B01MQH7MVO',
	'B01N8QDXH1',
	'B01N8Q0QEP',
	'B01N3UT4XD',
	'B01N8UH1RD',
	'B01MXJ0MWN',
	'B01N3YW6AP',
	'B01N3ML7UG',
	'B01MQH7NN0',
	'B01N3UTDNV']

	
	print ("Downloading and processing page")
	
	reviews = ParseReviews(AsinList)

	print (reviews['Reviews'])
	

	save_obj(reviews['Reviews'], 'Reviews')
	save_obj(reviews['Names'], 'Names')

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


	

if __name__ == '__main__':
	ReadAsin()