# coding: utf-8

import json 
import numpy as np
import pymysql as mdb
import pandas as pd



with open('WhiskeyStructureUpdated.json') as data_file:  #categories, notes, strength, categories vector, notes vector
    dataW = json.load(data_file)

data_file.close()



HOST = 'localhost'
USER = 'root'
PASSWD = ''




db_connect = mdb.connect(host = HOST,user = USER,passwd = PASSWD)


cursor = db_connect.cursor()
try:
    cursor.execute('CREATE DATABASE ViceMatchUpdated')
except:
    pass

cursor.execute('USE ViceMatchUpdated')

try:
    cursor.execute("""
    DROP TABLE whiskey_info
    """)
except:
    pass

cursor.execute('USE ViceMatchUpdated')
cursor.execute("""
    CREATE TABLE whiskey_info(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    notes TEXT,
    categories TEXT,
    image TEXT,
    strength TEXT, 
    wood DOUBLE,
    fruits DOUBLE,
    spice DOUBLE,
    earth DOUBLE,
    nuts DOUBLE,
    cereal DOUBLE,
    chocolate DOUBLE,
    vanilla DOUBLE,
    flowers DOUBLE,
    coffee DOUBLE,
    feint DOUBLE,
    mineral DOUBLE,
    PRIMARY KEY (id)
    )
    """)


add_whiskey = ("INSERT INTO whiskey_info "
           " (name,notes,categories,image,strength, wood, fruits, spice, earth, nuts, cereal, chocolate, vanilla, flowers, coffee, feint,mineral)"
           " VALUES (%s,%s,%s,%s, %s,%s,%s,%s,%s, %s, %s,%s,%s,%s, %s,%s,%s)")

NoteCategories = ['wood', 'fruits', 'spice', 'earth', 'nuts', 'cereal', 'chocolate', 'vanilla', 'flowers', 'coffee', 'feint','mineral']

MainNotes      = ['wood', 'fruits', 'spice', 'earth', 'nuts', 'cereal', 'chocolate', 'vanilla', 'flowers', 'coffee', 'feint','mineral']



for i in dataW:
    try:
        name = str(dataW[i]['name'].split('  ')[0]) #pop first is a space
        dataW[i]['name'] = name
        image = str(dataW[i]['image'])
        notes = str(dataW[i]['notes'])
        categories = str(dataW[i]['note categories'])
        strength =  str(dataW[i]['strength'])

        whiskey_data = (name,notes,categories,image,strength) +tuple(dataW[i]['category vector'][n] for n in range(len(dataW[i]['category vector'])))
        
        cursor.execute(add_whiskey, whiskey_data)
        db_connect.commit()
    except:
        1+1
        
        
###   cigars

with open('CigarStructureUpdated.json') as data_file:
    dataC = json.load(data_file)

data_file.close()



cursor.execute('USE ViceMatchUpdated')
try:
    cursor.execute("""
    DROP TABLE cigar_info
    """)
except:
    pass

cursor.execute("""
    CREATE TABLE cigar_info(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    notes TEXT,
    categories TEXT,
    image TEXT,
    strength TEXT,
    wood DOUBLE,
    fruits DOUBLE,
    spice DOUBLE,
    earth DOUBLE,
    nuts DOUBLE,
    cereal DOUBLE,
    chocolate DOUBLE,
    vanilla DOUBLE,
    flowers DOUBLE,
    coffee DOUBLE,
    feint DOUBLE,
    mineral DOUBLE,
    PRIMARY KEY (id)
    )
    """)

add_cigar = ("INSERT INTO cigar_info "
            " (name,notes,categories,image,strength, wood, fruits, spice, earth, nuts, cereal, chocolate, vanilla, flowers, coffee, feint,mineral)"
            " VALUES (%s,%s,%s,%s, %s,%s,%s,%s,%s, %s, %s,%s,%s,%s, %s,%s,%s)")


for i in dataC:
    name = str(dataC[i]['name'].split('  ')[0])
    dataC[i]['name'] = name
    image = str(dataC[i]['image'])
    notes = str(dataC[i]['notes'])
    categories = str(dataC[i]['note categories'])
    strength =  str(dataC[i]['strength'])
#       cigar_data = (name,notes,categories,image,strength, wood, fruits, spice, earth, nuts, cereal, chocolate, vanilla, flowers, coffee, feint)
    cigar_data = (name,notes,categories,image,strength) +tuple(dataC[i]['category vector'][n] for n in range(len(dataC[i]['category vector'])))

    cursor.execute(add_cigar, cigar_data)
    db_connect.commit()


################# MATCHING TABLE


cursor.execute('USE ViceMatchUpdated')
try:
    cursor.execute("""
    DROP TABLE Vmatch
    """)
except:
    pass

cursor.execute('USE ViceMatchUpdated')
cursor.execute("""
    CREATE TABLE Vmatch(
    id INTEGER NOT NULL AUTO_INCREMENT,
    whiskeyName TEXT NOT NULL,
    cigarName TEXT NOT NULL,
    highestMatch DOUBLE,
    overallMatch DOUBLE,
    wood DOUBLE,
    fruits DOUBLE,
    spice DOUBLE,
    earth DOUBLE,
    nuts DOUBLE,
    cereal DOUBLE,
    chocolate DOUBLE,
    vanilla DOUBLE,
    flowers DOUBLE,
    coffee DOUBLE,
    feint DOUBLE,
    mineral DOUBLE,
    PRIMARY KEY (id)
    )
    """)


