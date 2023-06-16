# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time
import datetime
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from familytreenow.settings import ITEM_LIST, FIELDS_LIST

class FamilytreenowPipeline(object):
    def __init__(self):
        self.files = {}
        self.exporter = {}
        self.start = False
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        # crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    # def spider_opened(self, spider):
    #     for item in ITEM_LIST:
    #         file = open('{}.csv'.format(item), 'w+b')
    #         self.files[item] = file
    #         self.exporter[item] = CsvItemExporter(file)
    #         self.exporter[item].fields_to_export = FIELDS_LIST[item]
    #         self.exporter[item].start_exporting()

    def spider_closed(self, spider):
        for item in ITEM_LIST:
            self.exporter[item].finish_exporting()
            file = self.files.pop(item)
            file.close()

    def process_item(self, item, spider):
        # self.exporter.export_item(item)
        if not self.start:
            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            self.start = True
            
            
            if item['filter_cohort'] == '' and item['filter_school'] == '':
                prefix = ''
            else:
                prefix = '{}_{}'.format(item['filter_cohort'], item['filter_school'])
            for row in ITEM_LIST:
                file = open('output/{}__{}_{}.csv'.format(item['input_file'], prefix, row), 'w+b')
                self.files[row] = file
                self.exporter[row] = CsvItemExporter(file)
                export_fields = FIELDS_LIST[row].copy()
                del export_fields[:3]
                self.exporter[row].fields_to_export = export_fields
                self.exporter[row].start_exporting()
        print('++++++++++++++++++++++')
        print(item)
        self.exporter[item['item_type']].export_item(item)
        print('++++++++++++++++++++++')
        return item