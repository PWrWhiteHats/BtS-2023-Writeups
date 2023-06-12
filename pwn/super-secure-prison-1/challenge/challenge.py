#!/usr/bin/env python

import ast

from time import sleep

# Blacklisted AST calls
BLACKLIST = {
    ast.Import
}

# List of forbidden words
FORBIDDEN_WORDS = {"eval", "exec", "system", "sys", "subprocess"}

CUSTOM_JAIL = []

WARDENS_MESSAGES = []


def is_code_secure(code: str) -> bool:
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, tuple(BLACKLIST)):
                return False
        return True
    except SyntaxError:
        print(code)
        return False


def clear_console():
    print("\033[H\033[J", end="")


def show_imprisoned():
    print("That's how the jail looks like now:")
    for word in FORBIDDEN_WORDS:
        print(
            f"""
              {'':_^20}
              |{'':#^19}|
              |{word:*^19}|
              |{'':#^19}|
              |{'':_^19}|
              """
        )
    for word in BLACKLIST:
        print(
            f"""
              |{'':#^19}|
              |{word.__name__:*^19}|
              |{'':#^19}|
              """
        )

    for custom in CUSTOM_JAIL:
        print(
            f"""
              |{'':#^19}|
              |{custom:*^19}|
              |{'':#^19}|
              """
        )


def imprison_someone():
    print("You are about to imprison someone")
    name = input("Please state their name: ")
    CUSTOM_JAIL.append(name)
    print("Thank you for using our software")


def write_to_another_warden():
    print("We want our communication to be secure so we use telegraphs!")
    print("<Remember to end your message with STOP>")
    print()
    user_input = ""
    end_of_transmission = "STOP"
    try:
        while end_of_transmission not in user_input:
            user_input += input(">> ") + "\n"

        source_code = user_input[: -(len(end_of_transmission) + 1)]
        if not is_code_secure(source_code) or any(
            forbidden_word in source_code for forbidden_word in FORBIDDEN_WORDS
        ):
            print(
                "Did you try to smuggle forbidden words to our jail? You cannot use this software anymore..."
            )
            exit(1)
        else:
            sleep(5)
            exec(compile(source_code, filename="test.py", mode="exec"))
            WARDENS_MESSAGES.append(source_code)
    except Exception as e:
        print(e)


def show_messages():
    clear_console()
    print("Your messages: ")
    for message in WARDENS_MESSAGES:
        print(f"Message: {message}")


def show_message_system():
    _menu = """

    1. Text another warden (for internal usage only)
    2. Messages (for internal usage only)
    """
    print(_menu, end="\n")
    option = input("Select an option from the menu: ")
    # Python 3.10 only supports match so why not old school if
    if option == "1":
        clear_console()
        write_to_another_warden()
    elif option == "2":
        clear_console()
        show_messages()
    else:
        print("Wrong option selected. You obviously can't use this tool, can you?")
        exit(1)


def show_menu():
    _menu = """

    1. Show imprisoned
    2. Imprison someone
    3. Internal message system
    """
    print(_menu, end="\n")
    option = input("Select an option from the menu: ")
    # Python 3.10 only supports match so why not old school if
    if option == "1":
        clear_console()
        show_imprisoned()
    elif option == "2":
        clear_console()
        imprison_someone()
    elif option == "3":
        clear_console()
        show_message_system()
    else:
        print("Wrong option selected. You obviously can't use this tool, can you?")
        exit(1)


def main():
    clear_console()
    prompt = """
    
   ___  ___  _____ _     ___  ___  ___   _   _   ___  _____  _____ 
  |_  |/ _ \|_   _| |    |  \/  | / _ \ | \ | | / _ \|  __ \|  ___|
    | / /_\ \ | | | |    | .  . |/ /_\ \|  \| |/ /_\ \ |  \/| |__  
    | |  _  | | | | |    | |\/| ||  _  || . ` ||  _  | | __ |  __| 
/\__/ / | | |_| |_| |____| |  | || | | || |\  || | | | |_\ \| |___ 
\____/\_| |_/\___/\_____/\_|  |_/\_| |_/\_| \_/\_| |_/\____/\____/ 
                                                                   
                                                                   
"""
    print(prompt)
    print("Welcome to the jail management system v1.0")
    print()
    print("Please note that this tool is only intended for the Warden to use!")
    while True:
        show_menu()


if __name__ == "__main__":
    main()
