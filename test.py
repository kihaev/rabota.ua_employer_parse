from bs4 import BeautifulSoup
from selenium import webdriver
import pickle

driver = webdriver.Firefox(executable_path='./geckodriver')

def load_cookie(driverx, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driverx.add_cookie(cookie)


driver.get("https://notebook.rabota.ua/employer/notepad/cvs?vacancyId=-1")
load_cookie(driver, './cookies.pkl')
for page in range(1, 19):
    link = 'https://notebook.rabota.ua/employer/notepad/cvs?vacancyId=-1&pg=' + str(page)
    source = driver.get('https://notebook.rabota.ua/employer/notepad/cvs?vacancyId=-1&pg=' + str(page))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for profile in soup.find_all("a", class_="rua-p-t_16 rua-p-c-default ga_cv_view_cv"):
        profile_url = profile["href"]
        name_surname = profile.text
        driver.get(profile_url)
        email = soup.find("span", id_="ctl00_centerZone_BriefResume1_CvView1_cvHeader_lblEmailValue").get_text()
        phone_number = soup.find("span", id_="ctl00_centerZone_BriefResume1_CvView1_cvHeader_lblPhoneValue").get_text()
        city = soup.find("span", id_="ctl00_centerZone_BriefResume1_CvView1_cvHeader_lblRegionValue").get_text()
        print(name_surname)
        print(profile_url)
        print(email)
        print(phone_number)
        print(city)
    for cv in soup.find_all("a", class_="rua-p-t_16 opacity rua-b-none"):
        cv_url = cv["href"]
        driver.get(cv_url)
