import subprocess
import pyfiglet
import random
import pyfiglet
from art import text2art
from termcolor import colored
from colorama import Fore, Style
from rich.console import Console

# Initialize Colorama
from colorama import init
init(autoreset=True)

console = Console()

def pyfiglet_art():
    """Generate text art using pyfiglet."""
    fonts = pyfiglet.FigletFont.getFonts()
    font = random.choice(fonts)
    return pyfiglet.figlet_format("Agentless Hacker", font=font)

def art_library():
    """Generate text art using the art library."""
    return text2art("Agentless Hacker")

def termcolor_art():
    """Generate colored text using termcolor."""
    return colored('Agentless Hacker', 'green', 'on_red')

def colorama_art():
    """Generate colored text using colorama."""
    return f"{Fore.CYAN}Agentless Hacker{Style.RESET_ALL}"

def rich_art():
    """Generate styled text using rich."""
    return "[bold magenta]Agentless Hacker[/bold magenta]"

# List of functions for random selection
art_functions = [pyfiglet_art, art_library, termcolor_art, colorama_art, rich_art]

# Select and execute a random text art function
selected_art_function = random.choice(art_functions)
art_output = selected_art_function()

# Display the result
if selected_art_function == rich_art:
    console.print(art_output)
else:
    print(art_output)

option=print(input("Enter y for ipconfig"))
if(option=="y"or"Y"):
    subprocess.call("ipconfig")

