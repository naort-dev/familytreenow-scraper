import scrapy
from scraper_api import ScraperAPIClient
import json
from datetime import datetime
import time
import csv
from bs4 import BeautifulSoup 
from familytreenow.items import SummaryItem, AddressItem, PossibleRelativeItem, RelativeSummaryItem, RelativeAddressItem
from familytreenow.utils import parse_input_row, generate_search_param, get_base_fields_from_input, get_recaptcha_answer, parse_address, check_is_relative
from familytreenow.settings import RECORDS_LIST, BIRTH_LABEL, SUMMARY_FIELD_MAPPING, ADDRESS_HEADING, POSSIBLE_RELATIVES_HEADING, RELATIVE_SUMMARY_FIELD_MAPPING, ASSOCIATED_NAMES_HEADING, ITEM_LIST, SCRAPER_API, PROXY

class FamilyTreeNowScraper(scrapy.Spider):
    name = "familytreenow"

    base_url = 'https://www.familytreenow.com'
    initial_search_url = 'https://www.familytreenow.com/search/genealogy/results?'
    relative_count = 0
    captcha_resolved = True
    total_requests = 0
    total_retries = 0
    client = None
    filter_cohort = ''
    filter_school = ''
    input_file = ''

    def __init__(self, *args, **kwargs):
      super(FamilyTreeNowScraper, self).__init__(*args, **kwargs) 
      if kwargs.get('cohort'):
        print(kwargs.get('cohort'))
        self.filter_cohort = kwargs.get('cohort')
      if kwargs.get('school'):
        self.filter_school = kwargs.get('school')
      if kwargs.get('input'):
        self.input_file = kwargs.get('input')

    def start_requests(self):
      # self.client = ScraperAPIClient(SCRAPER_API)
      if self.input_file == '':
        input_file = 'input'
        self.input_file = 'output'
      else:
        input_file = self.input_file

      h_list = open('{}.csv'.format(input_file))
      csv_reader = csv.reader(h_list, delimiter=',')
      for index, row in enumerate(csv_reader):
        if index == 0: continue
        input_data = parse_input_row(row)
        search_url = self.initial_search_url + generate_search_param(input_data)
        input_data['filter_cohort'] = self.filter_cohort
        input_data['filter_school'] = self.filter_school
        input_data['input_file'] = self.input_file
        print(search_url)
        if self.filter_school in input_data['school']:
          yield scrapy.Request(
            # url=self.client.scrapyGet(url = search_url, country_code = "US"), 
            url = search_url,
            callback=self.parse_search_result, 
            meta={'input': input_data, 'request_url': search_url})
        # break
      # for i in range(self.start * 6, (self.start + 1) * 6):
      #   state_url = '{}/businesses-for-sale-in-{}-{}'.format(self.base_url, US_STATE_ABBREV[US_STATE_SHORT[i]].replace(' ', '-'), US_STATE_SHORT[i])
      
    def handle_captcha(self, response, soup, parse_func):
      self.total_requests = 0
      print('Solving Captcha')
      retries = 0
      if 'retries' in response.meta:
        retries = response.meta['retries']
      if self.captcha_resolved and retries > 3:
        print('Solving Captcha')
        site_key = soup.find('div', class_='g-recaptcha').attrs['data-sitekey']
        action_url = soup.find('form').attrs['action']
        print(action_url, site_key)
        # get recaptcha_answer with 2captcha service
        recaptcha_answer = get_recaptcha_answer(site_key, response.meta['request_url'])
        print(self.base_url + action_url, recaptcha_answer)
        self.captcha_resolved = False
        yield scrapy.FormRequest(
          # url=self.client.scrapyGet(url = self.base_url + action_url, country_code = "US"),
          url = self.base_url + action_url,
          formdata={'g-recaptcha-response': recaptcha_answer},
          callback=parse_func,
          dont_filter=True,
          meta={'input': response.meta['input'] ,'captcha': True, 'request_url': self.base_url + action_url})
      else:
        print('Retrying')
        url = ''
        retries = 0
        if 'retry_url' not in response.meta:
          url = response.meta['request_url']
        else:
          url = response.meta['retry_url']
          self.total_retries = self.total_retries + 1
          retries = response.meta['retries']
          if self.total_retries > 30:
            self.captcha_resolved = True
            self.total_retries = 0
        print(response.url)
        print(url)
        yield scrapy.Request(
          # url=self.client.scrapyGet(url = url, country_code = "US"), 
          url = url,
          callback=parse_func, 
          dont_filter=True,
          meta={'input': response.meta['input'], 'retries': retries + 1, 'request_url': url, 'retry_url': url})

    def parse_search_result(self, response):
      soup = BeautifulSoup(response.body, features="html.parser")
      summaryResultsWrapper = soup.find('table', {'id': 'summaryResults'})
      print('================================================')
      print(response.url)
      input_data = response.meta['input']
      # check if response got captcha or not
      if not summaryResultsWrapper:
        print('Something went wrong during the search')
        for req in self.handle_captcha(response, soup, self.parse_search_result):
          yield req
        return
        
      self.total_requests = self.total_requests + 1
      if self.total_requests > 10:
        self.captcha_resolved = True

      results = summaryResultsWrapper.findAll('div', class_='row')
      searchnumber = 0
      is_relative = check_is_relative(input_data)
      if is_relative:
        relative_id = input_data['relative_id']
      input_data = get_base_fields_from_input(input_data)
      for result in results:
        detail_link = result.find('a', class_='summary-detail-link')
        
        if detail_link.text in RECORDS_LIST:
          print(input_data['student_no'], detail_link.attrs['href'])
          # input_data['search_number'] = '{}_{}'.format(input_data['student_no'], searchnumber)
          meta_data = input_data.copy()
          if is_relative:
            meta_data['relative_searchnumber'] = searchnumber
            meta_data['relative_id'] = relative_id
          else:
            meta_data['search_number'] = searchnumber
          url = self.base_url + detail_link.attrs['href']
          yield scrapy.Request(
            # url=self.client.scrapyGet(url = url, country_code = "US"), 
            url = url,
            callback=self.parse_detail_information, 
            meta={'input': meta_data, 'request_url': url})
          searchnumber = searchnumber + 1
      print('================================================')

    def parse_detail_information(self, response):
      soup = BeautifulSoup(response.body, features="html.parser")
      print('================================================')
      # print(soup.findAll('td', class_='detail-label')[0].text)
      data_tables = soup.findAll('table', class_='table-condensed')

      # check if response got captcha or not
      if len(data_tables) == 0:
        self.total_requests = 0
        for req in self.handle_captcha(response, soup, self.parse_detail_information):
          yield req
        return

      self.total_requests = self.total_requests + 1
      if self.total_requests > 10:
        self.captcha_resolved = True

      input_data = response.meta['input'].copy()
      is_relative = check_is_relative(input_data)
      print(input_data, is_relative)
      basic_information_table = data_tables[0]

      # summary item parser
      
      if is_relative:
        summary_item = RelativeSummaryItem(input_data)
        FIELD_MAPPING = RELATIVE_SUMMARY_FIELD_MAPPING
        summary_item['relative_associatedname_fromsearch'] = ''
        summary_item['item_type'] = ITEM_LIST[3]
      else:
        summary_item = SummaryItem(input_data)
        FIELD_MAPPING = SUMMARY_FIELD_MAPPING
        summary_item['associated_names'] = ''
        summary_item['item_type'] = ITEM_LIST[0]


      for row in basic_information_table.findAll('tr'):
        columns = row.findAll('td')
        summary_item[FIELD_MAPPING[columns[0].text]] = columns[1].text.strip()

      
      panels = soup.findAll('div', class_='panel-primary')
      for panel in panels:
        title = panel.find('div', class_='panel-heading')
        # associated names
        if title.text.strip() == ASSOCIATED_NAMES_HEADING:
          associated_names_table = panel.find('table', class_='table-striped')
          associated_names = ''
          for row in associated_names_table.findAll('tr'):
            associated_names = associated_names + row.text.strip() + ', '
          if associated_names != '':
             associated_names = associated_names.strip()[:-1]
          if is_relative:
            summary_item['relative_associatedname_fromsearch'] = associated_names
          else:
            summary_item['associated_names'] = associated_names
        # address item parser
        elif title.text.strip() == ADDRESS_HEADING:
          address_table = panel.find('table', class_='table-striped')
          for row in address_table.findAll('tr'):
            if is_relative:
              prefix = 'relative_'
              address_item = RelativeAddressItem(input_data)
              address_item['item_type'] = ITEM_LIST[4]
            else:
              prefix = ''
              address_item = AddressItem(input_data)
              address_item['item_type'] = ITEM_LIST[1]
            print(input_data)
            if row.find('a', class_='linked-record'):
              address = parse_address(row.find('a', class_='linked-record').text)
              address_item['{}timeframe'.format(prefix)] = row.find('em').text.strip()
              address_item['{}street'.format(prefix)] = address['street']
              address_item['{}state'.format(prefix)] = address['state']
              address_item['{}city'.format(prefix)] = address['city']
              address_item['{}zipcode'.format(prefix)] = address['zipcode']
              yield address_item

        # possible relative item parser
        elif title.text.strip() == POSSIBLE_RELATIVES_HEADING:
          if is_relative: continue
          relatives_table = panel.find('table', class_='table-striped')
          for index, row in enumerate(relatives_table.findAll('tr')):
            if index == 0: continue
            relative_item = PossibleRelativeItem(input_data)
            relative_item['relative_name'] = row.findAll('td')[0].find('a').text.strip()
            relative_item['relative_link'] = self.base_url + row.findAll('td')[0].find('a').attrs['href']
            relative_item['relative_age'] = row.findAll('td')[1].text.strip()
            relative_item['relative_birthyear'] = row.findAll('td')[2].text.strip()
            relative_item['relative_id'] = self.relative_count
            relative_item['item_type'] = ITEM_LIST[2]
            yield relative_item
            self.relative_count = self.relative_count + 1
            meta_data = input_data.copy()
            meta_data['relative_id'] = relative_item['relative_id']
            meta_data['relative_birthyear'] = relative_item['relative_birthyear']
            print(relative_item)
            yield scrapy.Request(
              # url=self.client.scrapyGet(url = relative_item['relative_link'], country_code = "US"),
              url = relative_item['relative_link'], 
              callback=self.parse_search_result, 
              meta={'input': meta_data, 'request_url': relative_item['relative_link']})
            # break

      yield summary_item
      print('================================================')
      