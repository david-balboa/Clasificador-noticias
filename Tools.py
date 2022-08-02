# To clean the given word from special characters
def clean_word(word):
    # set word in lowercase
    word = word.lower()
    # first clean of special characters
    word = word.replace(",", "").replace(".", "").replace("'s", "").strip()
    # is necessary continue the cleaning?
    wlength = len(word)
    if (wlength < 2):
        return word
    # remove special characters from the word
    to_remove = [":", ";", "(", ")", "?", "!", "'", "%", "$", "#", "'", '"']
    while (word[0] in to_remove) and (wlength > 1):
        word = word[1:]
        wlength -= 1

    while (word[wlength-1] in to_remove) and (wlength > 1):
        word = word[:wlength-1]
        wlength -= 1

    return word.strip()

# To avoid 3-characters words and numbers
def should_be_filtered(word):
    return (len(word) < 4) or word.isdigit() or any(map(str.isdigit, word))