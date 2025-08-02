import pygame
import random
from pygame import mixer
import json
import random
import time
import requests
import os
import sys
from cryptography.fernet import Fernet

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # Extracted temp folder used by PyInstaller
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#encryption key
key_path = resource_path("asset/leaderboard_asset/encryption/key.key")
with open(key_path, "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

#open file and choose word and allowed words
word_file_path = resource_path("asset/words_asset/words_file.json")
with open(word_file_path, "r", encoding="utf8") as word_file:
    word_list = json.load(word_file)
random_num=random.randint(0,len(word_list)-1)
chosen_word=word_list[random_num]["word"]
word_score=word_list[random_num]["score"]
word_chars=list(chosen_word)

#open leaderboard file
encrypted_data_path=resource_path("asset/leaderboard_asset/leaderboard_data.enc")
with open(encrypted_data_path, "rb") as leaderboard_file:
    encrypted_data = leaderboard_file.read()
decrypted_data = fernet.decrypt(encrypted_data)
decrypted_string=decrypted_data.decode("utf-8")
username_score_list = json.loads(decrypted_string)

def reroll_word():
    global word_chars,chosen_word,word_score
    random_num=random.randint(0,len(word_list)-1)
    chosen_word=word_list[random_num]["word"]
    word_score=word_list[random_num]["score"]
    word_chars=list(chosen_word)

just_word_list_path=resource_path("asset/words_asset/just_words_file.json")
with open(just_word_list_path,"r",encoding="utf8") as file1:
    just_word_list = json.load(file1)

# initialize the pygame
pygame.init()
clock = pygame.time.Clock()
fps=30

#title and icon
pygame.display.set_caption("Word Quest")
icon_path = resource_path('asset/game_image/app_icon/icon.png')
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

#create the screen((dimension))
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height-60))

#background
background_path=resource_path("asset/game_image/background/template.png")
background = pygame.image.load(background_path)
shade_path=resource_path("asset/game_image/background/background_shade.png")
shade= pygame.image.load(shade_path)

#background sound
def random_bg_music():
    a=resource_path("asset/game_music/Beethoven - Moonlight Sonata 1st Movement.mp3")
    b=resource_path("asset/game_music/Fallen Down reprise on Old Slightly Out-Of-Tune Piano.mp3")
    bg_random_num=random.randint(1,2)
    if bg_random_num==1:
        return a
    if bg_random_num==2:
        return b
bg_music=random_bg_music()
mixer.music.load(bg_music)
mixer.music.play(-1)#means play on loop

#button
button_path=resource_path("asset/game_image/button/guess_button.png")
button = pygame.image.load(button_path)
button_activated_path=resource_path("asset/game_image/button/guess_button_activated.png")
button_activated = pygame.image.load(button_activated_path)
button_pos = (682, 670)
button_rect = pygame.Rect(button_pos, button.get_size())
mouse_click_status=False

#save score button and play again button
play_again_button_path=resource_path("asset/game_image/button/play_again_button.png")
play_again_button = pygame.image.load(play_again_button_path)
play_again_button_acticated_path=resource_path("asset/game_image/button/play_again_button_activated.png")
play_again_button_activated = pygame.image.load(play_again_button_acticated_path)
play_again_button_pos = (511 , 430)
play_again_button_rect = pygame.Rect(play_again_button_pos, play_again_button.get_size())

save_score_button_path=resource_path("asset/game_image/button/save_score_button.png")
save_score_button = pygame.image.load(save_score_button_path)
save_score_button_activated_path=resource_path("asset/game_image/button/save_score_button_activated.png")
save_score_button_activated = pygame.image.load(save_score_button_activated_path)
save_score_button_pos = (811 , 430)
save_score_button_rect = pygame.Rect(save_score_button_pos, save_score_button.get_size())

#round
round=0
guess_x_pos_factor=147#in the loop add first gap and (time the position of letter in list with this factor )
guess_y_pos_factor=93#in the loop add 133 and (time the position of letter in list with this factor )
#first guess
first_guess=[]
#second guess
second_guess=[]
#third guess
third_guess=[]
#fourth guess
fourth_guess=[]
#fifth guess
fifth_guess=[]
#sixth guess
sixth_guess=[]

