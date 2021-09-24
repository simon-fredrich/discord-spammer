import discord
import random
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from dotenv import load_dotenv
load_dotenv()
import os

client = discord.Client()
token = os.environ.get("token")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ping'):
        for i in range(998):
            await message.channel.send("<@760194276696260639>")

    # Kleine traurige Geschichte
    if message.channel.id == 801470078579245056:
        if 2 == random.randint(0,3):
            animal = ""
            with open("lebewesen.txt", "r") as a_file:
                lines = []
                for line in a_file:
                    lines.append(line)
                animal = lines[random.randint(0, len(lines))-1]

            await message.channel.send("Es war einmal ein "+animal+" auf der Erde. Sie war hübsch. Sie fiel von einem Berg und starb.\n -Ende-")

    # IdleMiner Statistik :D
    if message.content.startswith('$scan'):
        data = pd.DataFrame(columns=['content', 'time', 'author'])
        def is_command (msg): # Checking if the message is a command call
            if len(msg.content) == 0:
                return False
            elif msg.content.split()[0] == '$scan':
                return True
            else:
                return False

        limit = 5000
        counter = 0
        general = []
        u200b = []

        async for msg in message.channel.history(limit=limit): # As an example, I've set the limit to 500
            if msg.author is not client.user:                        # meaning it'll read 500 messages instead of           
                if not is_command(msg):    
                    embeds = [embed.to_dict() for embed in msg.embeds] 
                    if len(embeds) > 0 and ("fields" in embeds[0]):
                        # print(embeds[0]["fields"])
                        fields = embeds[0]["fields"]
                        if sort_fields_general(fields) != None:
                            general.append(sort_fields_general(fields))

                        if fields[0]["name"]=="**General**":
                            u200b.append((sort_fields_u200b(fields), connect_date_day(embeds)))

                        data = data.append({'content': (fields, msg.content),
                                            'time': msg.created_at,
                                            'author': msg.author.name}, ignore_index=True)
                    # print(counter)
                    counter = counter + 1
                    
                if len(data) == limit:
                    break

        general = general[::-1]
        money = []
        level = []
        blocks_brocken = []
        prestige = []
        for i in general:
            money.append(i[0])
            level.append(i[1])
            blocks_brocken.append(i[2])
            prestige.append(i[3])

        u200b = u200b[::-1]
        shards = []
        rebirths = []
        dimension = []
        tokens = []
        rebirths_per_day_complete =  []
        rebirths_per_day = [0, 0, 0, 0, 0, 0, 0]
        rebirth_count = [0, 0, 0, 0, 0, 0, 0]
        for i in u200b:
            if i[0] != None:
                shards.append(i[0][0])
                rebirths.append(i[0][1])
                dimension.append(i[0][2])
                tokens.append(i[0][3])
                rebirths_per_day_complete.append(i[0][4])
                if i[1] == "Montag":
                    rebirths_per_day[0] = rebirths_per_day[0] + i[0][4]
                    rebirth_count[0] = rebirth_count[0] + 1
                if i[1] == "Dienstag":
                    rebirths_per_day[1] = rebirths_per_day[1] + i[0][4]
                    rebirth_count[1] = rebirth_count[1] + 1
                if i[1] == "Mittwoch":
                    rebirths_per_day[2] = rebirths_per_day[2] + i[0][4]
                    rebirth_count[2] = rebirth_count[2] + 1
                if i[1] == "Donnerstag":
                    rebirths_per_day[3] = rebirths_per_day[3] + i[0][4]
                    rebirth_count[3] = rebirth_count[3] + 1
                if i[1] == "Freitag":
                    rebirths_per_day[4] = rebirths_per_day[4] + i[0][4]
                    rebirth_count[4] = rebirth_count[4] + 1
                if i[1] == "Samstag":
                    rebirths_per_day[5] = rebirths_per_day[5] + i[0][4]
                    rebirth_count[5] = rebirth_count[5] + 1
                if i[1] == "Sonntag":
                    rebirths_per_day[6] = rebirths_per_day[6] + i[0][4]
                    rebirth_count[6] = rebirth_count[6] + 1
            
        rebirths_per_day[0] = rebirths_per_day[0] / rebirth_count[0]
        rebirths_per_day[1] = rebirths_per_day[1] / rebirth_count[1]
        rebirths_per_day[2] = rebirths_per_day[2] / rebirth_count[2]
        rebirths_per_day[3] = rebirths_per_day[3] / rebirth_count[3]
        rebirths_per_day[4] = rebirths_per_day[4] / rebirth_count[4]
        rebirths_per_day[5] = rebirths_per_day[5] / rebirth_count[5]
        rebirths_per_day[6] = rebirths_per_day[6] / rebirth_count[6]

        fig, axs = plt.subplots(3,3)
        fig.suptitle("Idle-Miner: SnowMarvel Statistiken")
        axs[0][0].plot(range(0, len(shards)), shards)
        axs[0][0].set_title("Shards")
        axs[1][0].step(["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"], rebirths_per_day, color="red")
        axs[1][0].set_title("Rebirths per day")
        axs[2][0].plot(range(0, len(money)), money, color="green")
        axs[2][0].set_title("Money")

        axs[0][1].plot(range(0, len(level)), level, color="peachpuff")
        axs[0][1].set_title("Level")
        axs[1][1].plot(range(0, len(blocks_brocken)), blocks_brocken, color="teal")
        axs[1][1].set_title("Blocks Brocken")
        axs[2][1].plot(range(0, len(prestige)), prestige, color="plum")
        axs[2][1].set_title("Prestige")

        axs[0][2].plot(range(0, len(rebirths)), rebirths, color="skyblue")
        axs[0][2].set_title("Rebirths")
        axs[1][2].plot(range(0, len(tokens)), tokens, color="gold")
        axs[1][2].set_title("Tokens")

        x1 = np.arange(0,4*np.pi,0.1)   # start,stop,step
        y1 = np.sin(x1)
        x2 = np.arange(0,4*np.pi,0.1)   # start,stop,step
        y2 = np.sin(x2+1)
        x3 = np.arange(0,4*np.pi,0.1)   # start,stop,step
        y3 = np.sin(x3+2)
        x4 = np.arange(0,4*np.pi,0.1)   # start,stop,step
        y4 = np.sin(x4+3)
        x5 = np.arange(0,4*np.pi,0.1)   # start,stop,step
        y5 = np.sin(x5+4)
        x6 = np.arange(0,4*np.pi,0.1)   # start,stop,step
        y6 = np.sin(x6+5)
        axs[2][2].plot(x1, y1, color="midnightblue")
        axs[2][2].plot(x2, y2, color="navy")
        axs[2][2].plot(x3, y3, color="darkblue")
        axs[2][2].plot(x4, y4, color="mediumblue")
        axs[2][2].plot(x5, y5, color="blue")
        axs[2][2].plot(x6, y6, color="slateblue")

        x7 = np.arange(0,4*np.pi,0.1)   # start,stop,step
        y7 = np.sin(x1)
        x8 = np.arange(0,4*np.pi,0.1)   # start,stop,step
        y8 = np.sin(x2+1)
        x9 = np.arange(0,4*np.pi,0.1)   # start,stop,step
        y9 = np.sin(x3+2)

        # axs[2][2].plot(y7, x7, color="lightcoral")
        # axs[2][2].plot(y8, x8, color="indianred")
        # axs[2][2].plot(y9, x9, color="brown")

        axs[2][2].set_title("Sinusspaß")

        plt.show()

        file_location = "pets.csv" # Set the string to where you want the file to be saved to
        data.to_csv(file_location)
        #await message.delete()

