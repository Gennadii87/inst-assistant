import time
import os


def func_stopwatch(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        if end - start < 61:
            timer = f"время выполнения {round(end - start, 3)}sec"
        else:
            timer = f"время выполнения {round((end - start) / 60, 2)}min"

        object_wrapper = {
            "result": result,
            "timer": timer
        }

        return object_wrapper
    return wrapper


def followers_actions(follower, target, folder):

    if os.path.exists(f"{folder}\\followers.{target}.txt"):
        with open(f"{folder}\\followers.{target}.txt", "r") as file:

            followers_result_read = file.read()
            set_followers = set(followers_result_read.split('\n'))

            not_followers = set_followers.difference(follower)
            new_followers = follower.difference(set_followers)

            message = f"Изменений в followers нет"

            if not_followers:
                with open(f"{folder}\\unfollowed.{target}.txt", "a") as not_f:

                    not_followers_str = '\n'.join(not_followers)
                    not_f.write(not_followers_str + '\n')
                    message = f"отписавшиеся: {list(not_followers)}"

                    return message

            if new_followers:
                with open(f"{folder}\\new_followed.{target}.txt", "w") as not_f:

                    new_followers_str = '\n'.join(new_followers)
                    not_f.write(new_followers_str + '\n')
                    message = f"новые followers: {list(not_followers)}"

                    return message

        return message
