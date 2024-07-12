import sys
from time import sleep

from service.profile import profile_actions, profile, loader, folder_path


def main():

    response = profile_actions(profile_=profile, context=loader.context, folder=folder_path)
    print(response.get("result"))
    timer = response.get("timer")
    print(timer)


try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    sleep(1)
    print(f"Завершено пользователем")
    sys.exit(1)
