# RuneAutoConvo

This is a simple tool to automate the process of clicking through the conversation in RuneScape Classic.
You might want to use RuneLite, as it marks the conversation text in blue, which makes it easier to filter out the action text.

## Installation

You will need to install tesseract to this location: 'C:\Program Files\Tesseract-OCR\tesseract.exe'

## How it works

The tool uses the `pyautogui` library to take screenshots of the game window and then look for the conversation text.

It will filter out and only show the blue text, which is the action text.
If that text contains the word "Continue", it will click "space" to advance the conversation.

If the word "Continue" is not found, it will parse the unfiltered text and look for the word "Continue" in the action text.
Then it will count each line. When it finds a line that starts with a "(" or a "[", it will click the key for the number of lines it counted.


## Warning

I have no idea if this is against the rules of the game, so use at your own risk.
When i've tested it, it have not banned any accounts, but i can't guarantee that it won't in the future.

This is just meant as quality of life tool, and should not give any big game advantage.
