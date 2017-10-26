import numpy as np
import re


##### Read text one time and save line by line
lines = [line.rstrip() for line in open('./input/itcont.txt')]

##### Regular expressions for all information we need to search
CMTE_ID = r'C\d+'
ZIP_CODE = r'\|\d{5}\||\|\d{9}\|'
TRANSACTION_DT_AMT = r'\|\d{8}\|\d{1,4}\|'  ## Date and Amount grouped
OTHER_ID = r'H\d\w{2}\d{5}'


cand_zip = {}
cand_date = {}

f = open('./output/medianvals_by_zip.txt','w')

for line in lines:

    date_amount = re.compile(TRANSACTION_DT_AMT).search(line).group().split('|')
    date = date_amount[1]
    amount = int(date_amount[2])

    other = re.compile(OTHER_ID).search(line)
    cand  = re.compile(CMTE_ID).search(line).group()
    zipcd = re.compile(ZIP_CODE).search(line).group().split('|')[1][0:5]  

##### OTHER_ID unconsidered
    if not other:

##### Candidate & Zipcode grouped-together dictionary: candzip
##### Dictionary candzip structure:
##### {(Candidate_ID,Zipcode):(Number,[Amount List])}

		candzip = (cand,zipcd)
		if cand_zip.has_key(candzip):
			amount_list = cand_zip[candzip][1]
			amount_list.append(amount)
			cand_zip[candzip] = (cand_zip[candzip][0]+1,amount_list)
		else:
			cand_zip[candzip] = (1,[amount])

##### Candidate & Date grouped-together dictionary: candate
##### Dictionary candate structure:
##### {(Candidate_ID,Date):(Number,[Amount List])}

		candate = (cand,date)
		if cand_date.has_key(candate):
			amount_list = cand_date[candate][1]
			amount_list.append(amount)
			cand_date[candate] = (cand_date[candate][0]+1,amount_list)
		else:
			cand_date[candate] = (1,[amount])

##### Get median for medianvals_by_zip.txt
		median = int(round(np.median(cand_zip[candzip][1])))

##### Adjust Output format
		result =[cand,zipcd,str(median),cand_zip[candzip][0],sum(cand_zip[candzip][1])]
		f.write('|'.join(str(txt) for txt in result)+'\n')

f.close()

f = open('./output/medianvals_by_date.txt','w')

for key in sorted(cand_date):
##### Get median for medianvals_by_date.txt
    median = int(round(np.median(cand_date[key][1])))

    result =[key[0],key[1],median,cand_date[key][0],sum(cand_date[key][1])]      
    f.write('|'.join(str(txt) for txt in result)+'\n')
f.close()
