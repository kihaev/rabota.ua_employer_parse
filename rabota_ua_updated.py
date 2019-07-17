from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pickle 
import sqlite3


# connection to db
def conn_db(path):
    connx = sqlite3.connect(path)
    cursorx = connx.cursor()
    return connx, cursorx


# create table
def create_table_db(name):
    create_table = "CREATE TABLE " + name + " (Ad_Name text, Ad_Url text, Price text, Phone_Number text, Breed text)"
    try:
        mycursor.execute(create_table)
    except sqlite3.OperationalError:
        drop_table_db(name)
        mycursor.execute(create_table)
        
          
# drop table from db
def drop_table_db(name):
    drop_table = "DROP TABLE " + name
    mycursor.execute(drop_table)
    
    
# insert animal info into db
def insert_into_db(table_name, Ad_name, Ad_url, Price, Phone_number, Breed):
    sql = "INSERT INTO "+table_name+" (Ad_Name, Ad_Url, Price, Phone_Number, Breed) VALUES (?, ?, ?, ?, ?)"
    val = (Ad_name, Ad_url, Price, Phone_number, Breed)
    mycursor.execute(sql, val)
    conn.commit()
    
    
# initializing webdriver
def sel_init(path, start_page):
    driverx = webdriver.Firefox(executable_path=path)
    driverx.get(start_page)
    return driverx


# loading cookies to webdriver
def load_cookie(path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)
            
            
# parsing animals info
def get_animals_info(start_page, table_name):
    #find last page number
    driver.get(start_page)
    soup_page = BeautifulSoup(driver.page_source, "html.parser")
    num_page = soup_page.find("div", {"class":"pager rel clr"})
    last_page = int(num_page.find_all("span")[-3].get_text())
    #check all pages
    for page in range(1, last_page + 1):
        driver.get(start_page + "&pg=" + str(page))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        #check all advertisements
        for ad_num, ad in enumerate(soup.find_all("a", class_="marginright5 link linkWithHash detailsLink")[5:]):
            ad_url = ad["href"]
            price = soup.find_all("p", {"class":"price"})[ad_num + 5].text.strip()
            ad_name = ad.text.strip()
            driver.get(ad_url)
            sleep(5)
            #getting phone number
            elem = driver.find_element_by_xpath('//*[@id="contact_methods"]/li[2]/div')
            elem.click()
            sleep(5)
            soup_ad = BeautifulSoup(driver.page_source, "html.parser")
            phone_number = soup_ad.find("strong",{"class":"xx-large"}).text
            breed = soup_ad.find_all("td", {"class":"value"})[1].text.strip()
            print(ad_name + "\n" + ad_url +"\n"+ price +"\n"+ phone_number + "\n" + breed)
            #inserting info
            insert_into_db(table_name, ad_name, ad_url, price, phone_number, breed)

                
# show results
def show_table_rows(name):
    sql_select_all = "SELECT * FROM " + name
    mycursor.execute(sql_select_all)
    print(mycursor.fetchall())


#start                        
def start():
    create_table_db(table_name_dogs)
    create_table_db(table_name_cats)
    #sleep(300)
    #pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))
    load_cookie(cookies_path)
    get_animals_info(starting_page_dogs, table_name_dogs)
    get_animals_info(starting_page_cats, table_name_cats)
    show_table_rows(table_name_dogs)
    show_table_rows(table_name_cats)

    
#constants    
database_path = "mydatabase_animals.db"
table_name_cats = "cats"
table_name_dogs = "dogs"
driver_path = "C:\\Users\\yurak\\Desktop\\test\\geckodriver.exe"
cookies_path = "cookies.pkl"
starting_page_dogs = "https://www.olx.ua/zhivotnye/sobaki/kiev/q-Печерский/?search%5Border%5D=created_at%3Adesc"
starting_page_cats = "https://www.olx.ua/zhivotnye/koshki/kiev/q-Печерский/?search%5Border%5D=created_at%3Adesc"
authorization_page = "https://www.olx.ua/account/?ref%5B0%5D%5Baction%5D=myaccount&ref%5B0%5D%5Bmethod%5D=index"
conn, mycursor = conn_db(database_path)
driver = sel_init(driver_path, authorization_page)


start()