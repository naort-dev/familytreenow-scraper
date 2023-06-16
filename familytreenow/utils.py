import requests
import urllib3
import time
from familytreenow.settings import INPUT_COLUMN, SEARCH_PARAM, US_STATE_ABBREV, CAPTCHA_KEY, BASE_FIELDS_FROM_INPUT, SCRAPER_API

# urllib3.disable_warnings() # This is not good practice. Do we need it? https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
})

BASE_URL = 'https://2captcha.com/'


def get_recaptcha_answer(site_key, pageurl):
    try:
        captcha_id = session.post('{}in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}'.format(
            BASE_URL, CAPTCHA_KEY, site_key, pageurl)).text.replace('OK|', '')
    except requests.ConnectionError as e:
        print("Connection failure : " + str(e))
        print("Verification with InsightFinder credentials Failed")
    print(captcha_id)

    # get captcha_answer with captcha_id and captcha_key
    try:
        recaptcha_answer = session.get('{}res.php?key={}&action=get&id={}'.format(
            BASE_URL, CAPTCHA_KEY, captcha_id)).text
    except requests.ConnectionError as e:
        print("Connection failure : " + str(e))
        print("Verification with InsightFinder credentials Failed")
    print(recaptcha_answer)

    # try to get captcha_answer repeatedly until it's ready
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        print (recaptcha_answer)
        seconds_to_sleep = 10
        time.sleep(seconds_to_sleep)
        try:
            recaptcha_answer = session.get('{}res.php?key={}&action=get&id={}'.format(
                BASE_URL, CAPTCHA_KEY, captcha_id)).text
        except requests.ConnectionError as e:
            print("Connection failure : " + str(e))
            print("Verification with InsightFinder credentials Failed")

    if recaptcha_answer == 'ERROR_CAPTCHA_UNSOLVABLE':
        return get_recaptcha_answer(site_key, pageurl)
    recaptcha_answer = recaptcha_answer.replace('OK|', '')
    return recaptcha_answer


def parse_input_row(row):
    input_data = {}
    for index, column in enumerate(INPUT_COLUMN):
        # print(INPUT_COLUMN[index], index)
        input_data[column] = row[index].strip()
    return input_data


def generate_search_param(input):
    query = ''
    location = ''
    if len(input['city']) > 0 and len(input['state']) > 0:
        location = '{}, {}'.format(input['city'], US_STATE_ABBREV[input['state']])
    input['location'] = location
    input_column = INPUT_COLUMN.copy()
    input_column.append('location')
    for index, item in enumerate(input_column):
        if input[item] != '' and input_column[index] in SEARCH_PARAM:
            query = query + '{}={}&'.format(SEARCH_PARAM[input_column[index]], input[item])
    if len(query) > 0:
        query = query[:-1]
    return query


def get_base_fields_from_input(input_data):
    base_data = {}
    for item in BASE_FIELDS_FROM_INPUT:
        # print(INPUT_COLUMN[index], index)
        if item in input_data:
            base_data[item] = input_data[item]
    return base_data


def parse_address(address_text):
    splitted_address = address_text.split(', ')
    splitted_address_len = len(splitted_address)
    address = {'street': '', 'city': '', 'state': '', 'zipcode': ''}
    if splitted_address_len >= 1:
        address['street'] = splitted_address[0].strip()
    if splitted_address_len >= 2:
        address['city'] = splitted_address[1].strip()
    if splitted_address_len >= 3:
        state_zipcode_string = splitted_address[2].strip().split(' ')
        state_zipcode_string_len = len(state_zipcode_string)
        if state_zipcode_string_len >= 1:
            address['state'] = state_zipcode_string[0]
        if state_zipcode_string_len >= 2:
            address['zipcode'] = state_zipcode_string[1]
    return address


def check_is_relative(data):
    if 'relative_id' in data:
        return True
    else:
        return False

