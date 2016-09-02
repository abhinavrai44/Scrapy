import scrapy
import nltk
import csv
import pandas as pd
import json
from scrapy.linkextractors import LinkExtractor
# from scrapy.contrib.linkextractors import LxmlLinkExtractor
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
                    # print "Content : ", content
                    # f.write(content)
                    content = content.split(',')
                    # print "C : "
                    for string in content:
                        # print string
                        if string in self.meta_data.keys():
                            self.meta_data[string] += 1
                        else:
                            if (string==''):
                                continue
                            else:
                                self.meta_data[string] = 1

                    # print self.meta_data
                    # words = []
                    # flag = 0
                    # for c in content:
                    #     if(flag == 0):
                    #         flag = 1
                    #     else:
                    #         if (c == ','):
                    #             string = ''.join(words)

                    #             if string in self.meta_data.keys():
                    #                 self.meta_data[string] += 1
                    #             else:
                    #                 if (string==''):
                    #                     continue
                    #                 else:
                    #                     self.meta_data[string] = 1
                    #             words = [] 

                    #         else:
                    #             words.append(c)
                yield scrapy.Request(link.url, callback=self.parse)

        # print self.count
        data = json.dumps(self.meta_data)
        file = open("output.json","w")
        # print "abho"
        file.write(data)

        # print self.meta_data

        # Extract one webpage
        # filename = str(self.count) + '.txt'

        # with open(filename, 'wb') as f:
        #   for content in response.xpath('//meta[@name=\'keywords\']/@content').extract():
        #       print "Content : ", content
  #             # f.write(content)
  #             words = []
  #             for c in content:
  #                 if c==' ':
  #                     continue
  #                 if (c == ','):
  #                     string = ''.join(words)

  #                     if string in self.meta_data.keys():
     #                      self.meta_data[string] += 1
     #                  else:
     #                      self.meta_data[string] = 1
     #                  words = [] 

  #                 else:
  #                     words.append(c)
        # print
        # print self.meta_data