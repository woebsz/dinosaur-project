import requests
from bs4 import BeautifulSoup, Tag, NavigableString
import random

url = 'https://www.nhm.ac.uk/discover/dino-directory/name/name-az-all.html'

meta_url = 'https://www.nhm.ac.uk' 

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
        

def get_all(url_1, url_2):
    
    link_list = []
    req = requests.get(url_1).text
    soup = BeautifulSoup(req, 'html5lib')
    dinosaur_links = soup.find_all('li', {'dinosaurfilter--dinosaur dinosaurfilter--all-list'})
    
    for i in dinosaur_links:
        link_list.append(i.a['href'])
        
    req_f = requests.get(meta_url + link_list[59]).text
    soup_f = BeautifulSoup(req_f, 'html5lib')
    
    print(link_list[13])
    
    dino_name = soup_f.h1.text
    dino_pronunciation = soup_f.find('dd', {'class':'dinosaur--pronunciation'}).text
    dino_meaning = soup_f.find('dd', {'class': 'dinosaur--meaning'}).text
    dino_info = {dino_name:None}
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
    #print(dino_info)
    
    get_keys_and_values(test_2, 0, info_keys, info_values)
    
    dino_i = {dino_name:None}
    my_c = dict(zip(info_keys, info_values))
    dino_i.update({dino_name:my_c})
    
    print(dino_i)
    
    """
    my_result = soup_f.find_all('div', {'class': 'dinosaur--container'})

    for x in my_result[0]:
        print(x)
        print('----')
    """
get_all(url, meta_url)    