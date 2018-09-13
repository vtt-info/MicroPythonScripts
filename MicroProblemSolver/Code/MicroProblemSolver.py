import json
import time
import urandom
import ssd1306
import machine


def clear_display(blnFill=0, blnShow=0):
    """
    This can be use either to clear the screen will all pixels activated or deactivated by changing the
    blnFill and if the blnShow is set to one it will immediately shown on the OLED screen

    Args:
        blnFill: Boolean to fill the screen.
        blnShow: Boolean to show or not on the screen.

    Returns:
            Nothing.
    """
    display.fill(blnFill)
    if blnShow:
        display.show()


def wrapped_text(pstrMessage, MaxChars = 16):
    """
    It will split the text to fit the MaxChars by line, by default is set to 16 but it could be changed.

    Args:
        pstrMessage: String with the text to split.

    Returns:
        wordlines: List with the text sliced.
    """
    words = pstrMessage.split(" ")
    wordlines = []
    message = ""
    for iteraction, word in enumerate(words):
        remaining_chars = MaxChars - len(message)
        if (len(message + " " + word) <= remaining_chars) or ((len(word) + 1) <= remaining_chars):
            if iteraction == len(words) - 1:
                message += word + " "
                wordlines.append(message)
                break
            else:
                message += word + " "
        else:
            if iteraction == len(words) - 1:
                wordlines.append(message)
                message = word + (" " * remaining_chars)
                wordlines.append(message)
                break
            else:
                wordlines.append(message)
                message = word + " "
        if (len(message) >= MaxChars):
            wordlines.append(message)
            message = ""
    return wordlines

def print_wrapped(lstwords):
    """
    This will print the text into the screen display.

    Args:
        lstwords: List with the text to print.

    Returns:
        Nothing.
    """
    Lines = [0, 8, 16, 24, 32, 40, 48]
    if len(lstwords) <= len(Lines):
        for Item, Message in enumerate(lstwords):
            display.text(Message, 0, Lines[Item])
            display.show()
    else:
        line_counter = 0
        for iteraction in range(len(lstwords)):
            if iteraction >= len(Lines):
                time.sleep(3)
                line_counter = 0
            display.text(lstwords[iteraction], 0, Lines[line_counter])
            display.show()
            line_counter += 1

def get_random_question():
    """
    It will actually get a random number
    Returns:
        String with the question selected.
    """
    with open("questions.json", "r") as questionsfile:
        questions = json.loads(questionsfile.read())
    questionsfile.close()

    choise = urandom.getrandbits(5)
    return questions[str(choise)]



i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
clear_display()


clear_display(1, 1)
time.sleep_ms(100)
clear_display(0, 1)
print_wrapped(wrapped_text(get_random_question()))
time.sleep(5)
clear_display(1, 1)
time.sleep_ms(200)
clear_display(0, 1)
