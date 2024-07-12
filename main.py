import sys
from time import sleep

from service.profile import profile_actions, profile, loader, folder_path


def main():
    try:
        response = profile_actions(profile_=profile, context=loader.context, folder=folder_path)
        print(response.get("result"))
        timer = response.get("timer")
        print(timer)

    except KeyboardInterrupt:
        sleep(1)
        print(f"Завершено пользователем")
        sys.exit(1)


if __name__ == "__main__":
    main()
