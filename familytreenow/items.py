# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SummaryItem(scrapy.Item):
    input_file = scrapy.Field()
    filter_cohort = scrapy.Field()
    filter_school = scrapy.Field()
    search_number = scrapy.Field()
    commencement_name = scrapy.Field()
    student_no = scrapy.Field()
    school = scrapy.Field()
    cohort = scrapy.Field()
    fullname = scrapy.Field()
    birthyear = scrapy.Field()
    age = scrapy.Field()
    associated_names = scrapy.Field()
    item_type = scrapy.Field()
    pass

class AddressItem(scrapy.Item):
    input_file = scrapy.Field()
    filter_cohort = scrapy.Field()
    filter_school = scrapy.Field()
    search_number = scrapy.Field()
    commencement_name = scrapy.Field()
    student_no = scrapy.Field()
    school = scrapy.Field()
    cohort = scrapy.Field()
    street = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()
    timeframe = scrapy.Field()
    item_type = scrapy.Field()
    pass

class PossibleRelativeItem(scrapy.Item):
    input_file = scrapy.Field()
    filter_cohort = scrapy.Field()
    filter_school = scrapy.Field()
    search_number = scrapy.Field()
    commencement_name = scrapy.Field()
    student_no = scrapy.Field()
    school = scrapy.Field()
    cohort = scrapy.Field()
    relative_name = scrapy.Field()
    relative_age = scrapy.Field()
    relative_birthyear = scrapy.Field()
    relative_link = scrapy.Field()
    relative_id = scrapy.Field()
    item_type = scrapy.Field()
    pass

class RelativeSummaryItem(scrapy.Item):
    input_file = scrapy.Field()
    filter_cohort = scrapy.Field()
    filter_school = scrapy.Field()
    search_number = scrapy.Field()
    commencement_name = scrapy.Field()
    student_no = scrapy.Field()
    school = scrapy.Field()
    cohort = scrapy.Field()
    relative_id = scrapy.Field()
    relative_searchnumber = scrapy.Field()
    relative_fullname_fromsearch = scrapy.Field()
    relative_brithyear_fromsearch = scrapy.Field()
    relative_age_fromsearch = scrapy.Field()
    relative_associatedname_fromsearch = scrapy.Field()
    item_type = scrapy.Field()
    pass

class RelativeAddressItem(scrapy.Item):
    input_file = scrapy.Field()
    filter_cohort = scrapy.Field()
    filter_school = scrapy.Field()
    search_number = scrapy.Field()
    commencement_name = scrapy.Field()
    student_no = scrapy.Field()
    school = scrapy.Field()
    cohort = scrapy.Field()
    relative_id = scrapy.Field()
    relative_searchnumber = scrapy.Field()
    relative_street = scrapy.Field()
    relative_city = scrapy.Field()
    relative_state = scrapy.Field()
    relative_zipcode = scrapy.Field()
    relative_timeframe = scrapy.Field()
    item_type = scrapy.Field()
    pass
