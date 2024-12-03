import tkinter as tk
import numpy as np
import itertools
import gensim
import pyautogui as pag
import time

BG_COLOR = "gray16"
TXT_COLOR = "white"

combos = []

hints = []

# Create a codenames board
with open("wordlist-eng.txt") as f:
    words = f.readlines()
    words = [word.strip().lower() for word in words]
board = np.random.choice(words, size=(5, 5), replace=False)

special_words = np.random.choice(range(25), size=18, replace=False)
flat_board = board.flatten()
red_words = flat_board[special_words[:8]]
blue_words = flat_board[special_words[8:17]]
assassin = flat_board[special_words[17]]

# Load the word2vec model
model = "GoogleNews-vectors-negative300-SLIM"
word2vec = gensim.models.KeyedVectors.load(f"models/{model}.kv")


def cos_similar(a, b):
    "convenience function to calculate the cosine similarity between two vectors"
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def has_common_substring(a, b, min_length=3):
    """
    Check if any substring of length >= min_length from string `a` is in string `b`.

    :param a: First string
    :param b: Second string
    :param min_length: Minimum length of the substring (default: 2)
    :return: True if any substring of length >= min_length in `a` is in `b`, otherwise False
    """
    len_a = len(a)
    for start in range(len_a):
        for end in range(start + min_length, len_a + 1):
            substring = a[start:end]
            if substring in b:
                return True
    return False


def find_best_subset(word_list: list, set_size=2):
    "Finds the best subset of words by rating all possible subsets"
    # first, make sure all the words are in ourt vocab, and kick any that aren't
    word_list = [word for word in word_list if word in word2vec.index_to_key]
    # generate all possible subsets
    subsets = itertools.combinations(word_list, set_size)
    best_subset = ([], 0)
    for subset in subsets:
        # first find the centroid of all the vectors
        centroid = np.mean([word2vec[word] for word in subset], axis=0)
        # then find the similarity of the centroid to each word in the subset
        similarity = np.mean([cos_similar(word2vec[word], centroid) for word in subset])
        # if the similarity is better than the current best, update the best
        if similarity > best_subset[1]:
            best_subset = (subset, similarity)
    return best_subset


def main():
    # Create the main window
    window = tk.Tk()
    window.configure(bg=BG_COLOR)
    # always be on top
    window.wm_attributes("-topmost", 1)
    # window.resizable(False, False)
    window.attributes("-toolwindow", True)
    window.title("Spymaster's Assistant")

    # Side-By-Side Radiobuttons for Red/Blue Team
    buttonFrame = tk.Frame(window)
    buttonFrame.configure(bg=BG_COLOR)
    team = tk.BooleanVar()
    team.set(True)
    team_label = tk.Label(window, text="Choose Team", bg=BG_COLOR, fg=TXT_COLOR)
    team_label.pack()
    red_button = tk.Radiobutton(
        buttonFrame,
        text="Red",
        variable=team,
        value=True,
        bg="red4",
        fg=TXT_COLOR,
        selectcolor=BG_COLOR,
    )
    red_button.pack(side=tk.LEFT)
    blue_button = tk.Radiobutton(
        buttonFrame,
        text="Blue",
        variable=team,
        value=False,
        bg="blue4",
        fg=TXT_COLOR,
        selectcolor=BG_COLOR,
    )
    blue_button.pack(side=tk.LEFT)
    buttonFrame.pack()

    CombosLabel = tk.Label(window, text="Top Combos", bg=BG_COLOR, fg=TXT_COLOR)
    CombosLabel.pack()

    # create listbox object
    CombosList = tk.Listbox(
        window,
        height=3,
        width=30,
        bg=BG_COLOR,
        activestyle="dotbox",
        font="Courier",
        fg=TXT_COLOR,
    )
    CombosList.pack()

    HintLabel = tk.Label(
        window, text="Possible Hints (Match Quality)", bg=BG_COLOR, fg=TXT_COLOR
    )
    HintLabel.pack()

    HintList = tk.Listbox(
        window,
        height=10,
        width=30,
        bg=BG_COLOR,
        activestyle="dotbox",
        font="Courier",
        fg=TXT_COLOR,
    )
    HintList.pack()

    def update_combo_list():
        # find best combos
        global combos
        combos = []
        if team.get():
            target_words = red_words
        else:
            target_words = blue_words
        for i in range(2, 5):
            combos.append(find_best_subset(target_words, i)[0])
        # print("combos:", combos)
        for i, combo in enumerate(combos):
            CombosList.insert(i, " ".join(combo))

    update_combo_list()
    # buttonFrame.bind("<Button-1>", update_combo_list)
    team.trace_add("write", lambda *args: update_combo_list())

    def update_hint_list(selection=None):
        # Check if one of the rows in the listbox is selected
        target_words = combos[CombosList.curselection()[0]]
        # print("target words:", target_words)
        # Display the hints for the selected row
        hints = []
        similars = word2vec.most_similar(positive=list(target_words), topn=15)
        for attempt in similars:
            # make sure the clue is not a word on the board
            attempt = (attempt[0].lower(), attempt[1])
            if attempt[0] in flat_board:
                continue
            # make sure ther clue is not a form of one of the prompts
            if has_common_substring(
                attempt[0], target_words[0]
            ) or has_common_substring(attempt[0], target_words[1]):
                continue
            # make sure the clue is not repeated in the list
            if any(has_common_substring(attempt[0], hint[0]) for hint in hints):
                continue
            hints.append(attempt)
        for i, hint in enumerate(hints):
            HintList.insert(
                i, str.ljust(hint[0], 15) + " (" + str(round(hint[1], 3)) + ")"
            )

    CombosList.bind("<<ListboxSelect>>", update_hint_list)

    def capture_screen_data():
        # Capture the screen data
        screen_data = pag.screenshot()
        print("Screen Data Captured")

    screencapButton = tk.Button(
        window, text="Capture Screen", command=capture_screen_data
    )
    screencapButton.pack()

    # Start the Tkinter event loop
    while True:
        # ~~~~~~~~ Capture Screen Data ~~~~~~~~

        try:
            window.update_idletasks()
            window.update()
        except tk.TclError:
            break


if __name__ == "__main__":
    main()
