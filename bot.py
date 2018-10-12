import json
import random
import requests
import tweepy
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
"""
auth = tweepy.OAuthHandler('', '')
auth.set_access_token('', '')
api = tweepy.API(auth)
"""

trove_api = ""
search = "VFL"
main_api = "http://api.trove.nla.gov.au/result?q="+search+"&zone=picture&n=1&key="+trove_api+"&encoding=json"
failed = True
while failed == True :
    random_post = main_api + "&s=" + str(random.randint(1,819))
    print(random_post)
    post = requests.get(random_post).json()
    try:
        print (post['response']['zone'][0]['records']['work'][0]['title'])
        print (post['response']['zone'][0]['records']['work'][0]['identifier'][1]['value'])


        def tweet_image(url, message, imageurl):
            print("\n \n image url"+imageurl)
        
            if "http://handle.slv.vic.gov.au" in imageurl:
                driver = webdriver.Chrome()
                driver.get(imageurl)
                time.sleep(5)
                frame = driver.find_element(By.XPATH, '//*[@id="VIEW_SET"]/frame[2]')
                driver.switch_to.frame(frame)
                #//*[@id="VIEW_SET"]/frame[2]
                frame = driver.find_element(By.XPATH, '/html/frameset/frame[2]')
                driver.switch_to.frame(frame)
                #/html/frameset/frame[2]
                frame = driver.find_element(By.XPATH, '/html/frameset/frame[3]')
                driver.switch_to.frame(frame)
                #/html/frameset/frame[3]
                frame = driver.find_element(By.XPATH, '//*[@id="JPEGNAV_MAIN_FRAME"]')
                driver.switch_to.frame(frame)
                img = driver.find_element(By.XPATH, '//*[@id="OuterDiv"]/img')
                url = img.get_attribute('src')
                driver.quit()
            
            if "recordsearch.naa.gov.au" in imageurl:
                driver = webdriver.Chrome()
                driver.get(imageurl)
                img = driver.find_element(By.XPATH,'//*[@id="ContentPlaceHolderSNR_imageCell"]/a/img')
                url = img.get_attribute('src')
                driver.quit()
                
            filename = 'temp.jpg'
            request = requests.get(url, stream=True)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)

                api.update_with_media(filename, status=message)
                os.remove(filename)
            else:
                print("Unable to download image")
        tweet_image(post['response']['zone'][0]['records']['work'][0]['identifier'][1]['value'], post['response']['zone'][0]['records']['work'][0]['title'] +"\n" + post['response']['zone'][0]['records']['work'][0]['identifier'][0]['value'], post['response']['zone'][0]['records']['work'][0]['identifier'][0]['value'])
        failed = False
    except:
        print("failed");
