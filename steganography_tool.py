# =============================================================================
# Image Steganography Tool
# Author: Dawson Erva
# Course: SAT 3310 - Scripting for Administration, Automation and Security
# Description: Hides and retrieves text from a file inside a PNG image
#              using the Least Significant Bit (LSB) method. 
#  Note: the image file and text file should be in the same folder as this 
#        script at run time. Image file should be named "cover.png" and the 
#        text file should be named : "secret.txt"
# =============================================================================


from PIL import Image
import os
import sys

# --- Debug Flag ---
# Set to True to print step-by-step progress, False for clean output
DEBUG = True

# --- Delimiter ---
# This unique string marks the end of the hidden message during decoding
DELIMITER = "#####"


def debug_print(message):
    """Prints a message only if DEBUG mode is enabled."""
    if DEBUG:
        print(f"  [DEBUG] {message}")


def text_to_binary(text):
    """Converts a string of text into a binary string."""
    binary = ""
    for char in text:
        # Convert each character to its 8-bit binary representation
        binary += format(ord(char), "08b")
    debug_print(f"Converted text to binary ({len(binary)} bits total)")
    return binary


def binary_to_text(binary):
    """Converts a binary string back into readable text."""
    text = ""
    # Process 8 bits at a time (one character)
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text


# =============================================================================
# ENCODE FUNCTION
# Reads a secret message from secret.txt and hides it inside cover.png
# =============================================================================
def encode_message():
    print("\n--- ENCODE MODE ---")

    # --- File I/O: Read the secret message ---
    secret_file = "secret.txt"
    if not os.path.exists(secret_file):
        print(f"[ERROR] '{secret_file}' not found. Please create it with your secret message.")
        return

    with open(secret_file, "r") as f:
        message = f.read()
    print(f"[+] Secret message loaded from '{secret_file}' ({len(message)} characters)")
    debug_print(f"Message content: {message[:50]}{'...' if len(message) > 50 else ''}")

    # --- File I/O: Open the cover image ---
    cover_file = "cover.png"
    if not os.path.exists(cover_file):
        print(f"[ERROR] '{cover_file}' not found. Please provide a PNG image.")
        return

    image = Image.open(cover_file)
    # Ensure image is in RGB mode for consistent pixel access
    image = image.convert("RGB")
    pixels = list(image.getdata())
    print(f"[+] Cover image loaded: '{cover_file}' ({image.width}x{image.height}, {len(pixels)} pixels)")

    # --- Convert message + delimiter to binary ---
    full_message = message + DELIMITER
    binary_message = text_to_binary(full_message)
    total_bits = len(binary_message)

    # --- Condition Check: Does the image have enough pixels to hold the message? ---
    if total_bits > len(pixels):
        print(f"[ERROR] Message too large! Need {total_bits} pixels, image only has {len(pixels)}.")
        return
    print(f"[+] Message fits: {total_bits} bits needed, {len(pixels)} pixels available")

    # --- Loop: Embed each bit into the LSB of the blue channel ---
    encoded_pixels = []
    bit_index = 0

    for i, pixel in enumerate(pixels):
        r, g, b = pixel

        # Condition check: If there are still bits to embed, modify the LSB
        if bit_index < total_bits:
            # Clear the last bit of blue, then set it to the message bit
            new_b = (b & 0b11111110) | int(binary_message[bit_index])
            encoded_pixels.append((r, g, new_b))
            bit_index += 1
            debug_print(f"Pixel {i}: blue {b} -> {new_b} (embedded bit '{binary_message[bit_index-1]}')")
        else:
            # No more bits to embed; keep pixel unchanged
            encoded_pixels.append((r, g, b))

    # --- File I/O: Save the stego image ---
    output_file = "stego_output.png"
    stego_image = Image.new("RGB", image.size)
    stego_image.putdata(encoded_pixels)
    stego_image.save(output_file)

    # --- Display: Confirm success ---
    print(f"\n[SUCCESS] Message hidden successfully!")
    print(f"  - Bits embedded : {bit_index}")
    print(f"  - Output file   : '{output_file}'")
    print(f"  - Image size    : {image.width}x{image.height}")


# =============================================================================
# DECODE FUNCTION
# Extracts a hidden message from stego_output.png
# =============================================================================
def decode_message():
    print("\n--- DECODE MODE ---")

    # --- File I/O: Open the stego image ---
    stego_file = "stego_output.png"
    if not os.path.exists(stego_file):
        print(f"[ERROR] '{stego_file}' not found. Run Encode first.")
        return

    image = Image.open(stego_file).convert("RGB")
    pixels = list(image.getdata())
    print(f"[+] Stego image loaded: '{stego_file}' ({image.width}x{image.height})")

    # --- Loop: Extract the LSB from the blue channel of each pixel ---
    binary_message = ""
    for i, pixel in enumerate(pixels):
        r, g, b = pixel
        # Extract the least significant bit of the blue channel
        lsb = b & 1
        binary_message += str(lsb)
        debug_print(f"Pixel {i}: blue={b}, LSB={lsb}")

        # --- Condition Check: Every 8 bits, check for the delimiter ---
        if len(binary_message) % 8 == 0:
            # Decode what we have so far and check if delimiter has appeared
            current_text = binary_to_text(binary_message)
            if DELIMITER in current_text:
                # Stop — we have the full message
                recovered = current_text.split(DELIMITER)[0]
                break
    else:
        # Loop finished without finding the delimiter
        print("[ERROR] Delimiter not found. Image may not contain a hidden message.")
        return

    # --- Display: Print the recovered secret message ---
    print(f"\n[SUCCESS] Hidden message recovered!")
    print(f"  - Characters extracted : {len(recovered)}")
    print(f"\n--- SECRET MESSAGE ---")
    print(recovered)
    print(f"----------------------")

    # --- File I/O: Save the recovered message to a file ---
    output_file = "recovered_message.txt"
    with open(output_file, "w") as f:
        f.write(recovered)
    print(f"\n[+] Message also saved to '{output_file}'")


# =============================================================================
# MAIN — Menu / Entry Point
# =============================================================================
def main():
    print("=" * 45)
    print("   Image Steganography Tool - SAT 3310")
    print("=" * 45)
    print(f"   Debug mode: {'ON' if DEBUG else 'OFF'}")
    print("=" * 45)

    # Loop: Keep showing the menu until the user quits
    while True:
        print("\nSelect an option:")
        print("  [E] Encode - Hide a message in an image")
        print("  [D] Decode - Extract a message from an image")
        print("  [Q] Quit")

        # Input from user
        choice = input("\nEnter choice (E/D/Q): ").strip().upper()

        # Condition check: Route to the correct function
        if choice == "E":
            encode_message()
        elif choice == "D":
            decode_message()
        elif choice == "Q":
            print("\n[+] Exiting. Goodbye!")
            sys.exit(0)
        else:
            print("[!] Invalid choice. Please enter E, D, or Q.")


# --- Entry point ---
if __name__ == "__main__":
    main()