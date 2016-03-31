import csv
import requests
import re
from bs4 import BeautifulSoup

icd10_codes = {}

#file = open("ICD10_Codes.csv",'wb')
#writer = csv.writer(file)

# Function to pull links
def follow_links(url):
	page = requests.get("http://www.icd10data.com"+url)
	soup = BeautifulSoup(page.text)
	next_urls = soup.find_all('a', href=True)
	no_matches = True
	for a in next_urls:
		## the -1 on the lengths is for urls with missing '-', check M84.x
		if a['href'][:(len(url)-1)] == url[:(len(url)-1)] and a['href'].count('/') > url.count('/'):
			follow_links(a['href'])
			no_matches = False
	if no_matches:
		icd_10_cd = url.split('/')
		icd_10_cd = icd_10_cd[len(icd_10_cd)-1]
		h2_list = soup.find_all('h2')
		if len(h2_list) > 0:
			for h2 in h2_list:
				print icd_10_cd+' '+h2.text
				icd10_codes[icd_10_cd] = h2.text
		

# http://www.icd10data.com/ICD10CM/Codes
url = "/ICD10CM/Codes"

#url = "/ICD10CM/Codes/M00-M99/M80-M85/M84-"
#url = "/ICD10CM/Codes/C00-D49/C7A-C7A/C7A-"
#page = requests.get(url)
#soup = BeautifulSoup(page.text)

follow_links(url)


#file.close()

with open("ICD10_Codes.csv",'wb') as file:
	writer = csv.writer(file)
	for code, text in icd10_codes.items():
		try:
			writer.writerow([code, text.encode('latin-1')])
			print('Done')
		except:
			print(text)
