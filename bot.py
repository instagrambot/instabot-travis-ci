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

my_likers = set([
    liker for media in my_last_medias for liker in bot.get_media_likers(media)
])

my_followers = set(bot.followers)

likers_that_dont_follow = my_likers - my_followers
print("Found %d likers that I don't follow" % len(likers_that_dont_follow))

for user in likers_that_dont_follow:
    if not bot.api.get_user_feed(user):
        print("can't get %s feed, private user?" % user)
        continue

    user_medias = [m["id"] for m in bot.api.last_json["items"] if not m["has_liked"]] 
    
    medias_to_like = random.sample(user_medias, min(random.randint(1,3), len(user_medias)))
    for m in medias_to_like:
        bot.like(m, check_media=False)
        time.sleep(random.random() * 5)

    time.sleep(random.random() * 10 + 5)