#past_chosen_word
past_chosen_word=[]

#font
keyboard_press_status=False
A = pygame.image.load(resource_path("asset/game_image/font/font_A.png"))
B = pygame.image.load(resource_path("asset/game_image/font/font_B.png"))
C = pygame.image.load(resource_path("asset/game_image/font/font_C.png"))
D = pygame.image.load(resource_path("asset/game_image/font/font_D.png"))
E = pygame.image.load(resource_path("asset/game_image/font/font_E.png"))
F = pygame.image.load(resource_path("asset/game_image/font/font_F.png"))
G = pygame.image.load(resource_path("asset/game_image/font/font_G.png"))
H = pygame.image.load(resource_path("asset/game_image/font/font_H.png"))
I = pygame.image.load(resource_path("asset/game_image/font/font_I.png"))
J = pygame.image.load(resource_path("asset/game_image/font/font_J.png"))
K = pygame.image.load(resource_path("asset/game_image/font/font_K.png"))
L = pygame.image.load(resource_path("asset/game_image/font/font_L.png"))
M = pygame.image.load(resource_path("asset/game_image/font/font_M.png"))
N = pygame.image.load(resource_path("asset/game_image/font/font_N.png"))
O = pygame.image.load(resource_path("asset/game_image/font/font_O.png"))
P = pygame.image.load(resource_path("asset/game_image/font/font_P.png"))
Q = pygame.image.load(resource_path("asset/game_image/font/font_Q.png"))
R = pygame.image.load(resource_path("asset/game_image/font/font_R.png"))
S = pygame.image.load(resource_path("asset/game_image/font/font_S.png"))
T = pygame.image.load(resource_path("asset/game_image/font/font_T.png"))
U = pygame.image.load(resource_path("asset/game_image/font/font_U.png"))
V = pygame.image.load(resource_path("asset/game_image/font/font_V.png"))
W = pygame.image.load(resource_path("asset/game_image/font/font_W.png"))
X = pygame.image.load(resource_path("asset/game_image/font/font_X.png"))
Y = pygame.image.load(resource_path("asset/game_image/font/font_Y.png"))
Z = pygame.image.load(resource_path("asset/game_image/font/font_Z.png"))

def return_font(char):
    if char == "a":
        return A 
    if char == "b":
        return B 
    if char == "c":
        return C 
    if char == "d":
        return D 
    if char == "e":
        return E 
    if char == "f":
        return F 
    if char == "g":
        return G 
    if char == "h":
        return H 
    if char == "i":
        return I 
    if char == "j":
        return J 
    if char == "k":
        return K 
    if char == "l":
        return L 
    if char == "m":
        return M 
    if char == "n":
        return N 
    if char == "o":
        return O 
    if char == "p":
        return P 
    if char == "q":
        return Q 
    if char == "r":
        return R 
    if char == "s":
        return S 
    if char == "t":
        return T 
    if char == "u":
        return U 
    if char == "v":
        return V 
    if char == "w":
        return W
    if char == "x":
        return X 
    if char == "y":
        return Y 
    if char == "z":
        return Z 
    


#game function for event
buffer_string=[]
def buffer_char(x):
    if round==0 and len(first_guess)<5:
        first_guess.append(x)
    if round==1 and len(second_guess)<5:
        second_guess.append(x)
    if round==2 and len(third_guess)<5:
        third_guess.append(x)
    if round==3 and len(fourth_guess)<5:
        fourth_guess.append(x)
    if round==4 and len(fifth_guess)<5:
        fifth_guess.append(x)
    if round==5 and len(sixth_guess)<5:
        sixth_guess.append(x)
    if len(buffer_string)<5:
        buffer_string.append(x)
    keyboard_Sound_path=resource_path("asset/game_music/click-345983.mp3")
    keyboard_Sound = mixer.Sound(keyboard_Sound_path)
    keyboard_Sound.play()

