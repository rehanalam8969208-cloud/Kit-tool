from flask import Flask, request, render_template_string, send_file, flash, redirect, url_for
import os
import io
from PIL import Image
import random
import base64

app = Flask(__name__)
app.secret_key = "cyber_secret_key"
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 # 100MB Limit

# ==========================================
# HTML DESIGN (Same as before)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber Photo Toolkit</title>
    <style>
        body { background-color: #0d0d0d; color: #00ff00; font-family: 'Courier New', Courier, monospace; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; flex-direction: column; }
        .container { background: #000; border: 2px solid #00ff00; padding: 20px; border-radius: 10px; box-shadow: 0 0 15px #00ff00; width: 90%; max-width: 500px; text-align: center; }
        h1 { text-shadow: 0 0 10px #00ff00; }
        input, select, button { background: transparent; border: 1px solid #00ff00; color: #00ff00; padding: 10px; margin: 10px 0; width: 100%; box-sizing: border-box; font-family: inherit; font-size: 16px; }
        button { cursor: pointer; font-weight: bold; text-transform: uppercase; transition: 0.3s; }
        button:hover { background: #00ff00; color: #000; box-shadow: 0 0 10px #00ff00; }
        .tab { display: none; }
        .active { display: block; }
        .nav-btn { width: 45%; display: inline-block; margin: 2%; }
    </style>
</head>
<body>
    <div class="container">
        <h1>[ CYBER PHOTO ]</h1>
        <div>
            <button class="nav-btn" onclick="showTab('stego')">Stego</button>
            <button class="nav-btn" onclick="showTab('glitch')">Glitch</button>
        </div>
        <div id="stego" class="tab active">
            <form method="POST" action="/stego" enctype="multipart/form-data">
                <h3>Hide / Extract Message</h3>
                <input type="file" name="image" accept="image/*" required>
                <input type="text" name="message" placeholder="Secret Message (Only to Hide)">
                <select name="action">
                    <option value="hide">Hide Message</option>
                    <option value="extract">Extract Message</option>
                </select>
                <button type="submit">Execute</button>
            </form>
            {% if stego_msg %}<div style="margin-top:20px; border:1px dashed #00ff00; padding:10px;"><b>Result:</b> {{ stego_msg }}</div>{% endif %}
            {% if download_link %}<a href="{{ download_link }}" download><button style="border-color: #00ffff; color: #00ffff;">Download Image</button></a>{% endif %}
        </div>
        <div id="glitch" class="tab">
            <form method="POST" action="/glitch" enctype="multipart/form-data">
                <h3>Glitch / Restore Image</h3>
                <input type="file" name="image" accept="image/*" required>
                <input type="text" name="key" placeholder="Secret Key" required>
                <select name="action">
                    <option value="glitch">Glitch Image</option>
                    <option value="restore">Restore Image</option>
                </select>
                <button type="submit">Execute</button>
            </form>
            {% if glitch_msg %}<div style="margin-top:20px; border:1px dashed #00ff00; padding:10px;"><b>Result:</b> {{ glitch_msg }}</div>{% endif %}
            {% if download_link %}<a href="{{ download_link }}" download><button style="border-color: #00ffff; color: #00ffff;">Download Image</button></a>{% endif %}
        </div>
    </div>
    <script>
        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
        }
    </script>
</body>
</html>
"""

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def text_to_bin(text): return ''.join(format(ord(i), '08b') for i in text)
def bin_to_text(binary):
    str_data = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            try: str_data += chr(int(byte, 2))
            except: pass
    return str_data

# ==========================================
# ROUTES
# ==========================================
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/stego', methods=['POST'])
def stego():
    action = request.form.get('action')
    file = request.files.get('image')
    message = request.form.get('message', '')
    
    if not file: return render_template_string(HTML_TEMPLATE, stego_msg="File upload failed.")
    
    # Original file ka format check karo (.jpg ya .png)
    original_format = file.filename.split('.')[-1].lower()
    if original_format not in ['jpg', 'jpeg', 'png']:
        original_format = 'png' # Default
        
    img = Image.open(file).convert('RGB')
    
    # --- FAST PROCESSING FIX ---
    width, height = img.size
    if width > 1500 or height > 1500:
        img.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
    
    if action == 'hide':
        if not message: return render_template_string(HTML_TEMPLATE, stego_msg="Message is empty.")
        
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
                
        img_io = io.BytesIO()
        # SMART SAVE: Agar jpg tha toh jpg mein save karo (Quality 85%)
        if original_format in ['jpg', 'jpeg']:
            img.save(img_io, 'JPEG', quality=85)
            mime = 'image/jpeg'
        else:
            img.save(img_io, 'PNG')
            mime = 'image/png'
            
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        link = f"data:{mime};base64,{b64}"
        return render_template_string(HTML_TEMPLATE, stego_msg="Message Hidden Successfully!", download_link=link)

    elif action == 'extract':
        pixels = img.load()
        width, height = img.size
        binary_data = ""
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1) + str(g & 1) + str(b & 1)
                if binary_data.endswith('1111111111111110'):
                    return render_template_string(HTML_TEMPLATE, stego_msg=f"Message: {bin_to_text(binary_data[:-16])}")
        return render_template_string(HTML_TEMPLATE, stego_msg="No message found in this image.")

@app.route('/glitch', methods=['POST'])
def glitch():
    action = request.form.get('action')
    file = request.files.get('image')
    key = request.form.get('key', '')
    
    if not file or not key: return render_template_string(HTML_TEMPLATE, glitch_msg="Missing File or Key.")
    
    # Original file ka format check karo
    original_format = file.filename.split('.')[-1].lower()
    if original_format not in ['jpg', 'jpeg', 'png']:
        original_format = 'png'
        
    img = Image.open(file).convert('RGB')
    width, height = img.size
    
    if action == 'glitch':
        pixels = list(img.getdata())
        random.seed(key)
        indices = list(range(len(pixels)))
        random.shuffle(indices)
        
        new_pixels = [None] * len(pixels)
        for i, new_idx in enumerate(indices): new_pixels[new_idx] = pixels[i]
            
        new_img = Image.new('RGB', (width, height))
        new_img.putdata(new_pixels)
        
        img_io = io.BytesIO()
        # SMART SAVE
        if original_format in ['jpg', 'jpeg']:
            new_img.save(img_io, 'JPEG', quality=85)
            mime = 'image/jpeg'
        else:
            new_img.save(img_io, 'PNG')
            mime = 'image/png'
            
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        link = f"data:{mime};base64,{b64}"
        return render_template_string(HTML_TEMPLATE, glitch_msg="Image Glitched Successfully!", download_link=link)

    elif action == 'restore':
        glitched_pixels = list(img.getdata())
        random.seed(key)
        indices = list(range(len(glitched_pixels)))
        random.shuffle(indices)
        
        original_pixels = [None] * len(glitched_pixels)
        for i, new_idx in enumerate(indices): original_pixels[i] = glitched_pixels[new_idx]
            
        new_img = Image.new('RGB', (width, height))
        new_img.putdata(original_pixels)
        
        img_io = io.BytesIO()
        # SMART SAVE
        if original_format in ['jpg', 'jpeg']:
            new_img.save(img_io, 'JPEG', quality=85)
            mime = 'image/jpeg'
        else:
            new_img.save(img_io, 'PNG')
            mime = 'image/png'
            
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        link = f"data:{mime};base64,{b64}"
        return render_template_string(HTML_TEMPLATE, glitch_msg="Image Restored Successfully!", download_link=link)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
