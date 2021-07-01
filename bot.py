import discord 
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import random
import string

client = commands.Bot(command_prefix=">")
token = 'token'
client.remove_command('help')

with open('storage.json', encoding='utf-8') as f:
  try:
    jobs = json.load(f)
  except ValueError:
    jobs = {}
    jobs['users'] = []

@client.command()
async def help(ctx):
    em = discord.Embed(
        title = "Help",
        color = discord.Color.dark_red()
    )
    em.add_field(name="addjob", value="Run this command to add a new job/bounty to the list [>addjob/aj]",inline=False)
    em.add_field(name="displayavailable", value="Run this command to display all jobs that haven't been done. [>displayavailable/da]",inline=False)
    em.add_field(name="displayfinished", value="Run this command to display all jobs that have been done. [>displayfinished/df]",inline=False)
    em.add_field(name="jobinfo", value="Run this command to only see a single job specified [>jobinfo/ji <Job ID>]",inline=False)
    em.add_field(name="finishjob", value="Run this command to mark a job as finished [>finishjob/fj <Job ID> <USERID or Ping of person that did the job>]",inline=False)
    em.add_field(name="deletejob", value="Run this command to delete a job from the listing, its similar to >finishjob, but it entirely erases it from the database [>deletejob/delj <Job ID>]",inline=False)
    em.add_field(name="editjob", value = "Run this command to edit a part of an existing job. [>editjob/ej <Job ID> <Part you want to edit (tit, des, pri, ava, peo)> <Replacement text for the edit>]")
    em.add_field(name = "rpsbot", value = "Run this command to play Rock Paper Scissors with the bot [>rpsbot]", inline = False)
    await ctx.send(embed = em)


