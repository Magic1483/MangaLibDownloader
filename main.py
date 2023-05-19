import json
import os


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import requests

def save_img(link,name,folder):
    img_data = requests.get(link).content
    with open(f'{folder}/{name}.png', 'wb') as handler:
        handler.write(img_data)
  
  
def SaveElementScreenShoot(element,name,folder):
    element.screenshot(f'{folder}/{name}.png')

def get_first_num(t):
    tmp = t.split(' ')
    for i in tmp:
        if i.isnumeric():
            return (int(i))
            break

def LoadCookieJSON(driver,cookie_file):
    # Load JSON Cookie
    with open(cookie_file) as f:
        cookie_dict = json.load(f)

    time.sleep(5)
    #set cookie from file
    driver.delete_all_cookies()
    for i in cookie_dict:
        del i['sameSite']
        driver.add_cookie(i)

    driver.refresh()

#mangalib downloader
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument('--beg',default='non',help='the begin volume')
    parser.add_argument('--end',default='non',help='the end volume')
    parser.add_argument('--cookie',default='non',help='user cookie auth')
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
    wait = WebDriverWait(browser, 10)

    browser.get(url)
    if args.cookie!='non':
        LoadCookieJSON(driver=browser,cookie_file=args.cookie)

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    #print(browser.find_element(By.TAG_NAME,'body').text)



    name = browser.find_element(By.XPATH,'//div[@class="media-name__main"]')
    print(name.text)
    name = name.text.replace(':','')
    name = name.replace('.', '')
    name = name.replace(',', '')
    

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
        print(f'from {args.beg} to {args.end} volumes')
    else:
        print('Full volume mode')

    #test output
    # for i in v:
    #     print(f'{i[1]} {i[0]}')





    def downloader(link,cname):

        actions = ActionChains(browser)

        # если есть несколько переводов
        if 'bid' in link:
            tmp = f'{link}&page=1'
        else:
            tmp = f'{link}?page=1'
        print(tmp)
        browser.get(tmp)

        pages = browser.find_elements(By.XPATH,'//div[@data-p]')
        # page_count = int(pages[-1].get_attribute('data-p'))
        page_count = len(pages)
        print(f'{len(pages)} pages')

        cname=cname.replace('.',' ')
        cname = cname.replace(':', '')
        cname = cname.replace('?', '')
        cname = cname.replace('-', ' ')

        

        if not os.path.exists(f'{name}/{cname}'):
            os.mkdir(f'{name}/{cname}')


        for i in range(1,page_count+1):
            #если есть несколько переводов
            if 'bid' in link:
                url = f'{link}&page={i}'
                print(url)
            else:
                url = f'{link}?page={i}'
                print(url)


            # browser.get(url)
            
            wait.until(EC.visibility_of_element_located((By.XPATH,f'//div[@data-p="{i}"]')))
            
            
            element = browser.find_element(By.XPATH, f'//div[@data-p="{i}"]')
            
            img = element.find_element(By.TAG_NAME, 'img')

            if 'hentailib' in url:
                #close warn button 
                try:
                    browser.find_element(By.XPATH,'//div[@class="toast-item__close"]').click()
                except: pass
                time.sleep(1)
                SaveElementScreenShoot(img,i,f'{name}/{cname}')
            else:

                save_img(img.get_attribute('src'),i,f'{name}/{cname}')

            actions.send_keys(Keys.ARROW_RIGHT).perform()

        print(f'chapter {cname} the end')

    count=1
    for i in v:
        downloader(i[0],i[1])
        print(f'{count}/{len(v)} volumes')
        count+=1
        time.sleep(4)




if __name__ == '__main__':
    main()




