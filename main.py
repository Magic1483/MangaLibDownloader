import json
import os


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests

def save_img(link,name,folder):
  img_data = requests.get(link).content
  with open(f'{folder}/{name}.jpg', 'wb') as handler:
      handler.write(img_data)

def get_first_num(t):
    tmp = t.split(' ')
    for i in tmp:
        if i.isnumeric():
            return (int(i))
            break


#mangalib downloader
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument('--beg',default='non',help='the begin volume')
    parser.add_argument('--end',default='non',help='the end volume')
    args = parser.parse_args()
    url = args.url

    Options = webdriver.ChromeOptions()
    #Options.add_argument('--headless')
    Options.add_argument('--no-sandbox')
    #url = 'https://mangalib.me/tokyo-revangers?section=chapters'

    #path to chrome driver
    #You need driver for your Google Chrome version
    DRIVER_PATH = 'chromedriver.exe'

    browser = webdriver.Chrome(DRIVER_PATH,options=Options)

    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    #print(browser.find_element(By.TAG_NAME,'body').text)



    name = browser.find_element(By.XPATH,'//div[@class="media-name__main"]')
    print(name.text)
    name = name.text.replace(':','')
    name = name.replace('.', '')

    #Create book folder
    if not os.path.exists(name):
        os.mkdir(name)
    else:
        print('folder is exist')

    volums = browser.find_elements(By.XPATH,'//div[@class="media-chapter__name text-truncate"]//a')
    v=[]
    for i in volums:
        v.append([i.get_attribute('href'),i.text])

    v_custom = []
    if args.beg!='non' and args.end!='non':
        for i in v:
            if get_first_num(i[1])<=int(args.end) and get_first_num(i[1])>=int(args.beg):
                v_custom.append(i)
        v = v_custom
    else:
        print('Full volume mode')





    def downloader(link,cname):
        browser.get(link)
        pages = browser.find_elements(By.XPATH,'//div[@data-p]')
        # page_count = int(pages[-1].get_attribute('data-p'))
        page_count = len(pages)
        print(len(pages))

        cname=cname.replace('.','')
        cname = cname.replace(':', '')

        os.mkdir(f'{name}/{cname}')


        for i in range(1,page_count+1):
            url = f'{link}?page={i}'
            print(url)
            browser.get(url)
            element = browser.find_element(By.XPATH, f'//div[@data-p="{i}"]')
            #
            img = element.find_element(By.TAG_NAME, 'img').get_attribute('src')
            save_img(img,i,f'{name}/{cname}')

        print(f'chapter {cname} the end')

    count=1
    for i in v:
        downloader(i[0],i[1])
        print(f'{count}/{len(v)}')
        count+=1
        time.sleep(4)




if __name__ == '__main__':
    main()


