import os
from datetime import datetime

from dotenv import load_dotenv
from instaloader import (Instaloader,
                         Profile,
                         TwoFactorAuthRequiredException,
                         BadCredentialsException,
                         ConnectionException,
                         LoginRequiredException, NodeIterator)

from service import followers_actions
from service import func_stopwatch

load_dotenv()

username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")

target_username = os.getenv("TARGET_USER")

if not username or not password:
    raise ValueError("USER_NAME and PASSWORD must be set in the .env file")


loader = Instaloader(sleep=True)
NodeIterator._graphql_page_length = 10

folder_path = os.path.join(os.getcwd(), "followers")
os.makedirs(folder_path, exist_ok=True)

print(f"Инициализация {datetime.now().time()}")


try:
    loader.load_session_from_file(username)
    print(f"Get session {datetime.now().time()}")
except FileNotFoundError:

    try:
        loader.login(username, password)
        print(f"Login profile {datetime.now().time()}")
    except TwoFactorAuthRequiredException:

        two_factor_code = input("Enter the 2FA code: ")
        try:
            loader.context.two_factor_login(two_factor_code)
        except BadCredentialsException as e:
            print(f"Failed 2FA login: {e}")
            exit(1)
    except BadCredentialsException as e:
        print(f"Invalid credentials: {e}")
        exit(1)
    except ConnectionException as e:
        print(f"Connection error: {e}")
        exit(1)
    except LoginRequiredException as e:
        print(f"Login required: {e}")
        exit(1)

    loader.save_session_to_file()

try:
    profile = Profile.from_username(loader.context, target_username)
except LoginRequiredException as e:
    print(f"Login required to access profile: {e}")
    exit(1)
except ConnectionException as e:
    print(f"Connection error while accessing profile: {e}")
    exit(1)


@func_stopwatch
def profile_actions(profile_, context, folder):
    try:
        context.do_sleep()
        print(f"start: {datetime.now().time()}")

        context.do_sleep()
        quantity_followers = profile_.followers
        print(f"Всего followers: {quantity_followers}")

        context.do_sleep()
        print(f"Получение followers..")

        followers = profile_.get_followers()

        page_length_int = followers.page_length()

        print(f"Длинна запрашиваемой страницы {page_length_int}")

        follower_names = set()

        for index, follower in enumerate(followers, start=1):
            follower_names.add(follower.username)

            if index % 7 == 0:
                @func_stopwatch
                def request_sleep():
                    context.do_sleep()

                sleep_time = request_sleep()
                timer = round(sleep_time, 3)
                print(f"Пауза ({timer}sec)... {index} followers")

        print(f"Completed fetching followers: {len(follower_names)}")

        result_name = profile_.username
        result_follow = quantity_followers
        follower_names_str = '\n'.join(follower_names)

        result_actions = followers_actions(follower_names, target_username, folder)

        with open(f"{folder_path}\\followers.{target_username}.txt", "w") as file:

            if follower_names:
                file.write(follower_names_str)
                print(f"{file.name} записан")

        result_all = {
                        "Имя пользователя": result_name,
                        "Количество подписчиков": result_follow,
                        "Действия": result_actions if result_actions is not None else "Действий не обнаружено"
                     }

        return result_all

    except LoginRequiredException as exc:
        print(f"Login required to get followers: {exc}")
        exit(1)
    except ConnectionException as exc:
        print(f"Connection error while getting followers: {exc}")
        exit(1)
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        exit(1)


def main():
    result = profile_actions(profile_=profile, context=loader.context, folder=folder_path)
    print(result.get("result"))
    timer = result.get("timer")

    if timer < 61:
        print(f"время выполнения {round(timer, 3)}sec")
    else:
        print(f"время выполнения {round(timer / 60, 2)}min")


if __name__ == "__main__":
    main()
