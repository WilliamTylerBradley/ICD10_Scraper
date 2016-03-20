import csv
import requests
import re
from bs4 import BeautifulSoup

icd10_codes = {}

#file = open("ICD10_Codes.csv",'wb')
#writer = csv.writer(file)

# Function to pull links
def follow_links(url):
	#print(url)
	page = requests.get("http://www.icd10data.com"+url)
	soup = BeautifulSoup(page.text)
	next_urls = soup.find_all('a', href=True)
	no_matches = True
	for a in next_urls:
		#print a['href'][:len(url)]
		if a['href'][:len(url)] == url and len(a['href']) > len(url):
			#print(a['href'])
			follow_links(a['href'])
			no_matches = False
		#else:
			#print("next url: ",a['href'])
			#print("match url ",a['href'][:(len(url)+1)])
			#print("len url ",len(a['href']))
	if no_matches:
		icd_10_cd = url.split('/')
		icd_10_cd = icd_10_cd[len(icd_10_cd)-1]
		h2_list = soup.find_all('h2')
		if len(h2_list) > 0:
			for h2 in h2_list:
				print icd_10_cd+' '+h2.text
				icd10_codes[icd_10_cd] = h2.text
				#writer.writerow((icd_10_cd,h2.text))
		

# http://www.icd10data.com/ICD10CM/Codes
#url = "/ICD10CM/Codes"

url = "/ICD10CM/Codes/A00-B99"



#page = requests.get(url)
#soup = BeautifulSoup(page.text)

follow_links(url)


#file.close()

with open("ICD10_Codes.csv",'wb') as file:
	writer = csv.writer(file)
	for code, text in icd10_codes.items():
		try:
			writer.writerow([code, text.encode('latin-1')])
		except:
			print(text)