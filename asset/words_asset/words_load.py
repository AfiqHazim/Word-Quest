import json
import requests

word_list=[]
just_word_list=[]

for letter in "abcdefghijklmnopqrstuvwxyz":
    url= "https://api.datamuse.com/words?sp="+letter+"?"*(4)+"&max=1000"
    response = requests.get(url)
    word_list.extend(response.json())

word_list_length=len(word_list)

for dic in range(0,word_list_length):
    if word_list[dic]["score"]>=5021:
        just_word_list.append(word_list[dic])


with open("words_file.json","w",encoding="utf8") as file:
    json.dump(just_word_list,file, ensure_ascii=False)