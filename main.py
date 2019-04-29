import time
import traceback

import praw
import schedule

import config
from database import DatabaseManager
from scan import scan


def start():
    print("Starting main")

    try:
        reddit = praw.Reddit(
            client_id=config.CLIENT["ID"],
            client_secret=config.CLIENT["SECRET"],
            user_agent=config.USER_AGENT,
            username=config.USERNAME,
            password=config.PASSWORD)
    except Exception as e:
        print("Exception occurred while instantiating praw")
        traceback.print_exc()
        print("End of praw exception handler")

    try:
        scan(reddit.subreddit(config.SUBREDDIT))
    except Exception as e:
        print("Exception occurred while scanning")
        traceback.print_exc()
        print("End of scan exception handler")


    try:
        DatabaseManager.disconnect()
    except Exception as e:
        print("Exception occurred while disconnecting database")
        traceback.print_exc()
        print("End of database disconnect exception handler")


schedule.every(config.RUN_EVERY).minutes.do(start)


if __name__ == "__main__":
    start()
    while True:
        schedule.run_pending()
        print("Sleeping")
        time.sleep(1)
