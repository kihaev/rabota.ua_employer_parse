from bs4 import BeautifulSoup

te = open('1.html').read()

print(te)


soup_ins = BeautifulSoup(te, "html.parser")
print(soup_ins)
        # ctl00_centerZone_BriefResume1_CvView1_cvHeader_lblEmailValue
        # ctl00_centerZone_BriefResume1_ViewAttachedCV1_cvHeader_lblEmailValue
        # ctl00_centerZone_BriefResume1_CvView1_cvHeader_lblEmailValue

email = soup_ins.find("span", {"id", "ctl00_centerZone_BriefResume1_ViewAttachedCV1_cvHeader_lblEmailValue"})

email_s = email.get_text()
print(email_s)
# phone_number = soup_ins.find("span", id_="ctl00_centerZone_BriefResume1_CvView1_cvHeader_lblPhoneValue").get_text()
# city = soup_ins.find("span", id_="ctl00_centerZone_BriefResume1_CvView1_cvHeader_lblRegionValue").get_text()
# print(name_surname)
# print(profile_url)
print(email)
# print(phone_number)
# print(city)