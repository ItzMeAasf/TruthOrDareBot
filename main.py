import os

import requests
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

PM_START_TEXT = """
<b>Welcome</b> {} <b>ー(  ° v ° )ﾉ</b>
`I'm A Telegram Truth Or Dare Game Bot!`
<b>Keep Your Group More Active By Using Cmd /td In Your Group ××</b>
"""


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


def change_t(user_id):
    BUTTON = [
        [
            InlineKeyboardButton(
                text="🔄 Change", callback_data=" ".join(["refresh_truth", str(user_id)])
            )
        ]
    ]
    return InlineKeyboardMarkup(BUTTON)


def change_d(user_id):
    BUTTON = [
        [
            InlineKeyboardButton(
                text="🔄 Change", callback_data=" ".join(["refresh_dare", str(user_id)])
            )
        ]
    ]
    return InlineKeyboardMarkup(BUTTON)


@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_photo(
        photo="https://telegra.ph/file/52161ddc6c3e6dc7d94b5.jpg",
        caption=PM_START_TEXT.format(message.from_user.mention),
    )


@app.on_message(filters.command("td"))
async def td(client, message):
    user = message.from_user
    if message.chat.type == "private":
        await message.reply_text(text="`This Command Only Works In Group`")
    else:
        await message.reply_text(text="`Reply To A User`")
        return
    if message.reply_to_message:
        await message.reply_text(
            text="{} Choose The Question Type You Want!".format(user.mention),
            reply_markup=t_or_d(user.id),
        )


@app.on_callback_query()
async def callbackstuffs(client, callback_query):
    t_link = requests.get("https://api.truthordarebot.xyz/v1/truth").json()
    t_list = t_link.get("question")
    d_link = requests.get("https://api.truthordarebot.xyz/v1/dare").json()
    d_list = d_link.get("question")
    user = callback_query.from_user
    c_q_d, user_id = callback_query.data.split()
    if str(user.id) == str(user_id):
        if c_q_d == "truth_data":
            await callback_query.answer(
                text="You Asked A Truth Question", show_alert=False
            )
            await client.delete_messages(
                chat_id=callback_query.message.chat.id,
                message_ids=callback_query.message.id,
            )

            await callback_query.message.reply_text(
                "**{user} Asked Truth Question:** __{t_list}__".format(
                    user=user.mention,
                    t_list=t_list,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🔄 Change",
                                    callback_data=" ".join(
                                        ["refresh_truth", str(user_id)]
                                    ),
                                )
                            ],
                        ]
                    ),
                )
            )
            return

        if c_q_d == "dare_data":
            await callback_query.answer(
                text="You Asked A Dare Question", show_alert=False
            )
            await client.delete_messages(
                chat_id=callback_query.message.chat.id,
                message_ids=callback_query.message.id,
            )
            await callback_query.message.reply_text(
                "**{user} Asked Dare Question:** __{d_list}__".format(
                    user=user.mention,
                    d_list=d_list,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🔄 Change",
                                    callback_data=" ".join(
                                        ["refresh_dare", str(user_id)]
                                    ),
                                )
                            ],
                        ]
                    ),
                )
            )
            return

        if c_q_d == "refresh_truth":
            await callback_query.answer(
                text="New Truth Question Changed", show_alert=False
            )
            await client.delete_messages(
                chat_id=callback_query.message.chat.id,
                message_ids=callback_query.message.id,
            )

            await callback_query.message.reply_text(
                "**{user} Asked Truth Question:** __{t_list}__".format(
                    user=user.mention, t_list=t_list, reply_markup=change_t(user.id)
                )
            )
            return

        if c_q_d == "refresh_dare":
            await callback_query.answer(
                text="New Dare Question Asked", show_alert=False
            )
            await client.delete_messages(
                chat_id=callback_query.message.chat.id,
                message_ids=callback_query.message.id,
            )
            await callback_query.message.reply_text(
                "**{user} Asked Dare Question:** __{d_list}__".format(
                    user=user.mention, d_list=d_list, reply_markup=change_d(user.id)
                )
            )
            return

        else:
            await callback_query.answer(
                text="You Are Not The Person Using This Command!", show_alert=False
            )
            return


app.run()
