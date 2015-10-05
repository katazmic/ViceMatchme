import numpy as np
import json 
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
import matplotlib.pyplot as plt




def find_features_within_categories(flc,featureDict,categories):
    st = LancasterStemmer()
    words_f = []
    flav_wrds =  word_tokenize(flc)
    for i in flav_wrds:
        try:
            if i.lower() not in words_f:
                words_f.append(i.lower())
            if st.stem(i.lower()) not in words_f:
                    words_f.append(st.stem(i.lower()))  
        except:
            pass   
        
    features = []
    category = []
    catvector  = []
    featurevector = []
    
    
    lensC = [len(featureDict[categories[i]])for i in range(len(categories))]
    icat = 0
    featurevector = []
    for i in categories:
        tempFeat = list(np.zeros(lensC[icat]))
        if len(set(words_f).intersection(featureDict[i])) !=0 :
            features = features + list(set(words_f).intersection(featureDict[i]))
            category.append(i)
            catvector.append(len(set(words_f).intersection(featureDict[i])))
            idx = 0
            for notesC in featureDict[i]:
                if notesC in words_f:
                    tempFeat = [1 if c==1 else c+1./lensC[icat] for c in tempFeat[:idx]] + [1] + [1 if c==1 else c+1./lensC[icat] for c in tempFeat[idx+1:]]                    
                idx = idx+1
                
            featurevector = featurevector+tempFeat             
        else:
            featurevector = featurevector  + tempFeat
            catvector.append(0)
            
            
        icat = icat+1
    return features, category, featurevector, catvector

 


with open('MoM_scraped.json') as mom_file:
    data = json.load(mom_file)

mom_file.close()


name = []
for i in data.keys():
    name.append(i)

    
L = len(data)
for i in range(L):
    if data[name[i]]['Palate'] == 'N/A':
        del data[name[i]]
        
    

fl = []    
for i in  data:
    fl.append(data[i]['Palate']+data[i]['Overall']+data[i]['description'])



# cigar attributes

#sooty, peaty, peat,bonfire, 


#strength = ['refreshing','crisp','clean','fresh','weak','floral','light','grassy','gentle','soft','medium-light','light-medium','mild','balance','gentle','balanced','medium-bodied','medium-body','sherry','sherried','medium-full','round','intense','strong','oily','resinous' ,'thick','voluptuous','bold','big','full-bodied','full-body','heavy','full-body','dense','firm']
categories_strength = {'light' :['refreshing','crisp','clean','fresh','weak','light'],'light-medium':['green','grassy','soft','medium-light','light-medium','mild'], 'medium':['lighter','firm','balance','balanced','medium-bodied','medium-body'], 'medium-full':['sherry','sherried','medium-full','round'],'full':['round','full-bodied','dense','intense','strong','oily','resinous' ,'thick','voluptuous','bold','big','full-body','heavy']}
MainStrengths = ['light','light-medium','medium','medium-full','full']



categories_notes = {'flowers':['tulips','violets','bouquet','flowers','floral','herbaceous','herbal','hay','haylike'], 
                    'plants':['grass','grassy','moss','tea','vegetal'], 
                    'wood':['cedar','cedary','oak','wood','woody','woodsy','woodiness','pine'],
                    'spice':['spice','spiciness','spicy','spices','anice','licorice','cardamon','nutmeg','pepper','peppery','cinnamon','clove','cloves','cumin','cayenne','chili','allspice'],
                    'earth':['barnyard','earth','earthy','earthy/peaty','earthiness','smoke','peat','smoky'],
                    'mineral':['lead','graphite','mineral','musk','musty','salt','salty','saltiness','savory','chalk'],
                    'fruits':['figs','dates','prunes','Watermelon','peach','currant','fruity','fruit','mango','pineapple','apple','raisin','plum','cherry','cherries','berry','orange','zest','citrus','lemon'],
                    'nuts':['walnut','peanut','marzipan','cashew','almond','nut','nuts','nuttiness','nutty','hazelnut','praline'],
                    'feint':['leather','leathery','honey','beewax','mead','molasses'],
                    'chocolate':['mocha','chocolate','chocolately','chocolaty','cream','butter','milky','creamy','creaminess','milk','fudge'],
                    'coffee':['espresso','coffee/mocha','coffee','roasted','cocoa','cappuccino','macchiato'],
                    'vanilla':['caramel','custard','toffee','butterscotch','vanilla'],
                    'cereal':['bran','bread','oat','barley','yeasty','husky','toasted']}

MainNotes = ['wood', 'fruits', 'spice', 'earth', 'nuts', 'cereal', 'chocolate', 'vanilla', 'flowers', 'coffee', 'feint','mineral']

#[len(categories_notes[NoteCategories[i]])for i in range(len(NoteCategories)) ]


# add body! and strength perhaps?! need bigrams! 


fl = []    
for i in data:
    fl.append(data[i]['full notes']+data[i]['description'])
    

notes_list = []
notesV_list = []
notescategory_list = []
notescategoryV_list = []
for i in fl:
    notes, notescategory,notesV,notescategoryV = find_features_within_categories(i,categories_notes,MainNotes)
    notes_list.append(notes)
    notescategory_list.append(notescategory)
    notescategoryV_list.append(notescategoryV)
    notesV_list.append(notesV)

    
fl = []    
for i in  data:
    fl.append(data[i]['Palate']+data[i]['Overall']+data[i]['description'])