add_match = ("INSERT INTO Vmatch "
             " (whiskeyName, cigarName, highestMatch, overallMatch, wood, fruits, spice, earth, nuts, cereal, chocolate, vanilla, flowers, coffee, feint,mineral)"
             " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")



categories_notes = {'flowers':['tulips','violets','bouquet','flowers','floral','herbaceous','herbal','hay','haylike'], 
                    'plants':['grass','grassy','moss','tea','vegetal'], 
                    'wood':['cedar','cedary','oak','wood','woody','woodsy','woodiness','pine'],
                    'spice':['spice','spiciness','spicy','spices','anice','licorice','cardamon','nutmeg','pepper','peppery','cinnamon','clove','cloves','cumin','cayenne','chili','allspice'],
                    'earth':['barnyard','earth','earthy','earthy/peaty','earthiness','smoke','peat','smoky'],
                    'mineral':['lead','graphite','mineral','musk','musty','salt','salty','saltiness','savory','chalk'],
                    'fruits':['Watermelon','peach','currant','fruity','fruit','mango','pineapple','apple','raisin','plum','cherry','cherries','berry','orange','zest','citrus','lemon'],
                    'nuts':['walnut','peanut','marzipan','cashew','almond','nut','nuts','nuttiness','nutty','hazelnut','praline'],
                    'feint':['leather','leathery','honey','beewax','mead','molasses'],
                    'chocolate':['cocoa','chocolate','chocolately','chocolaty','cream','butter','milky','creamy','creaminess'],
                    'coffee':['espresso','coffee/mocha','coffee','mocha','roasted'],
                    'vanilla':['caramel','custard','toffee','butterscotch','vanilla'],
                    'cereal':['bran','bread','oat','barley','yeasty','husky','toasted']}


lensC = [len(categories_notes[NoteCategories[i]])for i in range(len(NoteCategories))]

data_matched ={}
k=0

for w in dataW.keys():
    whiskey = dataW[w]
    for c in dataC.keys():
        le=0
        cigar = dataC[c]
        strngth = float(np.dot(dataW[w]['strength vector'],dataC[c]['strength vector']))
        if strngth !=0 and dataC[c]['image'] !='http://www.jrcigars.com/images/item/default.jpg/220/220':
            data_matched[str(k)] = {}        
            data_matched[str(k)]['whiskeyName'] = str(whiskey['name'].split('  ')[0])
            data_matched[str(k)]['cigarName'] = str(cigar['name'].split('  ')[0])
            highestM = 0
            cosCat = []
            for lnC in range(len(lensC)):
                lb = le
                le = lb+lensC[lnC]
                C_n = dataC[c]['note vector'][lb:le]
                W_n = dataW[w]['note vector'][lb:le]
                if np.sqrt((np.dot(C_n,C_n)*np.dot(W_n,W_n))) !=0 :
                    data_matched[str(k)][NoteCategories[lnC]] = round(float(np.dot(W_n,C_n))/np.sqrt((np.dot(C_n,C_n)*np.dot(W_n,W_n))),2)
                   # print data_matched[str(k)][NoteCategories[lnC]] 
                    if float(np.dot(W_n,C_n))/np.sqrt((np.dot(C_n,C_n)*np.dot(W_n,W_n)))>highestM:
                        highestM = float(np.dot(W_n,C_n))/np.sqrt((np.dot(C_n,C_n)*np.dot(W_n,W_n)))
                    cosCat.append(round(float(np.dot(W_n,C_n))/np.sqrt((np.dot(C_n,C_n)*np.dot(W_n,W_n))),2))
                else:
                    data_matched[str(k)][NoteCategories[lnC]]  = 0.0
                    cosCat.append(0.0)
                    
            data_matched[str(k)]['catVecMatch'] = np.dot(dataW[w]['category vector'],dataC[c]['category vector'])/np.sqrt(np.dot(dataC[c]['category vector'],dataC[c]['category vector'])*np.dot(dataW[w]['category vector'],dataW[w]['category vector']))
            data_matched[str(k)]['overallMatch'] = round((np.dot(dataW[w]['category vector'],cosCat)/float(sum(dataW[w]['category vector']))),2)
            data_matched[str(k)]['highestMatch'] = round(highestM,2)
            k=k+1
        
        

    #    data_matched.append(dict(whiskeyName = whiskey['name'], cigarName = cigar['name'], matchScore = scr))    



k=0
for matched in data_matched:
    match_data = (data_matched[matched]['whiskeyName'],data_matched[matched]['cigarName'],data_matched[matched]['highestMatch'],data_matched[matched]['overallMatch'])+tuple(str(data_matched[matched][n]) for n in NoteCategories)
    if  data_matched[matched]['overallMatch']>0.5:
        k=k+1
        cursor.execute(add_match, match_data)
        db_connect.commit()







