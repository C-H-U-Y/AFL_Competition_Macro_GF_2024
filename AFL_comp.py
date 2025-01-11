from selenium import webdriver
from selenium.webdriver.edge.service import Service
import time
import traceback
from selenium.webdriver.common.by import By 
import cv2
import urllib
import numpy as np


# Specify the path to your local Edge WebDriver (msedgedriver)
driver_path = "./msedgedriver.exe"

# Set up the Service with the path to Edge WebDriver
service = Service(driver_path)

# Initialize the Edge WebDriver using the Service object
driver = webdriver.Edge(service=service)


identity_carousel = [
    # Redacted
]

try:
    games_played = 0
    person_iter = 0

    while(True):
        # Open a webpage
        driver.get("https://comps.afl.com.au/tb_app/509807")

        time.sleep(3)
        
        if(games_played == 0):
        
            buttons = driver.find_elements(By.XPATH, '//button[@type="button"]')

            # accept cookies
            buttons[1].click()

            time.sleep(1)

        page_buttons = driver.find_elements(By.XPATH, '//button[@class="campaign-btn campaign-btn-primary"]')
        
        # start game
        page_buttons[0].click()

        time.sleep(3)

        # Get the image URLS
        cards = driver.find_elements(By.XPATH, '//div[@class="card-back"]')
        clickable_cards = driver.find_elements(By.XPATH, '//div[@class="card active"]') 

        # there are 12 cards
        # print(len(cards))

        images = []

        matches = []

        j = 0
        for card, clickable_card in zip(cards, clickable_cards):
            j += 1
            img_url = card.get_attribute('style').split("\"")[1]

            req = urllib.request.urlopen(img_url)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1) # 'Load it as it is'

            images.append(img)

            cv2.imshow('player photo {}'.format(j), img)
            cv2.waitKey(1)

            if(len(images) == 1):
                continue
            
            for i in range(0, len(images)-1):
                potential_match_image = images[i]

                if(potential_match_image.shape == img.shape and not(np.bitwise_xor(potential_match_image[150:161, :],img[150:161, :]).any())):
                    matches.append((clickable_card, clickable_cards[i]))
                    break
        
        cv2.destroyAllWindows()

        for match in matches:
            match[0].click()
            time.sleep(0.5)
            match[1].click()
            time.sleep(2)
        
        personal_data = identity_carousel[person_iter]

        # Fill in the success form
        inputs = driver.find_elements(By.XPATH, '//input') 

        for input in inputs:
            if(games_played == 0):
                if(input.get_attribute('name') == 'legal_agree'):
                    legal_agree_input = input
                    legal_agree_input.click()
                
            if(input.get_attribute('name') == 'first_name'):
                fname_input = input
                fname_input.clear()
                fname_input.send_keys(personal_data[0])
                
            elif(input.get_attribute('name') == 'last_name'):
                lname_input = input
                lname_input.clear()
                lname_input.send_keys(personal_data[1])
            
            elif(input.get_attribute('name') == 'email'):
                email_input = input
                email_input.clear()
                email_input.send_keys(personal_data[2])
            
            elif(input.get_attribute('name') == 'age_day'):
                age_day_input = input
                age_day_input.send_keys(personal_data[3])

            elif(input.get_attribute('name') == 'age_month'):
                age_month_input = input
                age_month_input.send_keys(personal_data[4])

            elif(input.get_attribute('name') == 'age_year'):
                age_year_input = input
                age_year_input.send_keys(personal_data[5])
                
            elif(input.get_attribute('name') == 'postal_code'):
                postal_code_input = input
                postal_code_input.send_keys(personal_data[7])
            
            elif(input.get_attribute('name') == 'city'):
                city_input = input
                city_input.send_keys(personal_data[6])

            elif(input.get_attribute('name') == 'is_subscribed'):
                is_subscribed_input = input
                is_subscribed_input.click()

        #select club
        club_select = driver.find_element(By.XPATH, '//select[@id="field_what_club_do_you_support"]') 
        club_select.click()
        swans_select = driver.find_element(By.XPATH, '//option[@value="Sydney Swans"]') 
        swans_select.click()
        # club_select = driver.find_element(By.XPATH, '//select[@id="field_what_club_do_you_support"]') 
        club_select.click()

        time.sleep(1)

        # submit form
        submit_button = driver.find_elements(By.XPATH, '//button[@class="campaign-btn campaign-btn-primary"]') 

        print(len(submit_button))
        submit_button[-1].click()

        time.sleep(5)

        games_played += 1
        person_iter += 1

        if(person_iter >= len(identity_carousel)):
            person_iter = 0

        print("PLAYED {} GAMES".format(games_played))

        # if(games_played + 25 >= 18 * len(identity_carousel)):
        #     break

    # Close the browser
    driver.quit()

except Exception as e:
    print(traceback.format_exc())
    driver.quit()
