from flask import Flask, request, render_template_string, redirect, url_for
import io
from PIL import Image
import random
import base64

app = Flask(__name__)
app.secret_key = "cyber_secret_key"
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 # 100MB Limit

# ==========================================
# BASE HTML LAYOUT (PROFESSIONAL HACKER THEME)
# ==========================================
BASE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        background-color: #0a0a0a;
        color: #00ff41;
        font-family: 'Share Tech Mono', 'Courier New', monospace;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
        background-size: 20px 20px;
        padding: 20px;
    }

    .container {
        background: rgba(0, 0, 0, 0.9);
        border: 1px solid #00ff41;
        padding: 40px;
        border-radius: 5px;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.2), inset 0 0 20px rgba(0, 255, 65, 0.1);
        width: 100%;
        max-width: 600px;
        position: relative;
        overflow: hidden;
    }

    .container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: #00ff41;
        box-shadow: 0 0 10px #00ff41;
    }

    h1, h2, h3 { text-shadow: 0 0 5px #00ff41; text-align: center; letter-spacing: 2px; }
    
    .subtitle { text-align: center; color: #008f11; margin-bottom: 30px; font-size: 14px; }

    /* Main Menu Buttons */
    .main-menu { display: flex; flex-direction: column; gap: 20px; margin-top: 30px; }
    
    .main-btn {
        display: block;
        text-decoration: none;
        background: transparent;
        border: 1px solid #008f11;
        color: #00ff41;
        padding: 20px;
        text-align: center;
        font-size: 20px;
        text-transform: uppercase;
        letter-spacing: 3px;
        transition: all 0.3s ease;
        position: relative;
        cursor: pointer;
    }
    
    .main-btn:hover {
        background: rgba(0, 255, 65, 0.1);
        border-color: #00ff41;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
        text-shadow: 0 0 10px #00ff41;
    }

    .main-btn span { display: block; font-size: 12px; color: #008f11; margin-top: 5px; letter-spacing: 1px;}

    /* Form Elements */
    .form-group { margin-bottom: 20px; }
    label { display: block; margin-bottom: 8px; font-size: 14px; color: #00ff41;}
    
    input[type="file"], input[type="text"], select {
        width: 100%;
        background: #050505;
        border: 1px solid #008f11;
        color: #00ff41;
        padding: 12px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 16px;
        outline: none;
        transition: border 0.3s;
    }
    
    input:focus, select:focus { border-color: #00ff41; box-shadow: 0 0 10px rgba(0, 255, 65, 0.2); }
    
    input[type="file"]::file-selector-button {
        background: #00ff41;
        color: #000;
        border: none;
        padding: 8px 15px;
        cursor: pointer;
        font-weight: bold;
        font-family: 'Share Tech Mono', monospace;
    }

    button[type="submit"] {
        width: 100%;
        background: #00ff41;
        color: #000;
        border: none;
        padding: 15px;
        font-size: 18px;
        font-weight: bold;
        font-family: 'Share Tech Mono', monospace;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s;
        margin-top: 10px;
    }
    
    button[type="submit"]:hover { background: #00cc33; box-shadow: 0 0 15px #00ff41; }

    /* Result Terminal Box */
    .result-box {
        margin-top: 30px;
        background: #000;
        border-left: 4px solid #00ff41;
        padding: 15px;
        font-size: 14px;
        word-break: break-all;
        animation: slideIn 0.3s ease-out;
    }
    .result-title { color: #008f11; font-size: 12px; margin-bottom: 5px; }
    
    .download-btn {
        display: block;
        width: 100%;
        background: transparent;
        border: 1px solid #00ffff;
        color: #00ffff;
        padding: 12px;
        text-align: center;
        text-decoration: none;
        margin-top: 15px;
        transition: 0.3s;
    }
    .download-btn:hover { background: rgba(0, 255, 255, 0.1); box-shadow: 0 0 10px #00ffff; }

    .back-link { display: block; text-align: center; margin-top: 20px; color: #008f11; text-decoration: none; font-size: 14px; }
    .back-link:hover { color: #00ff41; text-shadow: 0 0 5px #00ff41; }

    @keyframes slideIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
</style>
"""

# ==========================================
# PAGES TEMPLATES
# ==========================================

# 1. Main Menu
HTML_MAIN = BASE_CSS + """
<div class="container">
    <h1>[ CYBER PHOTO ]</h1>
    <div class="subtitle">Advanced Steganography & Glitch Suite</div>
    
    <div class="main-menu">
        <a href="/stego" class="main-btn">
            STEGO MODULE
            <span>Hide & Extract Secret Messages</span>
        </a>
        <a href="/glitch" class="main-btn">
            GLITCH MODULE
            <span>Corrupt & Restore Image Pixels</span>
        </a>
    </div>
</div>
"""

# 2. Stego Page
HTML_STEGO = BASE_CSS + """
<div class="container">
    <h2>STEGO MODULE</h2>
    <div class="subtitle">Hide / Extract Secret Payload</div>
    
    <form method="POST" enctype="multipart/form-data">
        <div class="form-group">
            <label>> Select Target Image</label>
            <input type="file" name="image" accept="image/*" required>
        </div>
        
        <div class="form-group">
            <label>> Payload (Text to Hide)</label>
            <input type="text" name="message" placeholder="Enter secret message...">
        </div>
        
        <div class="form-group">
            <label>> Execution Mode</label>
            <select name="action">
                <option value="hide">Inject Payload (Hide)</option>
                <option value="extract">Extract Payload (Read)</option>
            </select>
        </div>
        
        <button type="submit">EXECUTE COMMAND</button>
    </form>
    
    {% if result %}
        <div class="result-box">
            <div class="result-title">> TERMINAL OUTPUT:</div>
            {{ result }}
        </div>
    {% endif %}
    
    {% if download_link %}
        <a href="{{ download_link }}" download class="download-btn">[ DOWNLOAD PROCESSED IMAGE ]</a>
    {% endif %}
    
    <a href="/" class="back-link">.. / Return to Main Menu</a>
</div>
"""

# 3. Glitch Page
HTML_GLITCH = BASE_CSS + """
<div class="container">
    <h2>GLITCH MODULE</h2>
    <div class="subtitle">Pixel Corruption / Restoration</div>
    
    <form method="POST" enctype="multipart/form-data">
        <div class="form-group">
            <label>> Select Target Image</label>
            <input type="file" name="image" accept="image/*" required>
        </div>
        
        <div class="form-group">
            <label>> Encryption Key (Password)</label>
            <input type="text" name="key" placeholder="Enter secret key..." required>
        </div>
        
        <div class="form-group">
            <label>> Execution Mode</label>
            <select name="action">
                <option value="glitch">Corrupt Image (Glitch)</option>
                <option value="restore">Restore Image (Fix)</option>
            </select>
        </div>
        
        <button type="submit">EXECUTE COMMAND</button>
    </form>
    
    {% if result %}
        <div class="result-box">
            <div class="result-title">> TERMINAL OUTPUT:</div>
            {{ result }}
        </div>
    {% endif %}
    
    {% if download_link %}
        <a href="{{ download_link }}" download class="download-btn">[ DOWNLOAD PROCESSED IMAGE ]</a>
    {% endif %}
    
    <a href="/" class="back-link">.. / Return to Main Menu</a>
</div>
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
    return render_template_string(HTML_MAIN)

@app.route('/stego', methods=['GET', 'POST'])
def stego():
    if request.method == 'GET':
        return render_template_string(HTML_STEGO)
        
    action = request.form.get('action')
    file = request.files.get('image')
    message = request.form.get('message', '')
    
    if not file: return render_template_string(HTML_STEGO, result="ERROR: File upload failed.")
    
    original_format = file.filename.split('.')[-1].lower()
    if original_format not in ['jpg', 'jpeg', 'png']: original_format = 'png'
        
    img = Image.open(file).convert('RGB')
    
    # Auto resize if too big (Speed Optimization)
    if img.width > 1500 or img.height > 1500:
        img.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
    
    if action == 'hide':
        if not message: return render_template_string(HTML_STEGO, result="ERROR: Message is empty.")
        
        binary_msg = text_to_bin(message) + '1111111111111110'
        data_index = 0
        pixels = img.load()
        
        for y in range(img.height):
            for x in range(img.width):
                if data_index < len(binary_msg):
                    r, g, b = pixels[x, y]
                    if data_index < len(binary_msg): r = r & ~1 | int(binary_msg[data_index]); data_index += 1
                    if data_index < len(binary_msg): g = g & ~1 | int(binary_msg[data_index]); data_index += 1
                    if data_index < len(binary_msg): b = b & ~1 | int(binary_msg[data_index]); data_index += 1
                    pixels[x, y] = (r, g, b)
                else: break
            if data_index >= len(binary_msg): break
                
        img_io = io.BytesIO()
        if original_format in ['jpg', 'jpeg']:
            img.save(img_io, 'JPEG', quality=85); mime = 'image/jpeg'
        else:
            img.save(img_io, 'PNG'); mime = 'image/png'
            
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        link = f"data:{mime};base64,{b64}"
        return render_template_string(HTML_STEGO, result="SUCCESS: Payload injected successfully. File ready.", download_link=link)

    elif action == 'extract':
        pixels = img.load()
        binary_data = ""
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1) + str(g & 1) + str(b & 1)
                if binary_data.endswith('1111111111111110'):
                    return render_template_string(HTML_STEGO, result=f"DECRYPTED MESSAGE:<br><br><span style='color:#fff; font-size:18px;'>\"{bin_to_text(binary_data[:-16])}\"</span>")
        return render_template_string(HTML_STEGO, result="ERROR: No hidden data found in this image.")

@app.route('/glitch', methods=['GET', 'POST'])
def glitch():
    if request.method == 'GET':
        return render_template_string(HTML_GLITCH)
        
    action = request.form.get('action')
    file = request.files.get('image')
    key = request.form.get('key', '')
    
    if not file or not key: return render_template_string(HTML_GLITCH, result="ERROR: Missing File or Encryption Key.")
    
    original_format = file.filename.split('.')[-1].lower()
    if original_format not in ['jpg', 'jpeg', 'png']: original_format = 'png'
        
    img = Image.open(file).convert('RGB')
    
    if action == 'glitch':
        pixels = list(img.getdata())
        random.seed(key)
        indices = list(range(len(pixels)))
        random.shuffle(indices)
        
        new_pixels = [None] * len(pixels)
        for i, new_idx in enumerate(indices): new_pixels[new_idx] = pixels[i]
            
        new_img = Image.new('RGB', (img.width, img.height))
        new_img.putdata(new_pixels)
        
        img_io = io.BytesIO()
        if original_format in ['jpg', 'jpeg']:
            new_img.save(img_io, 'JPEG', quality=85); mime = 'image/jpeg'
        else:
            new_img.save(img_io, 'PNG'); mime = 'image/png'
            
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        link = f"data:{mime};base64,{b64}"
        return render_template_string(HTML_GLITCH, result="SUCCESS: Pixels corrupted. Remember your Key!", download_link=link)

    elif action == 'restore':
        glitched_pixels = list(img.getdata())
        random.seed(key)
        indices = list(range(len(glitched_pixels)))
        random.shuffle(indices)
        
        original_pixels = [None] * len(glitched_pixels)
        for i, new_idx in enumerate(indices): original_pixels[i] = glitched_pixels[new_idx]
            
        new_img = Image.new('RGB', (img.width, img.height))
        new_img.putdata(original_pixels)
        
        img_io = io.BytesIO()
        if original_format in ['jpg', 'jpeg']:
            new_img.save(img_io, 'JPEG', quality=85); mime = 'image/jpeg'
        else:
            new_img.save(img_io, 'PNG'); mime = 'image/png'
            
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        link = f"data:{mime};base64,{b64}"
        return render_template_string(HTML_GLITCH, result="SUCCESS: Image restored to original state.", download_link=link)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
