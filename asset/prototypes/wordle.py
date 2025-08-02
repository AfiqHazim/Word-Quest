import requests
import random
import time

word_list=[]
just_word_list=[]

word_length=int(input("How many letters word? ... "))
for letter in "abcdefghijklmnopqrstuvwxyz":
    url= "https://api.datamuse.com/words?sp="+letter+"?"*(word_length-1)+"&max=1000"
    response = requests.get(url)
    word_list.extend(response.json())

word_list_length=len(word_list)

for dic in range(0,word_list_length):
    just_word_list.append(word_list[dic]["word"])

print(word_list_length)
print(len(just_word_list))
word=word_list[random.randint(0,word_list_length-1)]["word"]
print("Your word is....","X"*word_length)
print("START")

word_chars = list(word)
guess_accuracy=[]

n=0
while n<word_length and guess_accuracy!=["green"]*word_length:
    try:
        input_guess=input()
        if input_guess.isdigit() or len(list(input_guess))!=word_length or input_guess not in just_word_list:
            print("Enter a",word_length,"letter guess!")
        else:
            guess_chars=list(input_guess)

            guess_accuracy=[]

            for i in range(0,word_length):
                if guess_chars[i]==word_chars[i]:
                    guess_accuracy.append("green")
                elif guess_chars[i] in word_chars:
                    guess_accuracy.append("yellow")
                else:
                    guess_accuracy.append("red")

            print(guess_accuracy)
            n+=1
    except Exception:
        print("Enter a",word_length,"letter guess!")

print("Your word is....", end=" ", flush=True)
time.sleep(1.5)
print(word)