def sort_fields_general(fields):
    if fields[0]["name"]=="**General**":
        general = fields[0]["value"]
        pos1 = general.find("**Money:** $")
        pos2 = general.find("**Level:**")
        pos3 = general.find("**Blocks broken:**")
        pos4 = general.find("**Prestige:**")
        pos5 = general.find("**Credits:**")

        if -1 not in (pos1, pos2, pos3, pos4, pos5):
            money = int(general[pos1+len("**Money:** $"):pos2].rstrip("\n").replace(",",""))
            level = int(general[pos2+len("**Level:**"):pos3].rstrip("\n"))
            blocks_brocken = int(general[pos3+len("**Blocks broken:**"):pos4].rstrip("\n").replace(",",""))
            prestige = int(general[pos4+len("**Prestige:**"):pos5].rstrip("\n").replace(",",""))
            credits = general[pos5+len("**Credits:**"):len(general)].rstrip("\n")

            return[money,level,blocks_brocken,prestige,credits]

def sort_fields_u200b(fields):
    u200b = fields[1]["value"]
    pos1 = u200b.find("**Shards:**")
    pos2 = u200b.find("<:shards:")
    pos3 = u200b.find("**Rebirth:**")
    pos4 = u200b.find("**Dimension:**")
    pos5 = u200b.find("**Tokens:**")
    pos6 = u200b.find("<:token:")
    pos7 = u200b.find("**Rebirths/day:**")

    if -1 not in (pos1, pos2, pos3, pos4, pos5, pos6, pos7):
        shards = int(u200b[pos1+len("**Shards:**"):pos2].replace(",",""))
        rebirths = int(u200b[pos3+len("**Rebirth:**"):pos4].rstrip("\n"))
        dimension = u200b[pos4+len("**Dimension:**"):pos5].rstrip("\n")
        tokens = int(u200b[pos5+len("**Tokens:**"):pos6])
        rebirths_per_day = int(u200b[pos7+len("**Rebirths/day:**"):])

        return[shards,rebirths,dimension,tokens,rebirths_per_day]

def connect_date_day(embeds):
    timestamp = embeds[0]["timestamp"].replace("-", "").replace(":", "").replace(".","")
    timestamp = timestamp[:15]+timestamp[21:]
    dt = datetime.datetime.strptime(timestamp, '%Y%m%dT%H%M%S%z')
    day = datetime.date(dt.year, dt.month, dt.day).strftime("%A")
    return day


client.run(token)