def delete_char():
    if round==0 and len(first_guess)>0:
        del first_guess[len(first_guess)-1]
    if round==1 and len(second_guess)>0:
        del second_guess[len(second_guess)-1]
    if round==2 and len(third_guess)>0:
        del third_guess[len(third_guess)-1]
    if round==3 and len(fourth_guess)>0:
        del fourth_guess[len(fourth_guess)-1]
    if round==4 and len(fifth_guess)>0:
        del fifth_guess[len(fifth_guess)-1]
    if round==5 and len(sixth_guess)>0:
        del sixth_guess[len(sixth_guess)-1]
    if len(buffer_string)>0:
        del buffer_string[len(buffer_string)-1]
    keyboard_Sound_path=resource_path("asset/game_music/click-345983.mp3")
    keyboard_Sound = mixer.Sound(keyboard_Sound_path)
    keyboard_Sound.play()
    
def length_current_round_guess(num):
    if num==0:
        return len(first_guess)
    if num==1:
        return len(second_guess)
    if num==2:
        return len(third_guess)
    if num==3:
        return len(fourth_guess)
    if num==4:
        return len(fifth_guess)
    if num==5:
        return len(sixth_guess)
    
guess_accuracy=[]
first_guess_accuracy=[]
second_guess_accuracy=[]
third_guess_accuracy=[]
fourth_guess_accuracy=[]
fifth_guess_accuracy=[]
sixth_guess_accuracy=[]
green_path=resource_path("asset/game_image/guess_accuracy_bg/green.png")
green= pygame.image.load(green_path)
yellow_path=resource_path("asset/game_image/guess_accuracy_bg/yellow.png")
yellow= pygame.image.load(yellow_path)
red_path=resource_path("asset/game_image/guess_accuracy_bg/red.png")
red= pygame.image.load(red_path)
def guess_check(buffer):
    for i in range(0,5):
        if buffer[i]==word_chars[i]:
            guess_accuracy.append("green")
        elif buffer[i] in word_chars:
            guess_accuracy.append("yellow")
        else:
            guess_accuracy.append("red")
    if round==0:
        global first_guess_accuracy
        first_guess_accuracy=guess_accuracy
    elif round==1:
        global second_guess_accuracy
        second_guess_accuracy=guess_accuracy
    elif round==2:
        global third_guess_accuracy
        third_guess_accuracy=guess_accuracy
    elif round==3:
        global fourth_guess_accuracy
        fourth_guess_accuracy=guess_accuracy
    elif round==4:
        global fifth_guess_accuracy
        fifth_guess_accuracy=guess_accuracy
    elif round==5:
        global sixth_guess_accuracy
        sixth_guess_accuracy=guess_accuracy
    ring_Sound_path=resource_path("asset/game_music/alert-sound-230091.mp3")
    ring_Sound = mixer.Sound(ring_Sound_path)
    ring_Sound.play()

def return_color(color_name):
    if color_name == "green":
        return green 
    if color_name == "yellow":
        return yellow
    if color_name == "red":
        return red

#reset when continue next round
def reset():
    global game_state,guess_accuracy, first_guess_accuracy,second_guess_accuracy,third_guess_accuracy,fourth_guess_accuracy,fifth_guess_accuracy,sixth_guess_accuracy,buffer_string,first_guess,second_guess,third_guess,fourth_guess,fifth_guess,sixth_guess,round
    guess_accuracy=[]
    first_guess_accuracy=[]
    second_guess_accuracy=[]
    third_guess_accuracy=[]
    fourth_guess_accuracy=[]
    fifth_guess_accuracy=[]
    sixth_guess_accuracy=[]
    buffer_string=[]
    first_guess=[]
    second_guess=[]
    third_guess=[]
    fourth_guess=[]
    fifth_guess=[]
    sixth_guess=[]
    round=0
    reroll_word()

score_value=0
def eval_score(given_word_score):
    global score_value
    value=int(100-(given_word_score/1000))
    score_value+=value

