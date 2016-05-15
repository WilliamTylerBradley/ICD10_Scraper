##########
# This code scrapes ICD 10 data from http://www.icd10data.com
##########

## Imports
import csv
import requests
import re
from bs4 import BeautifulSoup

# Start blank dictionary
icd10_codes = {}

## Function to pull links
# Becuase of the site's layout as a tree structure, using a recursive function makes sense
# This function looks through all the links on a given page
# If any are further down the tree, follow them
# If none are further down the tree, you reached a final ICD10 code, save the data
def follow_links(url):
	# Get the page and find all the links
	page = requests.get("http://www.icd10data.com"+url)
	soup = BeautifulSoup(page.text)
	next_urls = soup.find_all('a', href=True)
	# Assume you are on a final page for a diagnosis code by
	#	setting a variable for finding new links to false
	no_matches = True
	# Look through the links
	for a in next_urls:
		# If any match the current page and have a little more (another '/'), then it is further down the tree
		# Ex: 'http://www.icd10data.com/ICD10CM/Codes/S00-T88/T36-T50/T48-'
		# then to 'http://www.icd10data.com/ICD10CM/Codes/S00-T88/T36-T50/T48-' + '/T48.0X4D'
		#
		# (the -1 on the lengths is for urls with missing '-', check M84.x)
		if a['href'][:(len(url)-1)] == url[:(len(url)-1)] and a['href'].count('/') > url.count('/'):
			# Go further down the tree
			follow_links(a['href'])
			# Don't save data
			no_matches = False
	# Save data if no matches
	if no_matches:
		icd_10_cd = url.split('/')
		icd_10_cd = icd_10_cd[len(icd_10_cd)-1]
		h2_list = soup.find_all('h2')
		if len(h2_list) > 0:
			for h2 in h2_list:
				print icd_10_cd+' '+h2.text
				icd10_codes[icd_10_cd] = h2.text
		

# Start at the first URL with the basic links
url = "/ICD10CM/Codes"
follow_links(url)

# Output all the data to a csv
with open("ICD10_Codes.csv",'wb') as file:
	writer = csv.writer(file)
	for code, text in icd10_codes.items():
		try:
			writer.writerow([code, text.encode('latin-1')]) # Watch the encoding for a few diaseses
			print('Done')
		except:
			print(text)
