from flask import Flask, render_template, request, url_for
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import urllib.request
import time
import emoji
#import csv
import requests
import os
from bs4 import BeautifulSoup

#There Is No Need To LogIn It Can Access Data Behind The LogIn PopUp
def Pinterest( Query, Number_Of_Pins, Type ):

    for letter in Query:
        if letter==' ':
            letter = '%20'

    if 'https://www.pinterest.com/' in Query:
        Target_Link = Query
    else:
        if Type=='image':
            Target_Link = 'https://www.pinterest.com/search/pins/?q='+Query+'&rs=typed'
        else:
            Target_Link = 'https://www.pinterest.com/search/videos/?q='+Query+'&rs=filter'
                
            
        

    #print(Target_Link)

    #chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")   
    #chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    driver=webdriver.Chrome()#chrome_options=chrome_options
    #executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options
    
    driver.get(Target_Link)

    #print('Pins: ' + str(Number_Of_Pins))

    Scroll(driver, Type, Number_Of_Pins)

    DATA = Find_Pins_Data(driver, Type)

    Row_Data = []
    for row in range(Number_Of_Pins):
        Row_Data.append([DATA[0][row], DATA[1][row], DATA[2][row], DATA[3][row]])
        print(Row_Data[row])
   
    print('line')

    print(Row_Data)
    return Row_Data


#checking if the Title is Present For The Pin
def Title_exists(tag):
    try:
        element=driver.find_element_by_tag_name(tag)
    except NoSuchElementException:
        return 'No Title'
    return element.text

#checking if the description element is present and return desrciption(here the element is a css selector)
def Description_exists(css_selector):
    try:
        element=driver.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return 'No Description'
    return element.text

#scrolling feed until Number Of Required Pins Aren't Loaded
def Scroll(driver, Type, Number_Of_Pins):

    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

    if Type=='image':
        
        video_posts = driver.find_elements_by_css_selector('[data-test-id="PinTypeIdentifier"]')
        img_posts = driver.find_elements_by_tag_name('img')

        while (len(img_posts) - len(video_posts) <= Number_Of_Pins):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            img_posts = driver.find_elements_by_tag_name('img')
            video_posts = driver.find_elements_by_css_selector('[data-test-id="PinTypeIdentifier"]')

    else:
        video_post_elements = driver.find_elements_by_css_selector('[data-test-id="PinTypeIdentifier"]')

        while (len(video_post_elements) <= Number_Of_Pins):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

            video_post_elements = driver.find_elements_by_css_selector('[data-test-id="PinTypeIdentifier"]')

