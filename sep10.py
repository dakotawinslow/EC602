import time

WORDLIST = ["cat", "dog", "rabbit", "bird", "fish", "cheeseburger", "ice cream sundae"]


def title_caseify(word: str) -> str:
    word = word.title()
    return word


def return_capitalized_list(words):
    caps = [title_caseify(word) for word in words]
    return caps


def caps_in_place(words):
    for i in range(len(words)):
        word = words[i]
        newword = title_caseify(word)
        words[i] = newword


my_dict = {
    "cat": "feline",
    "dog": "canine",
    "rabbit": "bunny",
    "bird": "avian",
    "fish": "aquatic",
    "cheeseburger": "delicious",
    "ice cream sundae": "delicious",
}

# for keys in my_dict:
#     print(keys, my_dict[keys])

# for value in my_dict.values():
#     print(value)

# for keys, values in my_dict.items():
#     print(keys, values)

print(my_dict.values(), type(my_dict.values()))
mydictvals = my_dict.values()

print(my_dict.keys(), type(my_dict.keys()))
