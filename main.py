from selenium import webdriver
from selenium.webdriver.common.by import By
import glob
import os
import time
import mysql.connector
import cv2
import random
import datetime
from pynput.keyboard import Key, Controller



#Loading Home Page

driver=webdriver.Chrome()
driver.maximize_window()
driver.get("https://quora.com")
print(os.environ['host'])
print(os.environ['dbpass'])
print(os.environ['database'])
print(os.environ['username'])


#ReadFile
file_text=open(os.environ['file'],'r')
first_profile=file_text.readline()
mail,password,coursetech=first_profile.split(',')
print(mail)
print(password)
print(coursetech)
file_text.close()

#Database Connection
mydb=mysql.connector.connect(host=os.environ['host'],user=os.environ['username'],password=os.environ['dbpass'],database=os.environ['database'])

#Fetch Data
mycursor=mydb.cursor()
mycursor.execute("""select * from projects.groups where course=%s order by RAND() limit 1""",(coursetech,) )
result=mycursor.fetchone()
print(result)
url,name=result
print(url)
print(name)





#Login
driver.find_element(By.ID,'email').send_keys(mail)
driver.find_element(By.ID,'password').send_keys(password)
driver.find_element(By.XPATH,
                    '/html/body/div[2]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[4]/button/div').click()
time.sleep(10)







#Get date
datetime=datetime.datetime.now()
date=datetime.day

month=datetime.strftime("%b")
print(date)
print(month)

#Load URL
driver.get(url)
time.sleep(25)

driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div/div[2]/div/div/div[1]/button[1]/div/div[2]/div').click()
time.sleep(10)






#Image Manipulation


folder_path=os.environ['folder']
folder=os.path.join(folder_path+ "\\" + coursetech +"\\"+"*")
file_list=glob.glob(folder)
image=random.choice(file_list)
path=os.path.basename(image)
print(path)
image_path=os.path.join(os.environ['output']+"\\"+path)
print(image_path)


mycursor.execute("""select * from coordinates where img=%s""",(path,))
result=mycursor.fetchone()
print(result)
height,width,X,Y,R,G,B,image_details=result
print(height)
print(width)
print(X)
print(Y)
print(R)
print(G)
print(B)
image=cv2.imread(image,1)
text=str(date)+str(month)+"9pm"
image=cv2.putText(image,text,(X,Y),cv2.FONT_HERSHEY_TRIPLEX,1,(R,G,B),1,cv2.LINE_AA)
path=os.path.join(os.environ['output']+"\\"+path)
cv2.imwrite(path,image)

keyboard = Controller()
driver.find_element(By.XPATH,'//*[@id="modal_footer_portal_container"]/div/div/div/div[1]/div[1]/div[2]').send_keys(image_path)
time.sleep(5)
keyboard.type(image_path)
keyboard.press(Key.enter)
time.sleep(5)


driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/button/div/div/div').click()


time.sleep(50)
url=driver.current_url

final_output=os.path.join(os.environ['output_urls']+"\\"+"urls.txt")
os.remove(image_path)

with open(final_output,'a+') as fo:
    fo.write(url)
    fo.write("\n")
















