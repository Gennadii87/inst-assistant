import os
from dotenv import load_dotenv
from instaloader import (Instaloader,
                         Profile,
                         TwoFactorAuthRequiredException,
                         BadCredentialsException,
                         ConnectionException,
                         LoginRequiredException)


load_dotenv()

username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")

target_username = os.getenv("TARGET_USER")

if not username or not password:
    raise ValueError("USER_NAME and PASSWORD must be set in the .env file")


app = Instaloader()

try:
    app.load_session_from_file(username)
except FileNotFoundError:

    try:
        app.login(username, password)
    except TwoFactorAuthRequiredException:

        two_factor_code = input("Enter the 2FA code: ")
        try:
            app.context.two_factor_login(two_factor_code)
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

    app.save_session_to_file()

try:
    profile = Profile.from_username(app.context, target_username)
except LoginRequiredException as e:
    print(f"Login required to access profile: {e}")
    exit(1)
except ConnectionException as e:
    print(f"Connection error while accessing profile: {e}")
    exit(1)


def print_followers(profile_):
    try:
        quantity_followers = profile_.followers
        followers = profile_.get_followers()
        follower_names = [follower.username for follower in followers]
    except LoginRequiredException as exc:
        print(f"Login required to get followers: {exc}")
        exit(1)
    except ConnectionException as exc:
        print(f"Connection error while getting followers: {exc}")
        exit(1)
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        exit(1)

    result_name = profile_.username
    result_follow = quantity_followers

    result_all = (
                     f"Имя пользователя: {result_name}, "
                     f""f"Количество подписчиков: {result_follow},\nИмена подписчиков:\n"
                 ) + '\n'.join(follower_names)

    return result_all


if __name__ == "__main__":
    print(print_followers(profile))
