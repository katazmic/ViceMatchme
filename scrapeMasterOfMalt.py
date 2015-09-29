
# coding: utf-8

from bs4 import BeautifulSoup
import urllib2
import json

urlM = 'https://www.masterofmalt.com'
page = urllib2.urlopen(urlM+'/whisky')
soup = BeautifulSoup(page.read())

emptyurls = [ '/country-style/scotch/malt-spirit-and-new-make-whisky/','/country-style/american/straight-corn-whiskey/','/country-style/american/straight-wheat-whiskey/']

url_country = []
for countries in soup.findAll("div", {"class" : "promotions_linkList"}):
    for cnt in countries.findAll('a'):
        if cnt.get('href') not in emptyurls:
            url_country.append(urlM + str(cnt.get('href')))

url_country.pop(-1)



linkWhiskey = []
url_coun = url_country
for urlC in url_coun:
    page = urllib2.urlopen(urlC)
    soup = BeautifulSoup(page.read())
    print urlC
    for link in soup.findAll("div", {"class":"ctrl_PBW_Mid_Title"}):
        linkWhiskey.append(link.find('a').get('href'))
        print link.find('a').get('href')
    while 1<2:
        if len(soup.findAll("span", {"id":"ContentPlaceHolder1_ctl05_pageNext"}))!=0:
            next_url = soup.findAll("span", {"id":"ContentPlaceHolder1_ctl05_pageNext"})[0].find('a')
            if next_url != None:
                url = next_url.get('href')
            else:
                break
        else:
            break
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        for link in soup.findAll("div", {"class":"ctrl_PBW_Mid_Title"}):
            linkWhiskey.append(link.find('a').get('href'))
            print link.find('a').get('href')



links = {}
for i in range(2345):
    links[str(i)] = linkWhiskey[i]

with open('MoM_Links.json', 'w') as ff:
    json.dump(links, ff)

ff.close()

data = {}
inc = 0
weirdItemScope = []
annotedWhiskeys = []
for urlW in linkWhiskey:
    print "scraping .."
    inc = inc+1
    page = urllib2.urlopen(urlW)
    soup = BeautifulSoup(page.read())
    itemScope = soup.findAll("span" ,{"itemscope":"itemscope"})[2:]

    try:
        wName = str(itemScope[-1].get_text())
    except:
        wName = str(urlW.split('/')[-2].replace('-',' '))
    print wName
    
    data[wName] = {}
    data[wName]['link'] = urlW

    if len(itemScope) == 4:
        data[wName]['country'] = str(itemScope[0].get_text())# str                                                                                
        try:
            data[wName]['region'] = str(itemScope[1].get_text())
        except:
            data[wName]['region'] = str(itemScope[1].find('a').get('href').split('/')[-2].replace('-',' '))
        try:
            data[wName]['distillery'] = str(itemScope[2].get_text())
        except:
            data[wName]['distillery'] = itemScope[2].get_text()
            
    if len(itemScope) == 3:
        data[wName]['region'] = 'N/A'
        data[wName]['country']=str(itemScope[0].get_text())#str                                                                                  
        try:
            data[wName]['distillery']=str(itemScope[1].get_text())
        except:
            data[wName]['distillery'] = itemScope[1].find('a').get('href').split('/')[-2].replace('-',' ')                              
    if len(itemScope) != 3 and len(itemScope) != 4:
        data[wName]['itemscope'] = itemScope
        weirdItemScope.append(wName)
    try:    
        data[wName]['rating'] =  float(str(soup.find("meta",{"property":"og:rating"}).get('content')))
    except: 
        data[wName]['rating'] = 'N/A'

    try:
        data[wName]['price'] = float(str(soup.findAll("meta",{"property":"product:price:amount"})[1].get('content')))
    except:
        data[wName]['price'] = 'N/A'
    
    try:
        data[wName]['style'] = soup.find("div", {"id":"ContentPlaceHolder1_ctl01_ctl02_wdItemNameStyle"}).get('content')
    except: 
        data[wName]['style'] = 'N/A'
    

    try:
        data[wName]['description'] = soup.find("span", {"itemprop":"description"}).get_text()
    except:
        data[wName]['description'] = 'N/A'


    try:
        data[wName]['full notes'] = soup.find("div", {"id":"ContentPlaceHolder1_ctl01_ctl01_breakDownTastingNote"}).get_text()
    except:
        data[wName]['full notes'] = 'N/A'
        
    nt=[]
    if len(soup.findAll("p", {"class":"pageCopy"}))>1:
        for notes in soup.findAll("p", {"class":"pageCopy"}):
            nt.append(str(notes.get_text().split(':')[0]))
            data[wName][str(notes.get_text().split(':')[0])] = notes.get_text().split(':')[1]
        annotedWhiskeys.append(wName)
        if 'Nose' not in nt:
            data[wName]['Nose'] = 'N/A'
        if 'Palate' not in nt:
            data[wName]['Palate'] = 'N/A'
        if 'Finish' not in nt:
            data[wName]['Finish'] = 'N/A'
        if 'Overall' not in nt:
            data[wName]['Overall'] = 'N/A'
    else:
        data[wName]['Nose'] = 'N/A'
        data[wName]['Palate'] = 'N/A'
        data[wName]['Finish'] = 'N/A'
        data[wName]['Overall'] = 'N/A'
        
    if data[wName]['full notes'] == 'N/A':
            try:
                data[wName]['full notes'] = soup.findAll("p", {"class":"pageCopy"}).get_text()
            except:
                data[wName]['full notes'] = 'N/A'  
        
    try:
        data[wName]['image'] = str(soup.find("div",{"class":"productImageWrap"}).find('img').get('src'))[2:]
    except:
        data[wName]['image'] = 'N/A'

    revs = []
    for rev in soup.findAll("p" ,{"itemprop":"reviewBody"}):
        revs.append(rev.get_text())
    if len(revs)!=0:
        data[wName]['reviews'] = revs        
    else:
        data[wName]['reviews'] = 'N/A'
        
    print inc
    print '%f percent'%(float(inc)/float(len(linkWhiskey))*100.)  

with open('MoM_whiskeys.json', 'w') as ff:
    json.dump(data, ff)

ff.close() 