def Find_Pins_Data(driver, Type):

    All_Pin_Divs = driver.find_elements_by_class_name('Collection-Item')

    video_pin_link = ''
    video_download_link = ''
    Video_Download_Links = []
    Video_Pin_Links = []
    image_download_link = ''
    image_pin_link = ''
    Image_Download_Links = []
    Image_Pin_Links = []

    Titles = []
    Descriptions = []
    Description = ''
    Title =''

    Video_Thumbnail_Links =[]

    if Type=='image':

        for div in All_Pin_Divs:

            if div.find_elements_by_css_selector('[data-test-id="PinTypeIdentifier"]')==[]:

                img_tag = div.find_element_by_tag_name('img')

                image_pin_link = div.find_element_by_tag_name('a').get_attribute('href')
                print(image_pin_link)
                print('')

                Title = div.find_elements_by_tag_name('h3')
                if Title!=[]:
                    Title= Title[0].text
                else:
                    Title='no title'

                print(Title)
                print('')       
                Description = img_tag.get_attribute('alt')
                print(Description)
                print('')
                download_link = img_tag.get_attribute('srcset').split()[2]
                print(download_link)
                print('')

                Image_Pin_Links.append(image_pin_link)
                Image_Download_Links.append(download_link)
                Titles.append(Title)
                Descriptions.append(Description)

            else:
                continue
            
    else:

        for div in All_Pin_Divs:

            img_tag = div.find_element_by_tag_name('img')

            video_pin_link = div.find_element_by_tag_name('a').get_attribute('href')
            print(video_pin_link)
            print('')


            Title = div.find_elements_by_tag_name('h3')
            if Title!=[]:
                Title= Title[0].text
            else:
                Title='no title'

            print(Title)
            print('')
            Description = img_tag.get_attribute('alt')
            print(Description)
            print('')

            video_thumbnail_link = img_tag.get_attribute('srcset').split()[2]#will use this link for showing video thumbnails on our website coz download links rely on other source and gives request error often
            print(video_thumbnail_link)
            print('')

            Video_Pin_Links.append(video_pin_link)
            Titles.append(Title)
            Descriptions.append(Description)
            Video_Thumbnail_Links.append(video_thumbnail_link)
    
    for link in Video_Pin_Links:
    
        download_link = requests.get("https://pinterest-video-api.herokuapp.com/" + link).text
        download_link = download_link[1:len(download_link)-1]
        print(download_link)
        print('')

        Video_Download_Links.append(video_download_link)



    driver.close()


     

        # if pin.find_elements_by_css_selector('[data-test-id="PinTypeIdentifier"]'):

        #     video_pin_link = pin.find_element_by_tag_name('a').get_attribute('href')

        #     # this is a herokuapp api for pinterest video pin download link just make a request to it and retrieve file
        #     video_download_link = requests.get("https://pinterest-video-api.herokuapp.com/" + video_pin_link).text
        #     video_download_link=video_download_link[1:len(video_download_link)-1]

        #     Video_Pin_Links.append(video_pin_link)
        #     Video_Download_Links.append(video_download_link)
            

        # else:
        #     image_pin_link = pin.find_element_by_tag_name('a').get_attribute('href')
        #     image_download_link = pin.find_element_by_tag_name('img').get_attribute('srcset').split()[2]

        #     Image_Pin_Links.append(image_pin_link)
        #     Image_Download_Links.append(image_download_link)

    

    if Type == 'image':
        print('Image Pins')
        print('')
        print(len(Image_Pin_Links))
        print('')
        print(Image_Pin_Links)
        print('')
        print(len(Image_Download_Links))
        print('')
        print(Image_Download_Links)
        print('')

        print(len(Titles))
        print('')
        print(Titles)
        print('')
        print(len(Descriptions))
        print('')
        print(Descriptions)
        print('')

    if Type == 'video':
        print('Video Pins')
        print('')
        print(len(Video_Pin_Links))
        print('')
        print(Video_Pin_Links)
        print('')
        print(len(Video_Download_Links))
        print('')
        print(Video_Download_Links)
        print('')

        print(len(Titles))
        print('')
        print(Titles)
        print('')
        print(len(Descriptions))
        print('')
        print(Descriptions)
        print('')

        print(len(Video_Thumbnail_Links))
        print('')
        print(Video_Thumbnail_Links)

    if Type=='image':
        return Image_Pin_Links, Image_Download_Links, Titles, Descriptions


    if Type =='video':
        return Video_Pin_Links, Video_Download_Links, Titles, Descriptions




# def Find_Title_And_Description(Links, Number_Of_Pins):

#     Titles = []
#     Descriptions = []
#     Description = ''
#     Title =''
#     extracted = 0

#     for link in range(Number_Of_Pins):

#         print(Links[link])
#         content = requests.get(Links[link])
#         soup = BeautifulSoup(content.text, "lxml")
#         Description = ''
#         try:
#             Title = soup.find('meta', property="og:title").get('content')
#             Titles.append(Title)
#             print(Title)

#         except:
#             print(soup.find('meta', property="og:title"))
#             Title = 'No Title'
#             Titles.append(Title)

#         try:
#             descriptionall = soup.find('meta', property="og:description").get('content').split()[4:]
#             print(descriptionall)

#             for word in descriptionall:
#                 Description = Description + word + ' '

#             Descriptions.append(Description)

#             print(Description)

#         except:
#             print(soup.find('meta', property="og:description"))
#             Description = 'No Description'
#             Descriptions.append(Description)

#         extracted += 1
#         print('extracted: ' + str(extracted))

#         #print(Description)
#         #time.sleep(0.1)

#     print(len(Titles))
#     print(Titles)

#     print(len(Descriptions))
#     print(Descriptions)

#     return Titles, Descriptions

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'] )
def hello_world():
    if request.method=='POST':
        searched = str(request.form['searched'])
        numberofpins = int(request.form['numberofpins'])
        typeofpin = str(request.form['type'])

        data = Pinterest(searched, numberofpins, typeofpin)

        return render_template('index.html', data=data, typeofpin=typeofpin )

    else:
        searched=''
        print('something is wrong')
        return render_template('index.html', searched=searched)

    

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/how-to-use')
def how():
    return render_template('how-to-use.html')

if __name__=="__main__":
    app.run(debug=True)