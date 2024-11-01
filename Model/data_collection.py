from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import urllib.request
import time
import os

options=webdriver.ChromeOptions()
options.add_argument('--user-data-dir=C:\\Users\\Hp\\AppData\\Local\\Google\\Chrome for Testing\\User Data\\Default')
options.add_argument('--headless')
driver=uc.Chrome(options=options)

max_images=300
products=[
'drug powder',
'drug pills',
'drug liquid',
'cannabis drug',
'methenamine drug',
'drug crystals',
'khat drug',
'lsd drug',
'opium',
'steroid drug',
'benzodiazepines drug',
'methadone drug',
'morphine drug',
'marijuna drug',
'spice/K2 drug',
'u-47700 drug',
'weed smoking',
'heroine drug'
]

folder_path=r"D:\Codeutsav\Drugs"

for prod in products:
    dir=os.path.join(folder_path,prod)
    os.makedirs(dir,exist_ok=True)
    prod=prod.split()
    if len(prod)==1:
        url='https://www.google.com/search?sca_esv=c1df660eec58a1d6&sxsrf=ADLYWIJ93VSWNdMzqM6nGK8e19BEKYsRCA:1719418976768&q={}&udm=2&fbs=AEQNm0B8dVdIWR07uWWlg1TdKnNtA1cwMugrQsIKmAo5AEZHWRFlUeGLxYlhagMfUatSvHu3MSamP9Qd2SfjyZyVIdPFrZFmdorP0BQX-5QUvERZ7CgntLysKxPYR85LNkkQ-ODVQlzCBgHDwYGwBEtb1wyzIiqYOAGOFOhRLG73H-MUdJY1ZFjTgiSsk2gQgTHDHU_Mnn5ewYy4nGfZAENFgsXyYdMtYQ&sa=X&ved=2ahUKEwjT8tHq1vmGAxVqklYBHS0zCOIQtKgLegQIDhAB&biw=1280&bih=551&dpr=1.5'.format(prod[0])
    else:
        url='https://www.google.com/search?sca_esv=93393d72ee4371e2&sxsrf=ADLYWILdo6xEE7ASEJfNutn1Qou1SW9D6g:1719479283200&q={0}+{1}&udm=2&fbs=AEQNm0B8dVdIWR07uWWlg1TdKnNtA1cwMugrQsIKmAo5AEZHWRFlUeGLxYlhagMfUatSvHu3MSamP9Qd2SfjyZyVIdPFrZFmdorP0BQX-5QUvERZ7CgntLysKxPYR85LNkkQ-ODVQlzCBgHDwYGwBEtb1wyzIiqYOAGOFOhRLG73H-MUdJY1ZFjTgiSsk2gQgTHDHU_Mnn5ewYy4nGfZAENFgsXyYdMtYQ&sa=X&ved=2ahUKEwiJr_6-t_uGAxUZ2DgGHe74B_0QtKgLegQIERAB&biw=1280&bih=551&dpr=1.5'.format(prod[0],prod[1])

    driver.get(url)
    time.sleep(10)

    if max_images%100==0:
        count_loop=int(max_images/100)+2
    else:
        count_loop = int(max_images/100)+2

    for _ in range(count_loop):
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(10)

    img_results = driver.find_elements(By.XPATH,'//img[contains(@class,"YQ4gaf") and not(ancestor::div[contains(@class,"PHj8of")]) and not(contains(@class,"zr758c"))]')
    time.sleep(10)



    img_urls=[]
    for img in img_results:
        img_urls.append(img.get_attribute('src'))

    if len(img_urls)>max_images:
        c=max_images
    else:
        c=len(img_urls)

    for i in range(c):
        urllib.request.urlretrieve(str(img_urls[i]),os.path.join(dir,"{}.jpg".format(i)))

driver.quit()