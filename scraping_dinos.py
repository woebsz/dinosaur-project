import requests
from bs4 import BeautifulSoup, Tag, NavigableString
import random
import pandas as pd

url = 'https://www.nhm.ac.uk/discover/dino-directory/name/name-az-all.html'

meta_url = 'https://www.nhm.ac.uk' 

html_list = []

def get_keys_and_values(sentence, iterator, x, y):
    for i in sentence:
        if isinstance(i, Tag) and iterator % 2 == 0:
            x.append(i.text.split(':')[0].lower().replace(' ', '_'))
            iterator += 1
        elif isinstance(i, Tag) and iterator % 2 == 1:
            temp = i.text.lstrip().lower().replace('\t', '').replace('\n', '')
            if ',' in temp:
                temp_l = [temp.split(',')]
                for i in temp_l:
                    temp_ll = []
                    for k in i:
                        temp_ll.append(k.lstrip())
    
                y.append(temp_ll)            
            else:
                temp = temp.replace(' ','_')
                y.append(temp)
            
            
            #y.append(i.text.lstrip().lower().replace(' ','_').replace('\t', '').replace('\n', ''))
            iterator += 1

        else:
            pass
        

def get_all(url_1, dino_html):
    
    req = requests.get(url_1).text
    soup = BeautifulSoup(req, 'html5lib')
    dinosaur_links = soup.find_all('li', {'dinosaurfilter--dinosaur dinosaurfilter--all-list'})
    
    for i in dinosaur_links:
        html_list.append(i.a['href'])
        
get_all(url, html_list)      

dino_info = {}   

for i in html_list:
        
    req_f = requests.get(meta_url + i).text
    soup_f = BeautifulSoup(req_f, 'html5lib')
    
    
    dino_name = soup_f.h1.text
    dino_pronunciation = soup_f.find('dd', {'class':'dinosaur--pronunciation'}).text
    dino_meaning = soup_f.find('dd', {'class': 'dinosaur--meaning'}).text
    dino_diet = soup_f.find('dl', {'class': 'dinosaur--info dinosaur--list'}).dd.text
    dino_when_it_lived = dino_diet = soup_f.find('dl', {'class': 'dinosaur--info dinosaur--list'}).dd.find_next('dd').text
    
    test = soup_f.find('dl', {'class': 'dinosaur--description dinosaur--list'})
    test_2 = soup_f.find('dl', {'class': 'dinosaur--info dinosaur--list'})
    
    description_keys = []
    description_values = []
    
    info_keys = []
    info_values = []
    
    get_keys_and_values(test, 0, description_keys, description_values)

    my_d = dict(zip(description_keys, description_values))
    dino_info.update({dino_name:my_d})
    
    get_keys_and_values(test_2, 0, info_keys, info_values)
    
    my_c = dict(zip(info_keys, info_values))
    dino_info.update({dino_name:my_c})
    
    if html_list.index(i) % 10 == 0:
        print(dino_name, str(html_list.index(i)) + '/' + str(len(html_list)))
    elif html_list.index(i) == len(html_list) - 1:
        print('Completed.')
    else:
        pass
df = pd.DataFrame.from_dict(dino_info, orient='index')
df.drop(['teeth', 'food', 'how_it_moved'], axis = 1, inplace=True)
df.dropna(inplace=True)
df = df.reset_index().rename(columns={'index': 'name'})
for i, k in df.iterrows():
    if isinstance(k['when_it_lived'], list) == False:
        df.drop(i, inplace=True)
df_t = pd.DataFrame(df['when_it_lived'].to_list(), columns=['epoch', 'years ago'])
result = pd.concat([df, df_t], axis=1)
result.drop('when_it_lived', axis=1, inplace=True)

print(result.head())        