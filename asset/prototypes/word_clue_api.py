import requests
try:
    word=str(input("Search Meaning For: "))
    url= "https://api.dictionaryapi.dev/api/v2/entries/en/"+word
    response = requests.get(url)
    word_json=response.json()
    word_definition=word_json[0]["meanings"][0]["definitions"][0]["definition"]
    print(word_definition)
except Exception:
    print("None")


