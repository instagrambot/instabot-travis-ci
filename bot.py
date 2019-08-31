"""
    Example script that will be executed everyday by Travis-CI.

    
    This script take my likers who don't follow me and like them. 
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
print("Found %d likers" % len(my_likers))

my_followers = set(bot.followers)

likers_that_dont_follow = my_likers - my_followers
bot.logger.info("Found %d likers that I don't follow" % len(likers_that_dont_follow))

for user in likers_that_dont_follow:
    if not bot.api.get_user_feed(user):
        bot.logger.info("Can't get %s feed, private user?" % user)
        bot.logger.info(str(bot.api.last_json))
        continue

    
    liked_user_medias = [m["id"] for m in bot.api.last_json["items"] if m["has_liked"]] 
    if len(liked_user_medias):
        bot.logger.info("User %s was already liked, skipping" % user)
        time.sleep(random.random() * 5 + 5)
        continue

    user_medias = [m["id"] for m in bot.api.last_json["items"] if not m["has_liked"]] 
    
    medias_to_like = random.sample(user_medias, min(random.randint(1,3), len(user_medias)))
    for m in medias_to_like:
        bot.like(m, check_media=False)
        time.sleep(random.random() * 5)

    time.sleep(random.random() * 30 + 10)


