import sys
import os
import collections
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style


def create_save_dir(dir_name):
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass


def save_to_file(filename, contents):
    with open(filename, "w") as f:
        f.write(contents)


args = sys.argv
save_dir = args[1]
create_save_dir(save_dir)
stack = collections.deque()

while True:
    url = input()
    if url == "exit":
        break
    elif url == "back":
        if len(stack) > 1:
            temp = stack.pop()
            print(stack.pop())
            stack.append(temp)
    elif "." not in url:
        print("URL error")
    else:
        filename = save_dir + "/" + url.split('.')[0]
        if not url.startswith("https://"):
            url = "https://" + url
        data = requests.get(url)
        if data:
            soup_data = BeautifulSoup(data.content, "html.parser")
            tags = soup_data.find_all(["p", "a", "ul", "ol", "li", "h1",
                                       "h2", "h3", "h4", "h5", "h6"])
            contents = ""
            for tag in tags:

                if str(tag).startswith("<a "):
                    contents = contents + Fore.BLUE + " ".join(tag.text.split()) + "\n"
                contents = contents + Style.RESET_ALL + " ".join(tag.text.split()) + "\n"
            print(contents)
            save_to_file(filename, contents)
            stack.append(contents)
        else:
            print("URL access error")