import sys
import requests
from bs4 import BeautifulSoup
import os

languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese',
             'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish']
real_std = sys.stdout


def translate(frm, to, text, counts):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://context.reverso.net/translation/{languages[frm]}-{languages[to]}/{text}"
    lang = languages[to].title()
    try:
        page = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        print("Something wrong with your internet connection")
        exit()
    if page.status_code == 404:
        print(f"Sorry, unable to find {text}")
        exit()
    soup = BeautifulSoup(page.content, "html.parser")
    translates = []
    for a in soup.find("div", attrs={"id": "translations-content"}).find_all("a")[:counts]:
        translates.append(a.text.strip("\n "))
    with open(f"{text}.txt", "a", encoding="utf-8") as sys.stdout:
        print()
        print(lang, "Translations:")
        print("\n".join(translates))
        print()
        examples = [e.text.strip() for e in
                    soup.find("section", attrs={"id": "examples-content"}).find_all("span", class_="text")][
                   :2 * counts]
        print(lang, "Example:")
        for i in range(0, len(examples), 2):
            print(examples[i])
            print(examples[i + 1])
            print()


if True:
    args = sys.argv
    if len(args) == 4:
        if args[1].lower() in languages:
            lang_from = languages.index(args[1].lower())
        else:
            print(f"Sorry, the program doesn't support {args[1]}")
            exit()
        if args[2].lower() in languages:
            lang_to = languages.index(args[2].lower())
        elif args[2].lower() == "all":
            lang_to = -1
        else:
            print(f"Sorry, the program doesn't support {args[2]}")
            exit()
        word = args[3]
        if os.path.exists(f"{word}.txt"):
            os.remove(f"{word}.txt")
        if lang_to == -1:
            for too in range(len(languages)):
                if too != lang_from:
                    translate(lang_from, too, word, 1)
        else:
            translate(lang_from, lang_to, word, 5)
        sys.stdout = real_std
        with open(f"{word}.txt", encoding="utf-8") as f:
            for line in f:
                print(line, end="")
