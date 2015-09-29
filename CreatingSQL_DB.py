# coding: utf-8

import json 
import numpy as np
import pymysql as mdb
import pandas as pd


with open('WhiskeyStructureUpdated.json') as data_file:  #categories, notes, strength, categories vector, notes vector
    dataW = json.load(data_file)

data_file.close()
sql = True



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
cursor.execute("""
DROP TABLE whiskey_info
""")

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
        name = str(dataW[i]['name'])
        image = str(dataW[i]['image'])
        notes = str(dataW[i]['notes'])
        categories = str(dataW[i]['note categories'])
        strength =  str(dataW[i]['strength'])

        whiskey_data = (name,notes,categories,image,strength) +tuple(dataW[i]['category vector'][n] for n in range(len(dataW[i]['category vector'])))
        if sql:
            cursor.execute(add_whiskey, whiskey_data)
            db_connect.commit()
    except:
        1+1
        
        
###   cigars

with open('CigarStructureUpdated.json') as data_file:
    dataC = json.load(data_file)

data_file.close()



cursor.execute('USE ViceMatchUpdated')
cursor.execute("""
DROP TABLE cigar_info
""")

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
    name = str(dataC[i]['name'])
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

cursor.execute("""
    DROP TABLE Vmatch
    """)

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
                    'wood':['cedar','cedary','oak','smoky','wood','woody','woodsy','woodiness'],
                    'spice':['spice','spiciness','spicy','spices','anice','licorice','cardamon','nutmeg','pepper','peppery','cinnamon','clove','cloves','cumin','cayenne','chili','allspice'],
                    'earth':['barnyard','earth','earthy','earthy/peaty','earthiness'],
                    'mineral':['lead','graphite','mineral','musk','musty','salt','salty','saltiness','savory'],
                    'fruits':['Watermelon','peach','currant','fruity','fruit','mango','pineapple','apple','raisin','plum','cherry','cherries','berry','orange','zest','citrus','lemon'],
                    'nuts':['walnut','peanut','marzipan','cashew','almond','nut','nuts','nuttiness','nutty','hazelnut','praline'],
                    'feint':['leather','leathery','honey','beewax','cream','mead'],
                    'chocolate':['cocoa','chocolate','chocolately','chocolaty','cream','butter','milky','creamy','creaminess'],
                    'coffee':['espresso','coffee/mocha','coffee','mocha','roasted'],
                    'vanilla':['caramel','custard','toffee','butterscotch'],
                    'cereal':['bran','bread','oat','barley','yeasty','husky']}


lensC = [len(categories_notes[NoteCategories[i]])for i in range(len(NoteCategories))]

data_matched ={}
k=0

for w in dataW.keys():
    whiskey = dataW[w]
    for c in dataC.keys():
        le=0
        cigar = dataC[c]
        strngth = float(np.dot(dataW[w]['strength vector'],dataC[c]['strength vector']))
        if strngth !=0:
            data_matched[str(k)] = {}        
            data_matched[str(k)]['whiskeyName'] = str(whiskey['name'])
            data_matched[str(k)]['cigarName'] = str(cigar['name'])
            highestM = 0
            cosCat = []
            for lnC in range(len(lensC)):
                lb = le
                le = lb+lensC[lnC]
                C_n = dataC[c]['note vector'][lb:le]
                W_n = dataW[w]['note vector'][lb:le]
                try:
                    data_matched[str(k)][NoteCategories[lnC]] = round(float(np.dot(W_n,C_n))/np.sqrt((np.dot(C_n,C_n)*np.dot(W_n,W_n))),2)
                    if float(np.dot(W_n,C_n))/(max(C_n)*max(W_n))>highestM:
                        highestM = float(np.dot(W_n,C_n))/np.sqrt((np.dot(C_n,C_n)*np.dot(W_n,W_n)))
                    cosCat.append(round(float(np.dot(W_n,C_n))/np.sqrt((np.dot(C_n,C_n)*np.dot(W_n,W_n))),2))
                except:
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





pdW = pd.DataFrame(Vmatchd)
pdW = pdW.transpose()



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
    if Vmatchd[m]['highestMatch']<0.1: #0.62 for all combnies (47 ones)
        del Vmatchd[m]



pdW = pd.DataFrame(Vmatchd)
pdW = pdW.transpose()



for i in dataW.keys():
    whiskeyName = i
    pd_sp = pdW[pdW.whiskeyName == i]

    try:
        pd_BM = pd_sp[pd_sp['overallMatch']*pd_sp['catVecMatch'] == max(pd_sp['overallMatch']*pd_sp['catVecMatch'])]
        cigarName = pd_BM['cigarName'][0]
        matchScore = pd_BM['highestMatch'][0]
        overallMatch = pd_BM['overallMatch'][0]
        more_match_data = (whiskeyName,cigarName, 'All' ,matchScore,overallMatch)
        cursor.execute(add_more_matches, more_match_data)
        db_connect.commit()


        for cat in dataW[i]['note categories'].split(', '):
                pdTempCat = pd_sp[pd_sp[str(cat)] == pd_sp['highestMatch']]
                minOM = min(pdTempCat['overallMatch'])
                pdCat = pdTempCat[pdTempCat['overallMatch'] == minOM]
                cigarName = pdCat['cigarName'][0]
                matchScore = pdCat['highestMatch'][0]
                overallMatch = pdCat['overallMatch'][0]
                if matchScore !=0:
                    more_match_data = (whiskeyName,cigarName, cat,matchScore,overallMatch)
                    cursor.execute(add_more_matches, more_match_data)
                db_connect.commit()
    except:
        pass
    

