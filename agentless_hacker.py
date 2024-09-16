import subprocess
import pyfiglet
text=pyfiglet.figlet_format("Agentless Hacker")
print(text)
option=print(input("Enter y for ipconfig"))
if(option=="y"or"Y"):
    subprocess.call("ipconfig")
print("thank you")
