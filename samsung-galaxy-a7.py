import urllib.request as ur
import re

url = ['http://www.mysmartprice.com/mobile/samsung-galaxy-a7-16gb-msp5959']
htmlfile = ur.urlopen(url[0])
htmltext = htmlfile.read().decode('UTF-8')

str1 = '<title>(.+?) Price in India 2015'
regex = str1
pattern = re.compile(regex)
titles = re.findall(pattern, htmltext)
print (titles)

str2 = '<strong>(.+?)</strong>'
regex = str2
pattern = re.compile(regex)
attribs = re.findall(pattern, htmltext)

c1 = (len(attribs))
print (c1)

str3 = '<div class="store_rating_bar_out" data-storename="(.+?)"'
regex = str3
pattern = re.compile(regex)
storename = re.findall(pattern, htmltext)

c2 = (len(storename))
print (c2)

str4 = '<div class="store_price">Rs.(.+?)</div>'
regex = str4
pattern = re.compile(regex)
price = re.findall(pattern, htmltext)

c3 = (len(price))
print (c3)

str5 = '<div class="rating" title="(.+?)">'
regex = str5
pattern = re.compile(regex)
rating = re.findall(pattern, htmltext)

c4 = (len(rating))
print (c4)


str6 = '<div class="variant_namein">(.+?) <!--color--></div>'
regex = str6
pattern = re.compile(regex)
variants1 = re.findall(pattern, htmltext)

c5 = (len(variants1))
print (c5)

str7 = '<div class="variant_gostore">(.+?) target='
regex = str7
pattern = re.compile(regex)
variants2 = re.findall(pattern, htmltext)

c6 = (len(variants2))
print (c6)

str8 = '<div class="variant_price">Rs.(.+?)</div>'
regex = str8
pattern = re.compile(regex)
variants3 = re.findall(pattern, htmltext)

c7 = (len(variants3))
print (c7)

import csv
b = open('test1.csv', 'w')
a = csv.writer(b)

data = [c1,c2,c3,c4,c5,c6,c7]

for val in data:
   a.writerow([val])

data = [titles, attribs, storename, price, rating, variants1, variants2, variants3]
a.writerows(data)
        
b.close()
