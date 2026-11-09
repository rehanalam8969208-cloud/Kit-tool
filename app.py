from flask import Flask, request, render_template_string
import io
from PIL import Image
import random
import base64

app = Flask(__name__)
app.secret_key = "cyber_secret_key"
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 # 100MB Limit

# ==========================================
# FULL ADVANCED HACKER CSS DESIGN
# ==========================================
BASE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        background-color: #030a03;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
        background-size: 40px 40px;
        background-position: center;
    }

    .wrapper {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        width: 100%;
        max-width: 600px; /* Mobile first approach */
        margin: 0 auto;
    }

    /* HEADER SECTION */
    .header {
        width: 100%;
        height: 200px;
        background-image: url('https://i.ibb.co/6803xK5/hacker-bg.jpg'); /* Fallback hacker image */
        background-size: cover;
        background-position: center;
        border: 2px solid #00ff41;
        border-bottom: none;
        border-radius: 10px 10px 0 0;
        position: relative;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        display: flex;
        justify-content: space-between;
        padding: 15px;
        background-color: rgba(0,0,0,0.8);
        background-blend-mode: overlay;
    }

    .header-left h1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 28px;
        font-style: italic;
        color: #fff;
        text-shadow: 0 0 10px #00ff41;
        line-height: 1;
        margin-bottom: 5px;
    }
    .header-left h1 span { color: #00ff41; }
    .header-left .sub { font-size: 12px; color: #00ff41; letter-spacing: 2px; }
    
    .status-box {
        background: rgba(0,0,0,0.8);
        border: 1px solid #00ff41;
        padding: 8px;
        font-size: 11px;
        margin-top: 15px;
        display: inline-block;
    }
    .status-box div { margin-bottom: 4px; }
    .status-box span { color: #fff; }

    .header-right {
        text-align: right;
        font-size: 14px;
        color: #00ff41;
        text-shadow: 0 0 5px #00ff41;
        line-height: 1.5;
        font-weight: bold;
    }

    /* MAIN CONTAINER */
    .main-container {
        width: 100%;
        background: rgba(5, 15, 5, 0.9);
        border: 2px solid #00ff41;
        border-radius: 0 0 10px 10px;
        padding: 20px;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.2);
        margin-bottom: 20px;
    }

    /* MODULE CARDS */
    .module-card {
        border: 1px solid #00ff41;
        background: rgba(0, 255, 65, 0.05);
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 5px;
        position: relative;
        display: flex;
        gap: 15px;
        align-items: center;
    }

    /* Glowing Decorative Corners */
    .module-card::before, .module-card::after {
        content: ''; position: absolute; width: 10px; height: 10px; border: 2px solid #00ff41;
    }
    .module-card::before { top: -1px; left: -1px; border-right: none; border-bottom: none; }
    .module-card::after { bottom: -1px; right: -1px; border-left: none; border-top: none; }

    /* Left Icon Area */
    .module-icon {
        width: 80px;
        height: 80px;
        border: 2px solid #00ff41;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 30px;
        background: rgba(0, 255, 65, 0.1);
        box-shadow: inset 0 0 15px rgba(0, 255, 65, 0.5);
        flex-shrink: 0;
    }

    /* Right Form Area */
    .module-form { flex: 1; }
    .module-form h2 {
        font-family: 'Orbitron', sans-serif;
        font-size: 20px;
        color: #00ff41;
        margin-bottom: 5px;
        text-shadow: 0 0 5px #00ff41;
    }
    .module-form p { font-size: 12px; color: #00aa2b; margin-bottom: 15px; font-style: italic;}

    /* Custom Inputs */
    .input-group {
        display: flex;
        align-items: center;
        background: #000;
        border: 1px solid #00ff41;
        margin-bottom: 10px;
        padding: 0;
    }
    .input-icon {
        padding: 10px;
        background: rgba(0, 255, 65, 0.2);
        border-right: 1px solid #00ff41;
        font-size: 16px;
    }
    input[type="file"], input[type="text"] {
        width: 100%;
        background: transparent;
        border: none;
        color: #fff;
        padding: 10px;
        font-family: 'Share Tech Mono', monospace;
        outline: none;
        font-size: 14px;
    }
    input[type="file"]::file-selector-button {
        background: #00ff41; color: #000; border: none; padding: 5px 10px; cursor: pointer; font-weight: bold; margin-right: 10px;
    }

    /* Radio Buttons */
    .radio-group { display: flex; gap: 15px; margin-bottom: 15px; font-size: 14px; }
    .radio-group label { display: flex; align-items: center; cursor: pointer; }
    .radio-group input[type="radio"] { display: none; }
    .radio-btn {
        width: 16px; height: 16px; border: 2px solid #00ff41; border-radius: 50%; margin-right: 8px; display: inline-block;
    }
    .radio-group input[type="radio"]:checked + .radio-btn { background: #00ff41; box-shadow: 0 0 10px #00ff41; }

    /* Big Action Buttons */
    .action-btn {
        width: 100%;
        background: #00ff41;
        color: #000;
        border: none;
        padding: 15px;
        font-family: 'Orbitron', sans-serif;
        font-size: 18px;
        font-weight: 900;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 2px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
        transition: all 0.3s;
        clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
    }
    .action-btn:hover { background: #fff; box-shadow: 0 0 25px #00ff41; }

    /* Result Terminal Box */
    .result-box {
        background: #000;
        border-left: 4px solid #00ff41;
        padding: 15px;
        font-size: 14px;
        margin-bottom: 15px;
        animation: slideIn 0.3s ease-out;
    }
    .download-btn {
        display: block; width: 100%; background: transparent; border: 1px solid #00ffff; color: #00ffff;
        padding: 12px; text-align: center; text-decoration: none; margin-top: 10px; text-transform: uppercase;
    }

    /* FOOTER */
    .footer {
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #00ff41;
        padding-top: 15px;
        margin-top: 10px;
        font-size: 10px;
        text-align: center;
    }
    .footer div { flex: 1; border-right: 1px solid #00aa2b; }
    .footer div:last-child { border-right: none; }
    .footer span { display: block; font-size: 14px; color: #fff; margin-top: 5px; }

    /* Hidden Utility Classes */
    .hidden { display: none; }
    
    @keyframes slideIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
</style>
"""

# ==========================================
# MAIN DASHBOARD HTML
# ==========================================
HTML_MAIN = BASE_CSS + """
<div class="wrapper">
    <div class="header">
        <div class="header-left">
            <h1>CYBER<br><span>PHOTO</span></h1>
            <div class="sub">HACKER EDITION ///</div>
            <div class="status-box">
                <div>> Status : <span>Online</span></div>
                <div>> Tools  : <span>2 Modules</span></div>
                <div>> Version: <span>v2.0.0</span></div>
            </div>
        </div>
        <div class="header-right">
            Encrypt<br>Hide<br>Protect...
        </div>
    </div>

    <div class="main-container">
        <!-- STEGO MODULE CARD -->
        <div class="module-card">
            <div class="module-icon">📸</div>
            <div class="module-form">
                <h2>STEGO MODULE</h2>
                <p>Hide / Extract Secret Payload ///</p>
                <form method="POST" action="/stego" enctype="multipart/form-data" id="stegoForm">
                    <div class="input-group">
                        <span class="input-icon">📁</span>
                        <input type="file" name="image" accept="image/*" required>
                    </div>
                    <div class="input-group">
                        <span class="input-icon">💬</span>
                        <input type="text" name="message" placeholder="Enter Secret Message...">
                    </div>
                    <div class="radio-group">
                        <span>Mode :</span>
                        <label><input type="radio" name="action" value="hide" checked><span class="radio-btn"></span> Hide</label>
                        <label><input type="radio" name="action" value="extract"><span class="radio-btn"></span> Extract</label>
                    </div>
                    <button type="submit" class="action-btn">🔒 EXECUTE STEGO >>></button>
                </form>
            </div>
        </div>

        <!-- GLITCH MODULE CARD -->
        <div class="module-card">
            <div class="module-icon" style="border-color:#00ffff; box-shadow: inset 0 0 15px rgba(0,255,255,0.5); color:#00ffff;">⚡</div>
            <div class="module-form">
                <h2 style="color:#00ffff; text-shadow: 0 0 5px #00ffff;">GLITCH MODULE</h2>
                <p style="color:#008f8f;">Corrupt & Restore Image Pixels ///</p>
                <form method="POST" action="/glitch" enctype="multipart/form-data">
                    <div class="input-group" style="border-color:#00ffff;">
                        <span class="input-icon" style="background:rgba(0,255,255,0.2); border-color:#00ffff;">🔑</span>
                        <input type="text" name="key" placeholder="Enter Encryption Key..." required style="color:#00ffff;">
                    </div>
                    <div class="input-group" style="border-color:#00ffff;">
                        <span class="input-icon" style="background:rgba(0,255,255,0.2); border-color:#00ffff;">📁</span>
                        <input type="file" name="image" accept="image/*" required>
                    </div>
                    <div class="radio-group" style="color:#00ffff;">
                        <span>Mode :</span>
                        <label><input type="radio" name="action" value="glitch" checked><span class="radio-btn" style="border-color:#00ffff;"></span> Glitch</label>
                        <label><input type="radio" name="action" value="restore"><span class="radio-btn" style="border-color:#00ffff;"></span> Restore</label>
                    </div>
                    <button type="submit" class="action-btn" style="background:#00ffff; box-shadow: 0 0 15px rgba(0,255,255,0.5);">⚡ APPLY GLITCH >>></button>
                </form>
            </div>
        </div>

        <!-- RESULTS AREA (Shows only when available) -->
        {% if result %}
            <div class="result-box">
                <div style="color:#00aa2b; font-size:12px;">> SYSTEM OUTPUT:</div>
                <div style="color:#fff; margin-top:5px;">{{ result|safe }}</div>
            </div>
        {% endif %}
        {% if download_link %}
            <a href="{{ download_link }}" download class="download-btn">[ DOWNLOAD IMAGE ]</a>
        {% endif %}

        <!-- FOOTER STATS -->
        <div class="footer">
            <div>Total Tools<br><span>2 Modules</span></div>
            <div>Secure Mode<br><span>Activated</span></div>
            <div>Developed By<br><span>M_Setup</span></div>
        </div>
        <div style="text-align:center; color:#00aa2b; font-size:10px; margin-top:15px; letter-spacing:2px;">
            DECODE • ENCRYPT • BE UNSTOPPABLE
        </div>
    </div>
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

@app.route('/stego', methods=['POST'])
def stego():
    action = request.form.get('action')
    file = request.files.get('image')
    message = request.form.get('message', '')
    
    if not file: return render_template_string(HTML_MAIN, result="ERROR: File upload failed.")
    
    original_format = file.filename.split('.')[-1].lower()
    if original_format not in ['jpg', 'jpeg', 'png']: original_format = 'png'
        
    img = Image.open(file).convert('RGB')
    
    if img.width > 1500 or img.height > 1500:
        img.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
    
    if action == 'hide':
        if not message: return render_template_string(HTML_MAIN, result="ERROR: Message is empty.")
        
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
        return render_template_string(HTML_MAIN, result="SUCCESS: Payload injected securely.", download_link=link)

    elif action == 'extract':
        pixels = img.load()
        binary_data = ""
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1) + str(g & 1) + str(b & 1)
                if binary_data.endswith('1111111111111110'):
                    return render_template_string(HTML_MAIN, result=f"DECRYPTED MESSAGE:<br><br><span style='color:#00ff41; font-size:20px;'>\"{bin_to_text(binary_data[:-16])}\"</span>")
        return render_template_string(HTML_MAIN, result="ERROR: No hidden data detected in this image.")

@app.route('/glitch', methods=['POST'])
def glitch():
    action = request.form.get('action')
    file = request.files.get('image')
    key = request.form.get('key', '')
    
    if not file or not key: return render_template_string(HTML_MAIN, result="ERROR: Missing File or Encryption Key.")
    
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
        return render_template_string(HTML_MAIN, result="SUCCESS: Pixels corrupted. Remember your Key.", download_link=link)

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
        return render_template_string(HTML_MAIN, result="SUCCESS: Image restored to original state.", download_link=link)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
