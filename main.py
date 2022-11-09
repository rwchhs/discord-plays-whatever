import interactions
from interactions import Button
from platform_linux import PlatformLinux
from dotenv import dotenv_values


# load env variables
config = dotenv_values('.env')

# global variables
bot = interactions.Client(
    token = config["DISCORD_TOKEN"],
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
    msg = await ctx.send(f"checking")
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

    await msg.edit(content="", files=file, components=[row1, row2, row3])
    platform.cleanup()


# methods that are triggered by button presses on the discord message
@bot.component("A")
async def button_A(ctx):
    original_message = ctx.message
    await platform.button_press(platform.Buttons.A)

bot.start()
