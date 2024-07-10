import time
import os


def func_stopwatch(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        object_wrapper = {
            "result": result,
            "timer": end - start
        }

        return object_wrapper
    return wrapper


def followers_actions(response, target_username, folder_path):

    if os.path.exists(f"{folder_path}\\followers.{target_username}.txt"):
        with open(f"{folder_path}\\followers.{target_username}.txt", "r") as file:

            followers_result_read = file.read()
            set_followers = set(followers_result_read.split('\n'))

            not_followers = set_followers.difference(response)
            new_followers = response.difference(set_followers)

            message = f"Изменений в followers нет"

            if not_followers:
                with open(f"{folder_path}\\unfollowed.{target_username}.txt", "a") as not_f:

                    not_followers_str = '\n'.join(not_followers)
                    not_f.write(not_followers_str + '\n')
                    message = f"отписавшиеся: {list(not_followers)}"

                    return message

            if new_followers:
                with open(f"{folder_path}\\new_followed.{target_username}.txt", "w") as not_f:

                    new_followers_str = '\n'.join(new_followers)
                    not_f.write(new_followers_str + '\n')
                    message = f"новые followers: {list(not_followers)}"

                    return message

        return message
