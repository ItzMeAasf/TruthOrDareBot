import os
import random

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_ID = os.environ.get("API_ID", None)
API_HASH = os.environ.get("API_HASH", None)
TOKEN = os.environ.get("TOKEN", None)

# For Local Deploy:
"""
API_ID = ""
API_HASH = ""
TOKEN = ""
"""
app = Client("TD", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

TRUTH = (
    "Have you ghosted someone?" "Have you ever walked in on your parents doing 'it'?",
    "Who was the last person you liked the most? Why?",
    "Have you ever been suspended from school?",
    "If you had to choose between going naked or having your thoughts appear in thought bubbles above your head for everyone to read, which would you choose?",
    "What’s the one thing you’re afraid to lose?",
    "Do you like someone as of the moment?",
    "One thing about your best friend you are jealous of?",
    "Would you cheat on your boyfriend for a rich guy?",
    "What is your biggest turn on?",
    "When’s the last time you lied to your parents and why?",
    "Describe your ideal partner.",
    "What’s the scariest thing you’ve ever done?",
    "Have you ever picked your nose and eaten it?",
    "When’s the last time you lied to your parents and why?",
    "Have you ever lied about your age to participate in a contest?",
    "Have you ever been caught checking someone out?",
)

DARE = (
    "Show the most embarrassing photo on your phone"
    "Show the last five people you texted and what the messages said",
    "Let the rest of the group DM someone from your Instagram account",
    "Eat a raw piece of garlic",
    "Do 100 squats",
    "Keep three ice cubes in your mouth until they melt",
    "Say something dirty to the person on your leftYou've got company!",
    "Give a foot massage to the person on your right",
    "Put 10 different available liquids into a cup and drink it",
    "*Yell out the first word that comes to your mind",
    "Give a lap dance to someone of your choice",
    "Remove four items of clothing",
    "Like the first 15 posts on your Facebook newsfeed",
    "Eat a spoonful of mustard",
    "Keep your eyes closed until it's your go again",
    "Send a sext to the last person in your phonebook",
    "Show off your orgasm face",
    "Seductively eat a banana",
    "Empty out your wallet/purse and show everyone what's inside",
    "Do your best sexy crawl",
    "Pretend to be the person to your right for 10 minutes",
    "Eat a snack without using your hands",
    "Say two honest things about everyone else in the group",
    "Twerk for a minute",
    "Try and make the group laugh as quickly as possible",
    "Try to put your whole fist in your mouth",
    "Tell everyone an embarrassing story about yourself",
    "Try to lick your elbow",
    "Post the oldest selfie on your phone on Instagram Stories",
    "Tell the saddest story you know",
    "Howl like a wolf for two minutes",
    "Dance without music for two minutes",
    "Pole dance with an imaginary pole",
    "Let someone else tickle you and try not to laugh",
    "Put as many snacks into your mouth at once as you can",
    "Send your most recent selfie.",
    "Send your ugliest selfie.",
    "Send a screenshot of your facebook search history",
    "Send a screenshot of your gallery.",
    "Send a screenshot of your messenger inbox",
    "Tell something very intimate.",
    "Send a screenshot of your twitter inbox",
    "Send a screenshot of your homescreen.",
    "Send a cover of your favorite song. 🎤",
    "Do a lyric prank on someone and send proof.",
    "Confess to your current crush. ❤️",
    "Declare who is your true love.",
    "Send a screenshot of your gallery.",
    "Set your crush’s picture as your dp.",
    "Suggest me more dares.",
)


def t_or_d(user_id):
    BUTTON = [
        [
            InlineKeyboardButton(
                text="✅ Truth", callback_data=" ".join(["truth_data", str(user_id)])
            )
        ]
    ]
    BUTTON += [
        [
            InlineKeyboardButton(
                text="💪 Dare", callback_data=" ".join(["dare_data", str(user_id)])
            )
        ]
    ]
    return InlineKeyboardMarkup(BUTTON)


@app.on_message(filters.command("td"))
async def _(client, message):
    user = message.from_user
    await message.reply_text(
        text="{} Choose The Question Type You Want!".format(user.mention),
        reply_markup=t_or_d(user.id),
    )


@app.on_callback_query()
async def _(client, callback_query):
    t_list = random.choice(TRUTH)
    d_list = random.choice(DARE)
    user = callback_query.from_user
    c_q_d, user_id = callback_query.data.split()
    if str(user.id) == str(user_id):
        if c_q_d == "truth_data":
            await callback_query.answer(
                text="You Asked A Truth Question", show_alert=False
            )
            await client.delete_messages(
                chat_id=callback_query.message.chat.id,
                message_ids=callback_query.message.message_id,
            )

            await callback_query.message.reply_text(
                "**{user} Asked Truth Question:** __{t_list}__".format(
                    user=user.mention, t_list=t_list
                )
            )
            return

        if c_q_d == "dare_data":
            await callback_query.answer(
                text="You Asked A Dare Question", show_alert=False
            )
            await client.delete_messages(
                chat_id=callback_query.message.chat.id,
                message_ids=callback_query.message.message_id,
            )
            await callback_query.message.reply_text(
                "**{user} Asked Dare Question:** __{d_list}__".format(
                    user=user.mention, d_list=d_list
                )
            )
            return

        else:
            await callback_query.answer(
                text="You Are Not The Person Using This Command!", show_alert=False
            )
            return
