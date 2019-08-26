"""
    Example script that will be executed everyday by Travis-CI.

    
    This script take my likers and like their likers. 
"""


import os 
import time
import random
from instabot import Bot


def like_media_likers(bot, media, nlikes=2):
    for user in bot.get_media_likers(media):
        bot.like_user(user, nlikes)
    return True

bot = Bot()
bot.login(
    username=os.getenv("INSTAGRAM_USERNAME"), 
    password=os.getenv("INSTAGRAM_PASSWORD"),
)

my_last_medias = bot.get_your_medias()
random.shuffle(my_last_medias)
for media in my_last_medias:
    my_last_media_likers = bot.get_media_likers(media)
    random.shuffle(my_last_media_likers)
    for user in my_last_media_likers:
        user_medias = bot.get_user_medias(user)
        random.shuffle(user_medias)
        for m in user_medias:
            like_media_likers(bot, m)
            time.sleep(random.random() * 10)



