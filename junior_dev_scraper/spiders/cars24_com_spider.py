# Please run this command to retrieve the csv file: scrapy runspider cars24_com_spider.py -o cars.csv

import scrapy
import json
import re
from benedict import benedict
from w3lib.url import add_or_replace_parameter

two_words_brands = ['MERCEDES BENZ',
'LAND ROVER',
'ALFA ROMEO',
'ASTON MARTIN']

class Car24ComSpider(scrapy.Spider):
    name = 'cars24_com_spider'

    start_urls =[f'https://www.cars24.com/ae/buy-used-cars-dubai?&page={i}' for i in range(55)]

    def parse(self, response):
        yield from self.extract_car_data(response)
        
    def extract_car_data(self, response):
        for car in response.css('div._3IIl_._1xLfH'):

            features = car.css('ul._3ZoHn li::text').getall()
            brand_model = car.css('h3.RZ4T7::text').get()

            car_url = car.css('a._1Lu5u::attr(href)').get()
            price = car.css('span._7yds2::text').get()

            brand = None
            model = None

            for brand_name in two_words_brands:
                if brand_name.lower().strip() in brand_model.lower().strip():
                    brand = brand_name
                    model = ' '.join(brand_model.split(' ')[2:])
                    break 

            if brand is None:
                brand = brand_model.split(' ')[0]
                model = ' '.join(brand_model.split(' ')[1:])
            
            details = car.css('p._1i1E6::text').get()
            year_of_manufacture = details.split('|')[0].strip()

            fuel_type = details.split('|')[1].strip()
            if 'electric' in str(fuel_type).lower():
                fuel_type = 'ELECTRIC'
            elif 'hybrid' in str(fuel_type).lower():
                fuel_type = 'HYBRID'
            else:
                fuel_type = 'PETROL'

            mileage = features[1]
            engine_size = features[2]

            car_item = {
               'brand': brand,
               'engine_size':engine_size,
               'year_of_manufacture':year_of_manufacture,
               'deep_link':car_url,
               'fuel_type':fuel_type,
               'price_aed': price,
               'model':model,
               'mileage':mileage                
            }

            yield car_item