def reset_score():
    global score_value,chosen_word
    score_value,chosen_word=0,0

def show_score(x,y):
    font = pygame.font.Font("freesansbold.ttf",50)
    score = font.render("Score :"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

#show leaderboard function
def show_on_screen(element,x,y):
    screen.blit(element,(x,y))

#sort the leaderboard
def leaderboard_sort_desc(list_with_dic):
    length=len(list_with_dic)
    for i in range(0,length-1):
        for j in range(i+1,length):
            if list_with_dic[i]["score"]<list_with_dic[j]["score"]:
                temp=list_with_dic[i]
                list_with_dic[i]=list_with_dic[j]
                list_with_dic[j]=temp

def get_clue(word):
    try:
        url= "https://api.dictionaryapi.dev/api/v2/entries/en/"+word
        response = requests.get(url)
        word_json=response.json()
        word_definition=word_json[0]["meanings"][0]["definitions"][0]["definition"]
        return word_definition
    except Exception:
        return "None"
clue=get_clue(chosen_word)

#overflow for clue
clue_box_rect = pygame.Rect(1276 , 550 , 198, 167)  # (x, y, width, height)
clue_surface = pygame.Surface((clue_box_rect.width, clue_box_rect.height))
def render_multiline_text(text, font, color, surface):
    words = text.split(" ")
    space_width = font.size(" ")[0]
    x, y = 0, 0
    max_width = surface.get_width()

    for word in words:
        word_surface = font.render(word, True, color)
        word_width, word_height = word_surface.get_size()

        if x + word_width >= max_width:
            x = 0
            y += word_height
            if y + word_height > surface.get_height():
                break  # Clip overflow vertically

        surface.blit(word_surface, (x, y))
        x += word_width + space_width
font = pygame.font.Font("freesansbold.ttf", 30)
render_multiline_text(clue, font, (192, 192, 192), clue_surface)

def get_username_input(screen, font):
    import pygame
    import sys

    input_box = pygame.Rect(881, 575, 200, 50)
    color_active = pygame.Color((255,255,255))
    color = color_active
    active = True
    text = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    for n in range(120):
                        label_saved = font.render("SAVED!", True, (255, 255, 255))
                        screen.blit(label_saved, ((input_box.x-185, input_box.y+60)))
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif len(text) < 8 and event.unicode.isprintable():
                    text += event.unicode

        # Render typed text
        txt_surface = font.render(text, True, (255,255 , 255))
        input_box.w = max(200, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Optional label
        label_surface = font.render("Enter Username(max 8):", True, (255, 255, 255))
        screen.blit(label_surface, (input_box.x-420, input_box.y+5))

        pygame.display.update()

round=0
game_start=True
#game loop
while game_start:

    # Get mouse position and click status
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    
    #background color(screen continues continously so in loop)
    screen.blit(background,(0,0))

    # Hover effect
    if button_rect.collidepoint(mouse_pos):
        screen.blit(button_activated,button_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and not mouse_click_status:
            if event.button == 1 and length_current_round_guess(round)==5 and ''.join(buffer_string) in just_word_list:
                guess_check(buffer_string)
                round+=1
                buffer_string=[]
                guess_accuracy=[]
                mouse_click_status=True

        if event.type == pygame.MOUSEBUTTONUP and mouse_click_status:
            if event.button == 1:
                keyboard_Sound_path=resource_path("asset/game_music/click-345983.mp3")
                keyboard_Sound = mixer.Sound(keyboard_Sound_path)
                keyboard_Sound.play()
                mouse_click_status=False
    else:
        screen.blit(button,button_pos)
    
    
    #main game event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            game_start=False
        
        #if keystroke is pressed(a-z) [skip to line 212]
        try:
            if event.type ==pygame.KEYDOWN and not keyboard_press_status:
                if event.key == pygame.K_RETURN and length_current_round_guess(round)==5 and ''.join(buffer_string) in just_word_list:
                    guess_check(buffer_string)
                    round+=1
                    buffer_string=[]
                    guess_accuracy=[]
                    keyboard_press_status=True  
                if event.key == pygame.K_a:
                    keyboard_press_status=True   
                    buffer_char("a")
                if event.key == pygame.K_b:
                    keyboard_press_status=True
                    buffer_char("b")
                if event.key == pygame.K_c:
                    keyboard_press_status=True
                    buffer_char("c")
                if event.key == pygame.K_d:
                    keyboard_press_status=True
                    buffer_char("d")
                if event.key == pygame.K_e:
                    keyboard_press_status=True
                    buffer_char("e")
                if event.key == pygame.K_f:
                    keyboard_press_status=True   
                    buffer_char("f")
                if event.key == pygame.K_g:
                    keyboard_press_status=True
                    buffer_char("g")
                if event.key == pygame.K_h:
                    keyboard_press_status=True
                    buffer_char("h")
                if event.key == pygame.K_i:
                    keyboard_press_status=True
                    buffer_char("i")
                if event.key == pygame.K_j:
                    keyboard_press_status=True
                    buffer_char("j")
                if event.key == pygame.K_k:
                    keyboard_press_status=True   
                    buffer_char("k")
                if event.key == pygame.K_l:
                    keyboard_press_status=True
                    buffer_char("l")
                if event.key == pygame.K_m:
                    keyboard_press_status=True
                    buffer_char("m")
                if event.key == pygame.K_n:
                    keyboard_press_status=True
                    buffer_char("n")
                if event.key == pygame.K_o:
                    keyboard_press_status=True
                    buffer_char("o")
                if event.key == pygame.K_p:
                    keyboard_press_status=True   
                    buffer_char("p")
                if event.key == pygame.K_q:
                    keyboard_press_status=True
                    buffer_char("q")
                if event.key == pygame.K_r:
                    keyboard_press_status=True
                    buffer_char("r")
                if event.key == pygame.K_s:
                    keyboard_press_status=True
                    buffer_char("s")
                if event.key == pygame.K_t:
                    keyboard_press_status=True
                    buffer_char("t")
                if event.key == pygame.K_u:
                    keyboard_press_status=True
                    buffer_char("u")
                if event.key == pygame.K_v:
                    keyboard_press_status=True   
                    buffer_char("v")
                if event.key == pygame.K_w:
                    keyboard_press_status=True
                    buffer_char("w")
                if event.key == pygame.K_x:
                    keyboard_press_status=True
                    buffer_char("x")
                if event.key == pygame.K_y:
                    keyboard_press_status=True
                    buffer_char("y")
                if event.key == pygame.K_z:
                    keyboard_press_status=True
                    buffer_char("z")
                if event.key == pygame.K_BACKSPACE:
                    keyboard_press_status=True
                    delete_char()
        except Exception:
            pass
        

        if event.type == pygame.KEYUP and keyboard_press_status:
            if event.key == pygame.K_a or event.key == pygame.K_b or event.key == pygame.K_c or event.key == pygame.K_d or event.key == pygame.K_e or event.key == pygame.K_f or event.key == pygame.K_g or event.key == pygame.K_h or event.key == pygame.K_i or event.key == pygame.K_j or event.key == pygame.K_k or event.key == pygame.K_l or event.key == pygame.K_m or event.key == pygame.K_n or event.key == pygame.K_o or event.key == pygame.K_p or event.key == pygame.K_q or event.key == pygame.K_r or event.key == pygame.K_s or event.key == pygame.K_t or event.key == pygame.K_u or event.key == pygame.K_v or event.key == pygame.K_w or event.key == pygame.K_x or event.key == pygame.K_y or event.key == pygame.K_z or event.key == pygame.K_BACKSPACE:
                keyboard_press_status=False
    
    #guess accuracy color
    for pos in range(0,len(first_guess_accuracy)):
        color=return_color(first_guess_accuracy[pos])
        screen.blit(color,((402+(146*pos)),(118+(93*0))))

    for pos in range(0,len(second_guess_accuracy)):
        color=return_color(second_guess_accuracy[pos])
        screen.blit(color,((402+(146*pos)),(118+(93*1))))

    for pos in range(0,len(third_guess_accuracy)):
        color=return_color(third_guess_accuracy[pos])
        screen.blit(color,((402+(146*pos)),(118+(93*2))))

    for pos in range(0,len(fourth_guess_accuracy)):
        color=return_color(fourth_guess_accuracy[pos])
        screen.blit(color,((402+(146*pos)),(118+(93*3))))
    
    for pos in range(0,len(fifth_guess_accuracy)):
        color=return_color(fifth_guess_accuracy[pos])
        screen.blit(color,((402+(146*pos)),(118+(93*4))))

    for pos in range(0,len(sixth_guess_accuracy)):
        color=return_color(sixth_guess_accuracy[pos])
        screen.blit(color,((402+(146*pos)),(118+(93*5))))
    
    #character 
    for pos in range(0,len(first_guess)):
        char_font=return_font(first_guess[pos])
        screen.blit(char_font,((414+(guess_x_pos_factor*pos)),(133+(guess_y_pos_factor*0))))

    for pos in range(0,len(second_guess)):
        char_font=return_font(second_guess[pos])
        screen.blit(char_font,((414+(guess_x_pos_factor*pos)),(133+(guess_y_pos_factor*1))))

    for pos in range(0,len(third_guess)):
        char_font=return_font(third_guess[pos])
        screen.blit(char_font,((414+(guess_x_pos_factor*pos)),(133+(guess_y_pos_factor*2))))

    for pos in range(0,len(fourth_guess)):
        char_font=return_font(fourth_guess[pos])
        screen.blit(char_font,((414+(guess_x_pos_factor*pos)),(133+(guess_y_pos_factor*3))))
    
    for pos in range(0,len(fifth_guess)):
        char_font=return_font(fifth_guess[pos])
        screen.blit(char_font,((414+(guess_x_pos_factor*pos)),(133+(guess_y_pos_factor*4))))

    for pos in range(0,len(sixth_guess)):
        char_font=return_font(sixth_guess[pos])
        screen.blit(char_font,((414+(guess_x_pos_factor*pos)),(133+(guess_y_pos_factor*5))))

    show_score(10,10)

    #show leaderboard
    for user_index in range(0,len(username_score_list)):
        username=username_score_list[user_index]["username"]
        score=username_score_list[user_index]["score"]
        font = pygame.font.Font("freesansbold.ttf",30)
        score_show = font.render(str(user_index+1)+". "+username+" "+str(score),True,(0,0,0))
        show_on_screen(score_show,80,(user_index*30)+170)
    
    #show past chosen word
    for word_index in range(0,len(past_chosen_word)):
        word=past_chosen_word[word_index]
        font = pygame.font.Font("freesansbold.ttf",30)
        word_show = font.render(word,True,(0,0,0))
        show_on_screen(word_show,1326,(word_index*30)+100)
    
    #show clue
    clue_surface.fill((44, 230, 99))
    font = pygame.font.Font("freesansbold.ttf",20)
    render_multiline_text(clue, font, (0, 0, 0), clue_surface)
    screen.blit(clue_surface, (clue_box_rect.x, clue_box_rect.y))
    
    if first_guess_accuracy==["green"]*5 or second_guess_accuracy==["green"]*5 or third_guess_accuracy==["green"]*5 or fourth_guess_accuracy==["green"]*5 or fifth_guess_accuracy==["green"]*5 or sixth_guess_accuracy==["green"]*5:
        round=6
    if round>5:
        past_chosen_word.append(chosen_word)
        font = pygame.font.Font("freesansbold.ttf",64)
        word_show = font.render("Your Word Was: "+chosen_word,True,(192,192,192))
        rustle_Sound_path=resource_path("asset/game_music/clean-whoosh-effect-382719.mp3")
        rustle_Sound = mixer.Sound(rustle_Sound_path)
        rustle_Sound.play()
        for i in range(300):
            screen.blit(word_show,(416, 370))
            pygame.display.update()
        time.sleep(2)
        #if none is correct by round 7(6), then end game
        wait_status=True
        if first_guess_accuracy!=["green"]*5 and second_guess_accuracy!=["green"]*5 and third_guess_accuracy!=["green"]*5 and fourth_guess_accuracy!=["green"]*5 and fifth_guess_accuracy!=["green"]*5 and sixth_guess_accuracy!=["green"]*5:
            scary_Sound_path=resource_path("asset/game_music/scary-sound-effect-359877.mp3")
            scary_Sound = mixer.Sound(scary_Sound_path)
            scary_Sound.play()
            horror_bakcground_path=resource_path("asset/game_music/horror-background-atmosphere-for-suspense-166944.mp3")
            mixer.music.load(horror_bakcground_path)
            mixer.music.play(-1)
            save_status=False
            while wait_status:
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()
                for event in pygame.event.get():
                    screen.blit(shade,(0,0))
                    screen.blit(word_show,(416, 370))
                    if play_again_button_rect.collidepoint(mouse_pos):
                        screen.blit(play_again_button_activated,play_again_button_pos)
                        if event.type == pygame.MOUSEBUTTONDOWN and not mouse_click_status:
                            if event.button == 1:
                                keyboard_Sound_path=resource_path("asset/game_music/click-345983.mp3")
                                keyboard_Sound = mixer.Sound(keyboard_Sound_path)
                                keyboard_Sound.play()
                                reset_score()
                                mouse_click_status=True
                        if event.type == pygame.MOUSEBUTTONUP and mouse_click_status:
                            if event.button == 1:
                                bg_music=random_bg_music()
                                mixer.music.load(bg_music)
                                mixer.music.play(-1)
                                mouse_click_status=False
                                wait_status=False
                                
                    else:
                        screen.blit(play_again_button,play_again_button_pos)

                    if save_score_button_rect.collidepoint(mouse_pos):
                        screen.blit(save_score_button_activated,save_score_button_pos)
                        if event.type == pygame.MOUSEBUTTONDOWN and not mouse_click_status:
                            if event.button == 1 and not save_status:
                                keyboard_Sound_path=resource_path("asset/game_music/click-345983.mp3")
                                keyboard_Sound = mixer.Sound(keyboard_Sound_path)
                                keyboard_Sound.play()
                                username_overwrite=get_username_input(screen, pygame.font.Font(None, 50))
                                keyboard_Sound = mixer.Sound(keyboard_Sound_path)
                                keyboard_Sound.play()
                                overwritten=False
                                for username_index in range(0,len(username_score_list)):
                                    if username_score_list[username_index]["username"]==username_overwrite and len(list(username_overwrite))<=8:
                                        if username_score_list[username_index]["score"]<score_value:
                                            username_score_list[username_index]["score"]=score_value
                                        overwritten=True
                                    if not overwritten and username_index==len(username_score_list)-1 and len(list(username_overwrite))<=8:
                                        username_score_list.append({"username":username_overwrite,"score":score_value})
                                leaderboard_sort_desc(username_score_list)
                                json_string = json.dumps(username_score_list)
                                overwrite_encrypted_data = fernet.encrypt(json_string.encode("utf-8"))
                                leaderboard_asset_path=resource_path("asset/leaderboard_asset/leaderboard_data.enc")
                                with open(leaderboard_asset_path, "wb") as file_overwrite_leaderboard:
                                    file_overwrite_leaderboard.write(overwrite_encrypted_data)
                                reset_score()
                                mouse_click_status=True
                                save_status=True

                        if event.type == pygame.MOUSEBUTTONUP and mouse_click_status:
                            if event.button == 1:
                                mouse_click_status=False
                                #wait_status=False
                    else:
                        screen.blit(save_score_button,save_score_button_pos)
                    
                    pygame.display.update()
        else:
            eval_score(word_score)
            bg_music=random_bg_music()
            mixer.music.load(bg_music)
            mixer.music.play(-1)
        reset()
        clue=str(get_clue(chosen_word))
        save_status=False

    pygame.display.update()
    clock.tick(fps)