cursor.execute('USE ViceMatchUpdated')
try:
    cursor.execute("""
        DROP TABLE Vmatch_more
        """)
except:
    pass

cursor.execute("""
    CREATE TABLE Vmatch_more(
    id INTEGER NOT NULL AUTO_INCREMENT,
    whiskeyName TEXT NOT NULL,
    cigarName TEXT NOT NULL,
    category TEXT,
    matchScore DOUBLE,
    overallMatch DOUBLE,
    PRIMARY KEY (id)
    )
    """)


add_more_matches = ("INSERT INTO Vmatch_more "
             " (whiskeyName, cigarName, category, matchScore, overallMatch)"
             " VALUES (%s, %s, %s, %s, %s)")
Vmatchd = data_matched.copy()

for m in data_matched:
    if Vmatchd[m]['highestMatch']<0.4: #0.62 for all combnies (47 ones)
        del Vmatchd[m]



cursor.execute('USE ViceMatchUpdated')
try:
    cursor.execute("""
        DROP TABLE Vmatch_more
        """)
except:
    pass

cursor.execute("""
    CREATE TABLE Vmatch_more(
    id INTEGER NOT NULL AUTO_INCREMENT,
    whiskeyName TEXT NOT NULL,
    cigarName TEXT NOT NULL,
    category TEXT,
    matchScore DOUBLE,
    overallMatch DOUBLE,
    PRIMARY KEY (id)
    )
    """)

pdW = pd.DataFrame(Vmatchd)
pdW = pdW.transpose()

dropdown=[]
nd=0
for i in dataW.keys():
    whiskeyName = i
    pd_sp = pdW[pdW.whiskeyName == i]
    try:
        pd_BM = pd_sp[pd_sp['overallMatch']*pd_sp['catVecMatch']  == max(pd_sp['overallMatch']*pd_sp['catVecMatch'])]
        #pd_BM = pd_sp[pd_sp['overallMatch']  == max(pd_sp['overallMatch'])]
        #pd_BM = pd_sp[pd_sp['catVecMatch']  == max(pd_sp['catVecMatch'])]
        #print '%f %f %f' %(pd_BM['overallMatch'][0],pd_BM2['overallMatch'][0],pd_BM3['overallMatch'][0])
        cigarName = pd_BM['cigarName'][0]
        matchScore = pd_BM['highestMatch'][0]
        overallMatch = pd_BM['overallMatch'][0]
        more_match_data = (whiskeyName,cigarName, 'All' ,matchScore,overallMatch)
        dropdown.append("<option value=\"%s\">%s</option>" %(whiskeyName,whiskeyName))
        #print "<option value=\"%s\">%s</option>"%(whiskeyName,whiskeyName)
        cursor.execute(add_more_matches, more_match_data)
        db_connect.commit()
    except:
        pass
    
    
  
    cats = dataW[i]['note categories'].split(', ')
    found = 0
    for cat in cats:
        pdTempCat = pd_sp[pd_sp[str(cat)] == pd_sp['highestMatch']]
        #pd2 = pdTempCat.transpose()           
        #catL = MainNotes[:]
        #catL = MainNotes[:]
        #poppedc = catL.pop(MainNotes.index(cat))
        #indecies = [list(pd2.index).index(i) for i in catL]
        #pdN = pd2.iloc[indecies]
        #pdSummed = pdN.sum()
        #sum = pdSummed.ix(min(pdSummed))
        #minOther = pdSummed[pdSummed == min(pdSummed)]
        if len(pdTempCat) != 0:
            c = pdTempCat['cigarName'][0]
            cigCats = dataC[c]['category vector']
            minsum = sum(cigCats[:MainNotes.index(cat)]+cigCats[MainNotes.index(cat)+1:])
            respd = pdTempCat[pdTempCat['cigarName']==c]

            for c in pdTempCat['cigarName'][1:]:
                cigCats = dataC[c]['category vector']
                minT = sum(cigCats[:MainNotes.index(cat)]+cigCats[MainNotes.index(cat)+1:])
                if minT<minsum:
                    minsum = minT
                    respd = pdTempCat[pdTempCat['cigarName']==c]
            

            cigarName = respd['cigarName'][0]
            matchScore = respd['highestMatch'][0] 
            overallMatch = respd['overallMatch'][0] 
                                    
            #cigarName = pdTempCat[ pdTempCat.index == minOther.index[0]]['cigarName'][0]
            #matchScore = pdTempCat[ pdTempCat.index == minOther.index[0]]['highestMatch'][0] 
            #overallMatch = pdTempCat[ pdTempCat.index == minOther.index[0]]['overallMatch'][0] 
            if minsum<3 and cigarName != pd_BM['cigarName'][0]:
                more_match_data = (whiskeyName,cigarName, cat,matchScore,overallMatch)
                cursor.execute(add_more_matches, more_match_data)
                db_connect.commit()
                found = 1
                #print minsum
    if found==3:
        dropdown.append("<option value=\"%s\">%s</option>" %(whiskeyName,whiskeyName))
######################### BACKUP DIFF METHOD

for i in sorted(dropdown):
    print i