strength_list = []
strengthV_list = []
stengthcatergory_list = []
stengthcatergoryV_list = []
for i in fl:
    strengths, strength_category, strengthV,strength_categoryV = find_features_within_categories(i,categories_strength,MainStrengths)
    strength_list.append(strengths)
    stengthcatergory_list.append(strength_category)
    stengthcatergoryV_list.append(strength_categoryV)
    strengthV_list.append(strengthV)

#finds all hte stength notes. 
 
k=0
whiskeyStrength_num = []
whiskeyStrength_body = []
strengthV_list = []
for i in range(len(strength_list)):
    normStrength=[]
    strVec = [1,2,3,4,5]# strength from 1 to 5
    N = sum(stengthcatergoryV_list[i])
    if N != 0:
        for j in stengthcatergoryV_list[i]:
            normStrength.append(float(j)/float(N))
        whiskeyStrength_num.append(np.dot(normStrength,strVec))
        whiskeyStrength_body.append(MainStrengths[int(round(np.dot(normStrength,strVec)))-1])
        strengthV = np.zeros(5)
        strengthV[[int(round(np.dot(normStrength,strVec)))-1]] = 1
        strengthV_list.append(list(strengthV))
    else:
        whiskeyStrength_num.append('N/A')
        whiskeyStrength_body.append('N/A')
        strengthV_list.append('N/A')
        k=k+1
        
        
dataStr = {}
k=0
for i in data:
    if len(notes_list[k]) !=0 and whiskeyStrength_body[k] !='N/A':
        dataStr[i] = {}
        dataStr[i]['name'] = str(i)
        notes = ''
        for nts in notes_list[k]:
            notes = notes + nts
            if nts != notes_list[k][-1]:
                notes = notes + ', '
        dataStr[i]['notes'] = notes
        dataStr[i]['palate'] = data[i]['Palate']
        dataStr[i]['description'] = data[i]['description']
        dataStr[i]['nose'] = data[i]['Nose']
        dataStr[i]['link'] = str(data[i]['link']) 
        dataStr[i]['country'] = data[i]['country']
        dataStr[i]['price'] = data[i]['price']
        dataStr[i]['rating'] = data[i]['rating']
        dataStr[i]['style'] = data[i]['style']
        dataStr[i]['region'] = data[i]['region']
        dataStr[i]['distillery'] = data[i]['distillery']
        dataStr[i]['image'] = str(data[i]['image'])
        categories = ''
        for nts in notescategory_list[k]:
            categories = categories + nts 
            if nts != notescategory_list[k][-1]:
                categories = categories + ', '
        dataStr[i]['note categories'] = categories
        dataStr[i]['note vector'] = notesV_list[k]
        dataStr[i]['category vector'] = notescategoryV_list[k]
        dataStr[i]['strength'] = whiskeyStrength_body[k]
        dataStr[i]['strength vector'] = strengthV_list[k]
    k=k+1

    
dataC = dataStr
with open('WhiskeyStructureUpdated.json', 'w') as ff:
    json.dump(dataStr, ff)
    
ff.close()




#####################################################################


with open('JR_scraped.json') as cig_file:
    data= json.load(cig_file)

cig_file.close()



name = []
for i in data.keys():
    name.append(i.lower())


    
fl = []    
for i in data:
    fl.append(data[i]['MainDescription']+data[i]['description'])


# cigar attributes



# cigar attributes
STRNGTH = ['Mild','Mild - Medium','Medium','Medium - Full','Full']


notes_list = []
notesV_list = []
notescategory_list = []
notescategoryV_list = []
for i in fl:
    notes, notescategory,notesV,notescategoryV = find_features_within_categories(i,categories_notes,MainNotes)
    
    
    notes_list.append(notes)
    notescategory_list.append(notescategory)
    notescategoryV_list.append(notescategoryV)
    notesV_list.append(notesV)
    

dataStr = {}
k=0
for i in data:
    if len(notes_list[k]) !=0 and data[i]['Strength'] in STRNGTH:
        dataStr[i] = {}
        dataStr[i]['name'] = str(i)
        notes = ''
        for nts in notes_list[k]:
            notes = notes + nts
            if nts != notes_list[k][-1]:
                notes = notes + ', '
        dataStr[i]['notes'] = notes
        dataStr[i]['description'] = data[i]['MainDescription']
        dataStr[i]['wrapper type'] = data[i]['WrapperType']
        dataStr[i]['origin'] = data[i]['Origin']
        dataStr[i]['wrapperColor'] = data[i]['WrapperColor']
        dataStr[i]['binder'] = data[i]['Binder']
        dataStr[i]['filler'] = data[i]['Filler']
        dataStr[i]['brand'] = data[i]['brand']
        dataStr[i]['detailed descriptions'] = data[i]['description']
        dataStr[i]['link'] = str(data[i]['link']) 
        dataStr[i]['image'] = str(data[i]['image'])
        categories = ''
        for nts in notescategory_list[k]:
            categories = categories + nts 
            if nts != notescategory_list[k][-1]:
                categories = categories + ', '
        dataStr[i]['note categories'] = categories
        dataStr[i]['note vector'] = notesV_list[k]
        dataStr[i]['category vector'] = notescategoryV_list[k]
        dataStr[i]['strength'] = data[i]['Strength']
        strengthV = np.zeros(5)
        strengthV[STRNGTH.index(data[i]['Strength'])] = 1
        dataStr[i]['strength vector'] = list(strengthV)
        
        
    k=k+1

with open('CigarStructureUpdated.json', 'w') as ff:
    json.dump(dataStr, ff)
    
ff.close()


#with open('JR_CigarStructured.json', 'w') as ff:
#    json.dump(dataStr, ff)


