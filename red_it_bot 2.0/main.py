import random

import praw
import telebot
import time

from PIL import Image
import requests
from io import BytesIO



TOKEN = "YOUR TOKEN HERE"
bot = telebot.TeleBot(TOKEN)

reddit = praw.Reddit(client_id="REDDIT CLIENT ID", client_secret="REDDIT CLIENT SECRET", username="REDDIT USERNAME",
                     password="REDDIT PASSWORD", user_agent="helloworld")


def extract_arg(arg):
    return arg.split()[1:]


@bot.message_handler(commands=["start"])
def greetings(message):
    bot.reply_to(message, "Hello I am a reddit bot!\nType /help to find out more!")


@bot.message_handler(commands=["help"])
def greetings(message):
    bot.reply_to(message, """Use /r to get a post from a subreddit\n
Example: /r memes, /r woosh""")


@bot.message_handler(commands=["r"])
def r(message):
    try:
        args = extract_arg(message.text)
        bot.reply_to(message, "Looking for the best post for ya")

        subreddit = reddit.subreddit(args[0])  # Get the subreddit
        hot_reddit = subreddit.hot(limit=100)  # Get the first 100 posts in hot
        post = random.choice(list(hot_reddit))  # Chose a post randomly in the 100 posts

        try:
            response = requests.get(post.url)
            img = Image.open(BytesIO(response.content))
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_photo(message.chat.id, img, caption=f"{post.title}\n\n👍 {post.ups}")
        except Exception as ex:
            if "cannot identify image file <_io.BytesIO object at" in str(ex):
                bot.send_message(message.chat.id, post.url, disable_web_page_preview=False)
                bot.send_message(message.chat.id, f"{post.title}\n\n👍 {post.ups}", disable_web_page_preview=True)

    except Exception as e:
        if str(e) == "Redirect to /subreddits/search":
            bot.send_message(message.chat.id, f'"{message.text}" That subreddit doesn\'t exist bro.')

        else:
            bot.send_message(message.chat.id, "Oops that's a problem! Try again later")
        print(e)


while True:
    try:
        bot.polling()
    except:
        time.sleep(5)
