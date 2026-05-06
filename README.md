# steganosaurus.
Image Steganography automation with Python 

A command-line Python tool that hides and retrieves secret text messages inside PNG image files using the Least Significant Bit (LSB) method.
Developed during coursework in Scripting for Administration, Automation and Security at Michigan Technological University.

What is Steganography?
Steganography is the practice of concealing data within another file so that the existence of the message is hidden entirely. Unlike encryption, which scrambles a message to make it unreadable, steganography hides the fact that a message is being sent at all.

How It Works
This tool uses the Least Significant Bit (LSB) method to embed binary data into the pixels of a PNG image.
Every pixel in an RGB image has three color channels — red, green, and blue — each stored as a value from 0 to 255. By modifying only the last (least significant) bit of the blue channel, the color change is at most a difference of 1 out of 255, which is completely invisible to the human eye.
PNG format is used because it is lossless — no pixel data is altered during saving. JPEG compression would destroy the embedded bits, making recovery impossible.
A unique delimiter string is appended to the end of the message before encoding so the decoder knows exactly where the message ends.

Requirements
Python 3.x
Pillow library
Install Pillow with:
pip install Pillow


Setup
Place the following files in the same folder before running the script:
steganography_tool.py – the main script
cover.png – Any PNG image to act as the carrier
secret.txt – A plain text file containing your message
A standard 1920x1080 PNG image can hold over 250,000 characters. Larger images support larger messages.

Usage
Run the script from the command line:
python steganography_tool.py

You will be presented with a menu:
Select an option:
  [E] Encode - Hide a message in an image
  [D] Decode - Extract a message from an image
  [Q] Quit

To hide a message: Select E. The script reads secret.txt, embeds the message into cover.png, and saves the result as stego_output.png.
To recover a message: Select D. The script scans stego_output.png, extracts the hidden bits, and saves the recovered message to recovered_message.txt.

Configuration
Two variables at the top of the script can be adjusted:
DEBUG (line 14) — Set to True for detailed step-by-step output during testing. Set to False for clean minimal output. Recommended to disable for large images as it generates significant terminal output.
DELIMITER (line 18) — The string appended to mark the end of the hidden message. Default is #####. Do not change this unless necessary, and ensure it matches across both encode and decode runs.

Output Files

stego_output.png – The carrier image with the hidden message embedded
recovered_message.txt – The extracted message after decoding


Troubleshooting
ModuleNotFoundError: No module named 'PIL' Pillow is not installed. Run pip install Pillow and try again. If you have multiple Python versions, try python -m pip install Pillow.
[ERROR] 'cover.png' not found Ensure the file is named exactly cover.png (lowercase) and is in the same folder as the script.
[ERROR] Message too large The message exceeds the image's capacity. Switch to a larger PNG image.
[ERROR] Delimiter not found during Decode The image does not contain a hidden message, or it was saved as JPEG after encoding which destroys the embedded bits. Always use PNG throughout the process.
Permission Denied A required file is open in another application. Close it and try again.

Author
Dawson Erva Michigan Technological University — Applied Computing, Information Technology dlerva@mtu.edu
