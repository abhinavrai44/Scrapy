import scrapy
import nltk
import csv
import pandas as pd
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule, CrawlSpider

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = [""]
    start_urls = [""]

    def __init__(self):
        self.all_links = []
        self.count = 0
        self.meta_data = {}

    def parse(self, response):
        # Extract whole website
        extractor = LinkExtractor(allow_domains='')
        links = extractor.extract_links(response)
        for link in links:
            if(link.url not in self.all_links):
                self.count += 1
                print self.count
                self.all_links.append(link.url)
                
                for content in response.xpath('//meta[@name=\'keywords\']/@content').extract():
                    content = content.split(',')
                    for string in content:
                        if string in self.meta_data.keys():
                            self.meta_data[string] += 1
                        else:
                            if (string==''):
                                continue
                            else:
                                self.meta_data[string] = 1

                    
                yield scrapy.Request(link.url, callback=self.parse)

        # print self.count
        data = json.dumps(self.meta_data)
        file = open("output.json","w")
        file.write(data)
