import time
import os

DELAY=3.0
FILEPATH = 'test.txt'
SOURCE = 'ko'
TARGET = 'en'


URL = 'https://translate.google.com/'
EXPECTED_CONDITIONS = ('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea', # 텍스트 입력 창
                       # 텍스트입력 결과
                       )

OUTPUT_XPATH = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[7]/div/div[1]/span[1]/span/span'
# 이전 버전     //*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[8]/div/div[1]/span[1]/span/span
LANG_CODE = {
    'auto':'auto',
    'ko':'ko',
    'en':'en',
    'jp':'ja',
    'cn':'zh-CN',
    'tc':'zh-TW',
    'fr':'fr',
    'vi':'vi',
    'ru':'ru',
    'sv':'sv',
    'es':'es',
    'ar':'ar',
    'it':'it'
}

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
# from bs4 import BeautifulSoup as bs
# import requests
from webdriver_manager.chrome import ChromeDriverManager

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'

def getdriver(url, headless, **kwargs):
    
    # if 'required_UA' in kwargs.keys():
    #     if kwargs['required_UA']:
    #         opts=Options()
    #         opts.add_argument(f"user-agent={USER_AGENT}")
    #         driver=webdriver.Chrome(chrome_options=opts)
    # else:
    if headless:
        options = ChromeOptions()
        
        # page = requests.get('http://whatsmyuseragent.org/')
        # soup = bs(page.text, 'lxml')
        # print(soup.p.text)
        options.add_argument('--window-size=945,1020')
        #options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
        options.add_argument('--headless')
        
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--start-full-screen')
        
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    else:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    print(driver.get_window_size())
    driver.get(url)
    return driver

def waits_page(driver, *args):
    global loaded_page
    for a in args:
        loaded_page = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, a))
        )
        print(f'{a} done!')
        
def rm_em(s):
    return ''.join(c for c in s if c <= '\uFFFF')

def close_driver(driver):
    i = input("사용이 끝나셨다면 아무키나 입력해주세요.")
    if i:
        driver.quit()

def print_result(i, e, output):
    print('''====================================================\n'''
            'linenumber:',i+1,'''\n====================================================\n''',
            e + '\n', output)



def init_page(inlang, outlang, headless):
    global driver
    curpage = f'{URL}?sl={LANG_CODE[inlang]}&tl={LANG_CODE[outlang]}&op=translate'
    print(curpage)
    driver = getdriver(curpage, headless)
    waits_page(driver, *EXPECTED_CONDITIONS)
    
    global inputarea
    
    inputarea = driver.find_element(By.XPATH, EXPECTED_CONDITIONS[0])

def put_input(input):
    global driver
    global inputarea
    global outputarea
    
    time.sleep(DELAY)
    inputarea.send_keys(input)
    time.sleep(DELAY)
    # try:    
    return driver.find_element(By.XPATH, OUTPUT_XPATH).text
    # except:
    #     print("문제발생...")


def excecuteTranslation(infile, outfile, inlang, outlang, headless=True):
    global driver
    global inputarea
    with open(infile, 'r', encoding='utf-8-sig') as in_file:
        lst = in_file.read().split('\n')
    out_file = open(outfile, 'w', encoding='utf-8-sig')
    init_page(inlang, outlang, headless)
    for i,e in enumerate(lst):
        output = put_input(rm_em(e))
        print('linenumber:',i+1, output)
        out_file.write(output+'\n')
        inputarea.clear()
    
    out_file.close()
    print('done')
    close_driver(driver)



if __name__ == "__main__":
    abspath = os.path.abspath(FILEPATH)
    path = os.path.dirname(abspath)
    name = '.'.join(os.path.basename(abspath).split('.')[:-1])
    excecuteTranslation(abspath, f"{path}/{name}_{SOURCE}-{TARGET}.txt", SOURCE, TARGET, False)