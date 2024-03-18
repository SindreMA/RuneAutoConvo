import pygetwindow as gw
import pyautogui
import pytesseract
import re
import matplotlib.pyplot as plt
import numpy as np
import pydirectinput
from PIL import Image

# Configure pytesseract to use the Tesseract-OCR location
# You might need to update this path according to your Tesseract-OCR installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def find_numbers_in_image(image):
    # Use OCR to find text in the screenshot
    text = pytesseract.image_to_string(image)

    #

    print(f"Found text: {text}")

    if (text != ""):
        return []
    # Use regular expression to find numbers surrounded by brackets
    numbers = re.findall(r'\[(\d+)\]', text)
    return numbers

def main():
    # Get all windows with 'RuneLite' in the title
    runelite_windows = [win for win in gw.getWindowsWithTitle('RuneLite') if 'RuneLite' in win.title]

    for window in runelite_windows:
        try:

            # if the window is not active, skip it
            if not window.isActive:
                continue


            # Calculate the position for the bottom left part of the window
            window_left, window_top, window_width, window_height = window.left, window.top, window.width, window.height


            # select region of the window with 100px offset from the bottom
            #region = (left + 20, top + height - 220, 650, 180)  # Adjust based on your needs

            # Set the relative sizes as percentages
            margin_left_percentage = 2  # Margin from the left edge of the window as a percentage
            margin_bottom_percentage = 8  # Margin from the bottom edge of the window as a percentage
            region_width_percentage = 28  # Width of the region as a percentage of the window's width
            region_height_percentage = 16  # Height of the region as a percentage of the window's height

           # Calculate the actual pixel values for margins and size
            margin_left = min(int((window_width / 100) * margin_left_percentage), 15)
            margin_bottom = min(int((window_height / 100) * margin_bottom_percentage), 50)
            region_width = 720 #min(int((window_width / 100) * region_width_percentage), 720)
            # Calculate the height and make sure it does not exceed 200 pixels
            region_height = min(int((window_height / 100) * region_height_percentage), 200)

            # Calculate the position for the bottom left part of the region within the window,
            # considering the window's actual position
            region_left = window_left + margin_left
            region_top = window_top + window_height - margin_bottom - region_height

            # Define the region for the screenshot
            # Note: Adjusted to use the potentially limited height
            region = (region_left, region_top, region_width, region_height)

            # Take a screenshot of the bottom left part of the window
            screenshot = pyautogui.screenshot(region=region)

            screenshot_np = np.array(screenshot)

            black_threshold = 80  # Adjust this value based on how you define "black"
            blue_min = np.array([0, 0, 100])  # Minimum RGB values for a pixel to be considered blue
            blue_max = np.array([100, 100, 255])  # Maximum RGB values for a pixel to be considered blue

            # Create a mask for blue and black pixels
            blue_mask = ((screenshot_np >= blue_min) & (screenshot_np <= blue_max)).all(axis=-1)
            black_mask = (screenshot_np < black_threshold).all(axis=-1)
            combined_mask = blue_mask | black_mask

            # Apply the mask
            filtered_pixels = np.zeros_like(screenshot_np)
            filtered_pixels[combined_mask] = screenshot_np[combined_mask]

            # Convert back to an image and save or show it
            filtered_image = Image.fromarray(filtered_pixels)

            # screenshot_np to Image
            screenshot.save('screenshot.png')
            #screenshot = filtered_image
            filtered_image.save('screenshot_np.png')
            # Use OCR to find numbers in the image
            text = pytesseract.image_to_string(screenshot)
            blueText = str(pytesseract.image_to_string(filtered_image))

            # Text contains "Continue" case insensitive
            if text.lower().find("continue") != -1:
                print("Clicking to continue")
                # Click space to continue
                pydirectinput.press('space')
            else:
                if blueText.strip() == "":
                    continue
                text = pytesseract.image_to_string(screenshot)
                print(f"Found text: {text}")

                lines = text.split("\n")

                index = 0
                for line in lines:
                    if line == "":
                        continue
                    print(f"Checking line: {line}")
                    # If the line starts with parentheses or brackets, press the corresponding key
                    if line.startswith("(") or line.startswith("["):
                        print(f"Pressing {index}")
                        pydirectinput.press(str(index))
                        break
                    index += 1
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        main()
        # Sleep for 100ms to avoid using too much CPU
        pyautogui.sleep(0.1)


