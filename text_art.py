import subprocess
import random
import pyfiglet

# Text to display
text = "Agentless Hacker"

# All ASCII art and text from the Metasploit theme, Rabbit, Skull, and "I love you" designs
ascii_art_list = [
    # AL Hacker 2
    r'''
               .;lxO0KXXXK0Oxl:.
           ,o0WMMMMMMMMMMMMMMMMMMKd,
        'xNMMMMMMMMMMMMMMMMMMMMMMMMMWx,
      :KMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMK:
    .KMMMMMMMMMMMMMMMWNNNWMMMMMMMMMMMMMMMX,
   lWMMMMMMMMMMMXd:..     ..;dKMMMMMMMMMMMMo
  xMMMMMMMMMMWd.               .oNMMMMMMMMMMk
 oMMMMMMMMMMx.                    dMMMMMMMMMMx
.WMMMMMMMMM:                       :MMMMMMMMMM,
xMMMMMMMMMo                         lMMMMMMMMMO
NMMMMMMMMW                    ,cccccoMMMMMMMMMWlccccc;
MMMMMMMMMX                     ;KMMMMMMMMMMMMMMMMMMX:
NMMMMMMMMW.                      ;KMMMMMMMMMMMMMMX:
xMMMMMMMMMd                        ,0MMMMMMMMMMK;
.WMMMMMMMMMc                         'OMMMMMM0,
 lMMMMMMMMMMk.                         .kMMO'
  dMMMMMMMMMMWd'                         ..
   cWMMMMMMMMMMMNxc'.                ##########
    .0MMMMMMMMMMMMMMMMWc            #+#    #+#
      ;0MMMMMMMMMMMMMMMo.          +:+
        .dNMMMMMMMMMMMMo          +#++:++#+
           'oOWMMMMMMMMo                +:+
               .,cdkO0K;        :+:    :+:                                
                                :::::::+:
                      AL Hacker
    ''',
    # Metasploit ASCII Art
    r'''
         d88888b db    db d88888b d8b   db d888888b d888888b 
         88'     88    88 88'     888o  88   `88'   `~~88~~' 
         88ooooo 88    88 88ooooo 88V8o 88    88       88    
         88~~~~~ 88    88 88~~~~~ 88 V8o88    88       88    
         88.     88b  d88 88.     88  V888   .88.      88    
         Y88888P ~Y8888P' Y88888P VP   V8P Y888888P    YP    
                Agentless Hacker by Rapid7     
    ''',
    # Skull ASCII Art
    r'''
                      ########                  #
                      #################            #
                   ######################         #
                  #########################      #
                ############################
               ##############################
               ###############################
              ###############################
              ##############################
                              #    ########   #
                 ##        ###        ####   ##
                                      ###   ###
                                    ####   ###
               ####          ##########   ####
               #######################   ####
                 ####################   ####
                  ##################  ####
                    ############      ##
                       ########        ###
                      #########        #####
                    ############      ######
                   ########      #########
                     #####       ########
                       ###       #########
                      ######    ############
                     #######################
                     #   #   ###  #   #   ##
                     ########################
                      ##     ##   ##     ##
                            https://Agentless-Hacker.com
    ''',
    # Rabbit ASCII Art
    r'''
                        (`.         ,-,
                        ` `.    ,;' /
                         `.  ,'/ .'
                          `. X /.'
                .-;--''--.._` ` (
              .'            /   `
             ,           ` '   Q '            ======Agentless Hacker======
             ,         ,   `._    \
          ,.|         '     `-.;_'
           ' `    ,   )   .'
              `._ ,  '   /_
                 ; ,''-,;' ``-
                  ``-..__``--`
    ''',
    # I love you ASCII Art
    r'''
IIIIII    dTb.dTb        _.---._
  II     4'  v  'B   .'"".'/|\`.""'.
  II     6.     .P  :  .' / | \ `.  :
  II     'T;. .;P'  '.'  /  |  \  `.'
  II      'T; ;P'    `. /   |   \ .'
IIIIII     'YvP'       `-.__|__.-'

I love shells --egypt @ Agentless-Hacker
    '''
]

# Function to create and display random text art
def generate_text_art(text):
    fonts = pyfiglet.FigletFont.getFonts()
    random_font = random.choice(fonts)
    fig = pyfiglet.Figlet(font=random_font)
    art_text = fig.renderText(text)
    return art_text

# Function to display a random ASCII image
def display_random_ascii_image():
    random_image = random.choice(ascii_art_list)
    print(random_image)

# Generate and display the text art
print(generate_text_art(text))

# Display a random ASCII image below the text
display_random_ascii_image()

# Run system command if user chooses
option = input("Enter y for ipconfig: ")
if option.lower() == 'y':
    subprocess.call("ipconfig")
