import discord
import re
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore messages from bots (including itself)
    if message.author.bot:
        return

    # Combine the last 3 messages to scan for pattern
    history = [message async for message in message.channel.history(limit=3)]
    history.reverse()

    role_name = None
    member_id = None
    action = None

    for msg in history:
        if msg.author.bot:
            continue

        # Look for Role: [role name]
        role_match = re.search(r'Role\s*:\s*(.+)', msg.content)
        if role_match:
            role_name = role_match.group(1).strip()

        # Look for Member: @mention
        member_match = re.search(r'Member\s*:\s*<@!?(\d+)>', msg.content)
        if member_match:
            member_id = int(member_match.group(1))

        if "Give Role" in msg.content:
            action = "give"
        elif "Take Role" in msg.content:
            action = "take"

    if role_name and member_id and action:
        role = discord.utils.get(message.guild.roles, name=role_name)
        member = message.guild.get_member(member_id)

        if role and member:
            if action == "give":
                await member.add_roles(role)
            elif action == "take":
                await member.remove_roles(role)

            await message.channel.send("+")

# Replace with your actual bot token
bot.run("MTM2Mzk3NzA3NTIxNTY5NTg5Mg.GJrCuT.pPlmnMPjCfKYpMjvrWynFgBTis3ms0LjDEbliA")
