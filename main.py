from typing import List, Tuple
import interactions
from interactions import Button
from platform_linux import PlatformLinux
from dotenv import dotenv_values
import os
import glob


# load env variables
config = dotenv_values('.env')

# global variables
bot = interactions.Client(
    token=config["DISCORD_TOKEN"],
)

platform = PlatformLinux(config)


@bot.event
async def on_start():
    print("Bot is running!")


@bot.command(
    name="screenshot",
    description="takes a screenshot of the client",
)
async def screenshot(ctx: interactions.CommandContext):
    msg = await ctx.send(f"checking...")

    file, components = await screenshot_compose_message()

    await msg.edit(content="", files=file, components=components)
    platform.cleanup()

# This is its own method because if we put the code into screenshot() then we don't
# actually have a way to string the "direct" /screenshot call and the /game routine together,
# since game_select() only has a ComponentContext ctx that's incompatible
# with screenshot()'s CommandContext, making it impossible to call the latter from within the former.
async def screenshot_compose_message() -> Tuple[interactions.File, List[interactions.ActionRow]]:
    filename = await platform.screenshot()
    file = interactions.File(filename)
    #embed = interactions.Embed()
    #embed.set_image(url="attachment://" + filename)

    # create all the buttons
    buttonA = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="🇦",
        custom_id="A",
    )

    buttonB = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="🇧",
        custom_id="B",
    )

    buttonLEFT = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="⬅️",
        custom_id="LEFT",
    )
    buttonRIGHT = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="➡️",
        custom_id="RIGHT",
    )
    buttonUP = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="⬆️",
        custom_id="UP",
    )
    buttonDOWN = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="⬇️",
        custom_id="DOWN",
    )

    buttonSELECT = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="SELECT",
        custom_id="SELECT",
    )
    buttonSTART = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="START",
        custom_id="START",
    )

    buttonL = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="🇱",
        custom_id="L",
    )
    buttonR = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="🇷",
        custom_id="R",
    )

    row1 = interactions.ActionRow(
        components=[buttonLEFT, buttonRIGHT, buttonUP, buttonDOWN]
    )
    row2 = interactions.ActionRow(
        components=[buttonA, buttonB, buttonL, buttonR]
    )
    row3 = interactions.ActionRow(
        components=[buttonSTART, buttonSELECT]
    )

    return file, [row1, row2, row3]

@bot.command(
    name="game",
    description="lets you pick a game to play",
)
async def game(ctx: interactions.CommandContext):
    msg = await ctx.send(f"checking")

    games = list()

    # TODO: don't limit the emulator choice by file extension. However, temporary files
    # and save files need to be filtered out still, any good way to accomplish both?
    game_files = glob.glob("./roms/*.gba")

    for game_file in game_files:
        option = interactions.SelectOption(
            label=game_file,
            value=game_file,
        )
        games.append(option)

    menu = interactions.SelectMenu(
        options=games,
        placeholder="available ROMs...",
        custom_id="menu_games",
    )

    await msg.edit(content="pick a game to play", components=menu)


# methods that are triggered by button presses on the discord message
@bot.component("A")
async def button_A(ctx):
    original_message = ctx.message
    await platform.button_press(platform.Buttons.A)

# methods that are triggered by select actions on discord messages
@bot.component("menu_games")
async def game_select(ctx, selected_option: str):
    original_message = ctx.message
    await original_message.edit(content="starting game...")
    platform.run_client(selected_option[0])
    
    file, components = await screenshot_compose_message()

    await original_message.edit(content="", files=file, components=components)
    platform.cleanup()


bot.start()
