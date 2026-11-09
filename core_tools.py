from PIL import Image
import os
import sys
import time
import random

GALLERY_PATH = "/storage/emulated/0/DCIM/Camera/"

def find_photo(image_name):
    if os.path.exists(image_name):
        return image_name
    paths = [os.path.join(GALLERY_PATH, image_name), os.path.join(os.getcwd(), image_name)]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def text_to_bin(text):
    return ''.join(format(ord(i), '08b') for i in text)

def bin_to_text(binary):
    str_data = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            try: str_data += chr(int(byte, 2))
            except: pass
    return str_data

def hide_message(image_path, message, output_path):
    real_path = find_photo(image_path)
    if not real_path: return print("[-] Photo nahi mili.")
    
    try: img = Image.open(real_path).convert('RGB')
    except Exception as e: return print(f"[-] Error: {e}")
    
    binary_msg = text_to_bin(message) + '1111111111111110'
    data_index = 0
    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            if data_index < len(binary_msg):
                r, g, b = pixels[x, y]
                if data_index < len(binary_msg): r = r & ~1 | int(binary_msg[data_index]); data_index += 1
                if data_index < len(binary_msg): g = g & ~1 | int(binary_msg[data_index]); data_index += 1
                if data_index < len(binary_msg): b = b & ~1 | int(binary_msg[data_index]); data_index += 1
                pixels[x, y] = (r, g, b)
            else: break
        if data_index >= len(binary_msg): break
            
    if not output_path.endswith('.png'): output_path += '.png'
    img.save(output_path)
    print(f"\n[+] Success! Secret Message chhup gaya hai: {output_path}")

def extract_message(image_path):
    real_path = find_photo(image_path)
    if not real_path: return print("[-] Photo nahi mili.")
    
    try: img = Image.open(real_path).convert('RGB')
    except Exception as e: return print(f"[-] Error: {e}")
    
    pixels = img.load()
    width, height = img.size
    binary_data = ""
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1) + str(g & 1) + str(b & 1)
            if binary_data.endswith('1111111111111110'):
                print("\n[+] Secret Message mil gaya:\n" + "="*30)
                print(bin_to_text(binary_data[:-16]))
                print("="*30)
                return
    print("[-] Koi message nahi mila.")

def glitch_image(image_path, output_path, key):
    real_path = find_photo(image_path)
    if not real_path: return print("[-] Photo nahi mili.")
    
    try: img = Image.open(real_path).convert('RGB')
    except Exception as e: return print(f"[-] Error: {e}")
    
    width, height = img.size
    pixels = list(img.getdata())
    
    random.seed(key)
    indices = list(range(len(pixels)))
    random.shuffle(indices)
    
    new_pixels = [None] * len(pixels)
    for i, new_idx in enumerate(indices): new_pixels[new_idx] = pixels[i]
        
    new_img = Image.new('RGB', (width, height))
    new_img.putdata(new_pixels)
    if not output_path.endswith('.png'): output_path += '.png'
    new_img.save(output_path)
    print(f"\n[+] Photo Glitch ho gayi: {output_path}\n[!] Key yaad rakhna: {key}")

def restore_image(image_path, output_path, key):
    real_path = find_photo(image_path)
    if not real_path: return print("[-] Photo nahi mili.")
    
    try: img = Image.open(real_path).convert('RGB')
    except Exception as e: return print(f"[-] Error: {e}")
    
    width, height = img.size
    glitched_pixels = list(img.getdata())
    
    random.seed(key)
    indices = list(range(len(glitched_pixels)))
    random.shuffle(indices)
    
    original_pixels = [None] * len(glitched_pixels)
    for i, new_idx in enumerate(indices): original_pixels[i] = glitched_pixels[new_idx]
        
    new_img = Image.new('RGB', (width, height))
    new_img.putdata(original_pixels)
    if not output_path.endswith('.png'): output_path += '.png'
    new_img.save(output_path)
    print(f"\n[+] Photo wapas sahi ho gayi: {output_path}")
