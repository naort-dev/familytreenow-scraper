# -*- coding: utf-8 -*-

# Scrapy settings for familytreenow project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'familytreenow'

SPIDER_MODULES = ['familytreenow.spiders']
NEWSPIDER_MODULE = 'familytreenow.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'familytreenow (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DUPEFILTER_DEBUG = True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 40

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
  
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'familytreenow.middlewares.FamilytreenowSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'familytreenow.middlewares.FamilytreenowDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'familytreenow.pipelines.FamilytreenowPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
SCRAPER_API = '277c3c9f2bb9cd9446c23cb9cff3032e'
PROXY = 'http://scraperapi.country_code=us:277c3c9f2bb9cd9446c23cb9cff3032e@proxy-server.scraperapi.com:8001'
# PROXY = ''

INPUT_COLUMN = [
   'student_no',
   'school',
   'subschool',
   'degree',
   'degree_conferred_date',
   # 'cohort',
   'commencement_name',
   'first_name',
   'middle_name',
   'last_name',
   'major',
   'city',
   'state',
   'country',
   'honors', 
   'distinct',
   'birthyear'
]

SEARCH_PARAM = {
   'first_name': 'first',
   'middle_name': 'middle',
   'last_name': 'last',
   'location': 'citystatezip',
   'birthyear': 'dobyyyy'
}

CAPTCHA_KEY = '372689742a0bf4b7d80ad479c275b2f2'
RECORDS_LIST = ['Living People Records']
BIRTH_LABEL = 'Birth:'

ITEM_LIST = ['summary', 'address', 'possible_relatives', 'relative_summary', 'relative_address']
BASE_FIELDS_FROM_INPUT = ['input_file', 'filter_cohort', 'filter_school', 'search_number', 'commencement_name', 'student_no', 'school', 'cohort']
FIELDS_LIST = {
    'summary': ['input_file', 'filter_cohort', 'filter_school', 'search_number', 'commencement_name', 'student_no', 'school', 'cohort', 'fullname', 'birthyear', 'age', 'associated_names'],
    'address': ['input_file', 'filter_cohort', 'filter_school', 'search_number', 'commencement_name', 'student_no', 'school', 'cohort', 'street', 'city', 'state', 'zipcode', 'timeframe'],
    'possible_relatives': ['input_file', 'filter_cohort', 'filter_school', 'search_number', 'commencement_name', 'student_no', 'school', 'cohort', 'relative_name', 'relative_age', 'relative_birthyear', 'relative_link', 'relative_id'],
    'relative_summary': ['input_file', 'filter_cohort', 'filter_school', 'search_number', 'commencement_name', 'student_no', 'school', 'cohort', 'relative_id', 'relative_searchnumber', 'relative_fullname_fromsearch', 'relative_brithyear_fromsearch', 'relative_age_fromsearch', 'relative_associatedname_fromsearch'],
    'relative_address': ['input_file', 'filter_cohort', 'filter_school', 'search_number', 'commencement_name', 'student_no', 'school', 'cohort', 'relative_id', 'relative_searchnumber', 'relative_street', 'relative_city', 'relative_state', 'relative_zipcode', 'relative_timeframe']
}

SUMMARY_FIELD_MAPPING = {
   'Full Name': 'fullname',
   'Birth Year': 'birthyear',
   'Age': 'age'
}

RELATIVE_SUMMARY_FIELD_MAPPING = {
   'Full Name': 'relative_fullname_fromsearch',
   'Birth Year': 'relative_brithyear_fromsearch',
   'Age': 'relative_age_fromsearch'
}

ADDRESS_HEADING = 'Current & Past Addresses'
POSSIBLE_RELATIVES_HEADING = 'Possible Relatives'
ASSOCIATED_NAMES_HEADING = 'Associated Names'

US_STATE_ABBREV = {
   'Alabama': 'AL',
   'Alaska': 'AK',
   'Arizona': 'AZ',
   'Arkansas': 'AR',
   'California': 'CA',
   'Colorado': 'CO',
   'Connecticut': 'CT',
   'Delaware': 'DE',
   'Florida': 'FL',
   'Georgia': 'GA',
   'Hawaii': 'HI',
   'Idaho': 'ID',
   'Illinois': 'IL',
   'Indiana': 'IN',
   'Iowa': 'IA',
   'Kansas': 'KS',
   'Kentucky': 'KY',
   'Louisiana': 'LA',
   'Maine': 'ME',
   'Maryland': 'MD',
   'Massachusetts': 'MA',
   'Michigan': 'MI',
   'Minnesota': 'MN',
   'Mississippi': 'MS',
   'Missouri': 'MO',
   'Montana': 'MT',
   'Nebraska': 'NE',
   'Nevada': 'NV',
   'New Hampshire': 'NH',
   'New Jersey': 'NJ',
   'New Mexico': 'NM',
   'New York': 'NY',
   'North Carolina': 'NC',
   'North Dakota': 'ND',
   'Ohio': 'OH',
   'Oklahoma': 'OK',
   'Oregon': 'OR',
   'Pennsylvania': 'PA',
   'Rhode Island': 'RI',
   'South Carolina': 'SC',
   'South Dakota': 'SD',
   'Tennessee': 'TN',
   'Texas': 'TX',
   'Utah': 'UT',
   'Vermont': 'VT',
   'Virginia': 'VA',
   'Washington': 'WA',
   'West Virginia': 'WV',
   'Wisconsin': 'WI',
   'Wyoming': 'WY',
   'Alberta': 'AB',
   'British Columbia': 'BC',
   'Manitoba': 'MB',
   'New Brunswick': 'NB',
   'Newfoundland and Labrador': 'NL',
   'Nova Scotia': 'NS',
   'Northwest Territories': 'NT',
   'Nunavut': 'NU',
   'Ontario': 'ON',
   'Prince Edward Island': 'PE',
   'Quebec': 'QC',
   'Saskatchewan': 'SK',
   'Yukon': 'YT'
}