@client.command(aliases=['aj'])
@commands.has_permissions(manage_nicknames = True)
async def addjob(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    #Title
    em = discord.Embed(
        title = "What is the title of the job?",
        color = discord.Color.dark_gold()
    )
    em.set_footer(text="Type 'cancel' to cancel the command")
    await ctx.send(embed = em)
    
    title = str((await client.wait_for('message', check=check)).content)
    if title.lower() == "cancel":
        await ctx.send("Command Cancelled.")
        return
    for job in jobs['jobs']:
        if job['title'].lower() == title.lower():
            await ctx.send("Title is already in use, please re-run the command")
            return
    #Description
    em2 = discord.Embed(
        title = "What is the description of the job?",
        color = discord.Color.dark_gold()
    )
    em2.set_footer(text="Type 'cancel' to cancel the command")
    await ctx.send(embed = em2)

    description = str((await client.wait_for('message', check=check)).content)
    if description.lower() == "cancel":
        await ctx.send("Command Cancelled.")
        return
    
    #Price
    em3 = discord.Embed(
        title = "What is the price of the job? (Must be at least 3,000,000 credits)",
        color = discord.Color.dark_gold()
    )
    em3.set_footer(text="Type 'cancel' to cancel the command")
    await ctx.send(embed = em3)

    price = str((await client.wait_for('message', check=check)).content)
    price = price.replace(',','')
    if price.lower() == "cancel":
        await ctx.send("Command Cancelled.")
        return
    elif int(price) < 3000000:
        await ctx.send("Price is too low, must be above 3,000,000 credits")
        await ctx.send("Command cancelled")
        return
    
    em4 = discord.Embed(
        title = "Difficulty?",
        color = discord.Color.dark_gold()
    )
    em4.set_footer(text = "Choose: Very Easy, Easy, Medium, Hard, Very Hard, Expert. Cancel to cancel")
    await ctx.send(embed = em4)

    difficulty = str((await client.wait_for('message', check=check)).content)
    
    if difficulty.lower() == 'cancel':
        await ctx.send("```Cancelled```")
        return
    #Checking if its acceptable
    await ctx.send("```This is the job:```")
    em5 = discord.Embed(
        title = f"{title}",
        color = discord.Color.red()
    )
    
    """
    Random ID
    """

    char_set = string.ascii_uppercase + string.digits
    random_id = ''.join(random.sample(char_set*6, 6))
    

    for job in jobs['jobs']:
        while job['id'] == random_id:
            char_set = string.ascii_uppercase + string.digits
            random_id = ''.join(random.sample(char_set*6, 6))

    em5.add_field(name = '**Description:**', value = f"{description}", inline=False)
    em5.add_field(name = '**Price:**', value = f"<:credits:647021662662819850> {price}", inline=False)
    em5.add_field(name = "Difficulty", value = difficulty)
    em5.add_field(name = "ID of the Job", value = random_id)
    em5.set_footer(text="Type 'cancel' to cancel adding this job to the job database. Type 'Go ahead' to add it to the database")
    await ctx.send(embed = em5)

    response = str((await client.wait_for('message', check=check)).content)

    if response.lower() == "cancel":
        await ctx.send("Job adding cancelled.")
        return
    if response.lower() == 'go ahead':
        jobs['jobs'].append({
            'title' : title,
            'description' : description,
            'price' : price,
            'availability' : 'available',
            'difficulty' : difficulty.lower(),
            'id' : random_id,
            'people' : "None"
        })
        with open('storage.json','w+') as f:
            json.dump(jobs,f)
        await ctx.send("```Added to database```")
        return
    else:
        await ctx.send("Unknown Response, job adding still cancelled.")


@client.command(aliases=['da'])
async def displayavailable(ctx):
    em = discord.Embed(
        title = f"Available Jobs",
        color = discord.Color.blue()
    )
    for job in jobs['jobs']:
        if job['availability'] == 'available':
            em.add_field(name=f" <:credits:647021662662819850> {job['price']} - {job['id']} - {job['title']} - {job['difficulty']}", value = job['description'], inline=False)
    await ctx.send(embed = em)

@client.command(aliases=['df'])
async def displayfinished(ctx):
    em = discord.Embed(
        title = f"Finished Jobs",
        color = discord.Color.blue()
    )
    for job in jobs['jobs']:
        if job['availability'] == 'not available':
            em.add_field(name=f" <:credits:647021662662819850> {job['price']} - {job['id']} - {job['title']} - {job['difficulty']}", value = job['description'], inline=False)
    await ctx.send(embed = em)


@client.command(aliases=['ji'])
async def jobinfo(ctx, id):
    for job in jobs['jobs']:
        if id.upper() == job['id'].upper():
            em = discord.Embed(
                title = f"Job Title: {job['title']} - {job['id']}",
                color = discord.Color.blue()
            )
            em.add_field(name="Description:", value = job['description'], inline=False)
            em.add_field(name = "Price:", value = f"{job['price']} <:credits:647021662662819850>", inline=False)
            em.add_field(name = "Availability:", value = f"{job['availability']}", inline=False)
            em.add_field(name = "difficulty:", value = f"{job['difficulty']}", inline=False)
            em.add_field(name="People who've done the job:", value="** **", inline=False)
            if job['people'] == "None":
                em.add_field(name="** **", value="None", inline=False)
            else:
                for userid in job['people']:
                    em.add_field(name = "** **", value = f"<@{userid}>", inline=False)
            await ctx.send(embed = em)  
            return

    await ctx.send("```Sorry, can't find the job you were looking for. Try checking your spelling of the job ID```") 
    return



@client.command(aliases=['fj'])
@commands.has_permissions(manage_nicknames = True)
async def finishjob(ctx,id,*,person):
    for char in person:
        if char == "<" or char == "@"  or char == ">" or len(person) == 18:
            removeChar = ["<@!",">"]
            personlist = person.split()
            newpsnlst = []
            for userid in personlist:
                for word in removeChar:
                    userid = userid.replace(word,'')
                newpsnlst.append(int(userid))
            for job in jobs['jobs']:
                if id.upper() == job['id'].upper():
                    job['availability'] = 'not available'
                    job['people'] = newpsnlst
                    with open('storage.json', 'w+') as f:
                        json.dump(jobs,f)
                    await ctx.send("```Job availablity updated```")
                    return
            await ctx.send("```Job not found. Check the spelling of the job ID```")
            return
        else:
            await ctx.send("That is not a valid ping/UserID. Command Cancelled.")
            return


@client.command(aliases=['delj'])
@commands.has_permissions(manage_nicknames = True)
async def deletejob(ctx,id):
    for job in jobs['jobs']:
        if id.upper() == job['id'].upper():
            job['availability'] = 'deleted'
    with open('storage.json', 'w+') as f:
                    json.dump(jobs,f)


@client.command(aliases = ['ej'])
@commands.has_permissions(manage_nicknames = True)
async def editjob(ctx,id,part,*,text):
    dict_part = {
        "tit" : "title",
        "des" : "description",
        "pri" : "price",
        "ava" : "availability",
        "dif" : "difficulty",
        "peo" : "people"
    }
    part_list = ["tit","des","pri","ava","dif","peo"]
    part = part.lower()
    for job in jobs['jobs']:
        if id.upper() == job['id'].upper():
            if part in part_list:
                part = dict_part[part]
            else:
                await ctx.send("```I do not recognize the part in which you want to edit!```")
                return

            #Checking some specifics
            if part == "difficulty" or part == "availability" or part == "title" or part == "description":
                job[part] = text
                with open('storage.json', 'w+') as f:
                    json.dump(jobs,f)
                await ctx.send(f"```Job {part} updated!```")
                return

            elif part == "price":
                text = text.replace(',','')
                if text.isdigit() == False:
                    await ctx.send("```You did not enter a valid number!```")
                    return
                if int(text) < 3000000:
                    await ctx.send("```The price has to be higher than 3 million!```")
                    return
                job["price"] = text
                with open('storage.json', 'w+') as f:
                    json.dump(jobs,f)
                await ctx.send(f"```Job {part} updated!```")
                return 
            
            elif part == "people":
                for char in text:
                    if char == "<" or char == "@"  or char == ">" or len(text) == 18:
                        removeChar = ["<@!",">"]
                        personlist = text.split()
                        newpsnlst = []
                        for userid in personlist:
                            for word in removeChar:
                                userid = userid.replace(word,'')
                            newpsnlst.append(int(userid))
                        job['people'] = newpsnlst
                        with open('storage.json', 'w+') as f:
                            json.dump(jobs,f)
                        await ctx.send(f"```Job {part} updated!```")
                        return
                    else:
                        await ctx.send("```Not a valid user ID or ping!")
                        return


"""
Fun Commands
"""
@client.command()
async def rpsbot(ctx):

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    if True:
        emojidict = {
            "s" : ":scissors:",
            "r" : ":rock:",
            "p" : ":newspaper:"
        }

    
        roundcountem = discord.Embed(
            title = "How many rounds do you want to play for?",
            color = discord.Color.blue()
        )
        roundcountem.set_footer(text = "Choose a number between 1 and 50. You have 10 seconds to respond")
        await ctx.send(embed = roundcountem)
        
        try:
            roundcount = int((await client.wait_for('message', check=check, timeout = 10)).content)
            if isinstance(roundcount,int) == False:
                await ctx.send("You didn't send a number!")
                return
        except:
            await ctx.send("You took too long to respond!")
            return

        playerscore = 0
        computerscore = 0
        roundnumber = 0

        for match in range(1, roundcount + 1):
            computer = random.choice(['r','p','s'])
            roundnumber += 1
            playerchoiceem = discord.Embed(
                title = f"What is your choice? Current round: {roundnumber}",
                color = discord.Color.blue()
            )
            
            playerchoiceem.set_footer(text = f"What's your choice? 'r' for rock, 'p' for paper, 's' for scissors. Send cancel to cancel. You have 10 seconds to respond.")
            await ctx.send(embed = playerchoiceem)
            try:
                playerchoice = str((await client.wait_for('message', check=check,timeout=10)).content)
                if playerchoice is None:
                    await ctx.send("You took too long to respond!")
                    return
            except:
                await ctx.send("```You took too long to respond! The bot has automatically won!```")
                return
            playerchoice = playerchoice.lower()
            if playerchoice == computer:
                await ctx.send(f"Tie!")
                playerscore += 1
                computerscore += 1
            elif (playerchoice == 'r' and computer == 's') or (playerchoice == 's' and computer == 'p') or (playerchoice == 'p' and computer == 'r'):
                await ctx.send(f"You won! The bot chose {emojidict[computer]}.")
                playerscore += 1
            elif playerchoice == "cancel":
                await ctx.send("```Cancelled```")
                return
            else:
                await ctx.send(f"You lost! The bot chose {emojidict[computer]}.")
                computerscore += 1
        if playerscore > computerscore:
            winnerem = discord.Embed(
                title = f"{ctx.author} is the winner!",
                color = discord.Color.blue()
            )
            winnerem.add_field(name = "Player score:", value = playerscore, inline = False)
            winnerem.add_field(name = "Bot score:", value = computerscore, inline = False)
            await ctx.send(embed = winnerem)
        elif playerscore < computerscore:
            winnerem = discord.Embed(
                title = f"The Bot is the winner!",
                color = discord.Color.blue()
            )
            winnerem.add_field(name = "Player score:", value = playerscore, inline = False)
            winnerem.add_field(name = "Bot score:", value = computerscore, inline = False)
            await ctx.send(embed = winnerem)
        else:
            winnerem = discord.Embed(
                title = f"It was a tie!",
                color = discord.Color.blue()
            )
            winnerem.add_field(name = "Player score:", value = playerscore, inline = False)
            winnerem.add_field(name = "Bot score:", value = computerscore, inline = False)
            await ctx.send(embed = winnerem)
 

@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You're missing permissions to execute that command!")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Please enter all the required arguements!")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=">help | Developed by Spinduck5384#1704| https://bountybot.netlify.app/"))
    print("Bot is online")

client.run(token)
