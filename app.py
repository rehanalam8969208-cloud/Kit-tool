from flask import Flask, request, render_template_string
import io
from PIL import Image
import random
import base64

app = Flask(__name__)
app.secret_key = "cyber_secret_key"
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 # 100MB Limit

# ==========================================
# FULLSCREEN HACKER UI WITH MATRIX EFFECT
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
        background-size: 30px 30px;
        overflow-x: hidden;
    }

    /* MATRIX HEADER EFFECT */
    .cyber-header {
        width: 100%;
        height: 180px;
        background: #000;
        border-bottom: 2px solid #00ff41;
        position: relative;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 30px;
        overflow: hidden;
    }

    /* CSS Matrix Code effect */
    .matrix-bg {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: repeating-linear-gradient(0deg, transparent, transparent 2px, #00ff41 3px);
        opacity: 0.1;
        animation: scan 10s linear infinite;
    }
    @keyframes scan { 0% { background-position: 0 0; } 100% { background-position: 0 100vh; } }

    .header-left { z-index: 2; }
    .header-left h1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 32px;
        font-style: italic;
        color: #fff;
        text-shadow: 0 0 10px #00ff41;
        line-height: 1;
    }
    .header-left h1 span { color: #00ff41; }
    .header-left .sub { font-size: 12px; color: #00ff41; letter-spacing: 2px; margin-bottom: 15px; }
    
    .status-box {
        background: rgba(0,0,0,0.8);
        border: 1px solid #00ff41;
        padding: 8px;
        font-size: 11px;
        display: inline-block;
        box-shadow: inset 0 0 10px rgba(0,255,65,0.2);
    }
    .status-box div { margin-bottom: 4px; }
    .status-box span { color: #fff; }

    .header-right {
        z-index: 2;
        text-align: right;
        font-family: 'Orbitron', sans-serif;
        font-size: 16px;
        color: #00ff41;
        text-shadow: 0 0 8px #00ff41;
        line-height: 1.6;
    }

    /* MAIN CONTAINER FULL WIDTH */
    .main-container {
        flex: 1;
        width: 100%;
        max-width: 800px; /* PC par bhi beech mein rahe */
        margin: 0 auto;
        padding: 30px 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* MODULE CARDS */
    .module-card {
        border: 1px solid #00ff41;
        background: rgba(0, 255, 65, 0.05);
        padding: 20px;
        margin-bottom: 25px;
        border-radius: 5px;
        position: relative;
        display: flex;
        gap: 20px;
        align-items: center;
        box-shadow: 0 0 20px rgba(0,255,65,0.1);
    }

    .module-card::before, .module-card::after {
        content: ''; position: absolute; width: 15px; height: 15px; border: 2px solid #00ff41;
    }
    .module-card::before { top: -1px; left: -1px; border-right: none; border-bottom: none; }
    .module-card::after { bottom: -1px; right: -1px; border-left: none; border-top: none; }

    .module-icon {
        width: 90px; height: 90px; border: 2px solid #00ff41; border-radius: 50%;
        display: flex; justify-content: center; align-items: center; font-size: 35px;
        background: rgba(0, 255, 65, 0.1); box-shadow: inset 0 0 20px rgba(0, 255, 65, 0.5);
        flex-shrink: 0;
    }

    .module-form { flex: 1; }
    .module-form h2 {
        font-family: 'Orbitron', sans-serif; font-size: 22px; color: #00ff41;
        margin-bottom: 5px; text-shadow: 0 0 5px #00ff41;
    }
    .module-form p { font-size: 12px; color: #00aa2b; margin-bottom: 15px; font-style: italic;}

    /* Custom Inputs */
    .input-group {
        display: flex; align-items: center; background: #000; border: 1px solid #00ff41;
        margin-bottom: 12px; padding: 0;
    }
    .input-icon {
        padding: 12px; background: rgba(0, 255, 65, 0.2); border-right: 1px solid #00ff41; font-size: 18px;
    }
    input[type="file"], input[type="text"] {
        width: 100%; background: transparent; border: none; color: #fff; padding: 12px;
        font-family: 'Share Tech Mono', monospace; outline: none; font-size: 15px;
    }
    input[type="file"]::file-selector-button {
        background: #00ff41; color: #000; border: none; padding: 6px 12px; cursor: pointer; font-weight: bold; margin-right: 10px;
    }

    /* Radio Buttons */
    .radio-group { display: flex; gap: 20px; margin-bottom: 20px; font-size: 15px; align-items: center;}
    .radio-group label { display: flex; align-items: center; cursor: pointer; }
    .radio-group input[type="radio"] { display: none; }
    .radio-btn {
        width: 18px; height: 18px; border: 2px solid #00ff41; border-radius: 50%; margin-right: 8px; display: inline-block;
    }
    .radio-group input[type="radio"]:checked + .radio-btn { background: #00ff41; box-shadow: 0 0 10px #00ff41; }

    /* Action Buttons */
    .action-btn {
        width: 100%; background: #00ff41; color: #000; border: none; padding: 15px;
        font-family: 'Orbitron', sans-serif; font-size: 18px; font-weight: 900;
        cursor: pointer; text-transform: uppercase; letter-spacing: 2px;
        display: flex; justify-content: center; align-items: center; gap: 10px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.5); transition: all 0.3s;
        clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
    }
    .action-btn:hover { background: #fff; box-shadow: 0 0 25px #00ff41; }

    /* Result Box */
    .result-box {
        background: #000; border-left: 4px solid #00ff41; padding: 15px;
        font-size: 14px; margin-bottom: 15px; animation: slideIn 0.3s ease-out;
        word-break: break-all;
    }
    .download-btn {
        display: block; width: 100%; background: transparent; border: 1px solid #00ffff; color: #00ffff;
        padding: 15px; text-align: center; text-decoration: none; margin-bottom: 20px; text-transform: uppercase;
        box-shadow: 0 0 10px rgba(0,255,255,0.3);
    }

    /* FOOTER */
    .footer {
        display: flex; justify-content: space-between; border-top: 1px solid #00ff41;
        padding-top: 15px; margin-top: auto; font-size: 11px; text-align: center;
        background: rgba(0,0,0,0.8);
    }
    .footer div { flex: 1; border-right: 1px solid #00aa2b; padding: 5px;}
    .footer div:last-child { border-right: none; }
    .footer span { display: block; font-size: 15px; color: #fff; margin-top: 5px; font-family: 'Orbitron';}

    @keyframes slideIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }

    /* Mobile Responsive */
    @media (max-width: 600px) {
        .cyber-header { height: 150px; flex-direction: column; justify-content: center; text-align: center; padding: 10px; }
        .header-left h1 { font-size: 24px; }
        .header-right { display: none; } /* Mobile par side text hide */
        .module-card { flex-direction: column; text-align: center; }
        .module-icon { margin-bottom: 10px; }
        .radio-group { justify-content: center; }
    }
</style>
"""

HTML_MAIN = BASE_CSS + """
<!-- HEADER -->
<div class="cyber-header">
    <div class="matrix-bg"></div>
    <div class="header-left">
        <h1>CYBER<br><span>PHOTO</span></h1>
        <div class="sub">HACKER EDITION ///</div>
    </div>
    <div class="header-right">
        Encrypt<br>Hide<br>Protect...
    </div>
</div>

<!-- MAIN BODY -->
<div class="main-container">
    <!-- STATUS BOX -->
    <div class="status-box" style="margin-bottom:20px; width:200px; margin-left:auto; margin-right:auto;">
        <div style="text-align:center;">> Status : <span>Online</span></div>
        <div style="text-align:center;">> Tools  : <span>2 Modules</span></div>
        <div style="text-align:center;">> Version: <span>v2.0.0</span></div>
    </div>

    <!-- STEGO CARD -->
    <div class="module-card">
        <div class="module-icon">📸</div>
        <div class="module-form">
            <h2>STEGO MODULE</h2>
            <p>Hide / Extract Secret Payload ///</p>
            <form method="POST" action="/stego" enctype="multipart/form-data">
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

    <!-- GLITCH CARD -->
    <div class="module-card" style="border-color:#00ffff;">
        <div class="module-icon" style="border-color:#00ffff; box-shadow: inset 0 0 20px rgba(0,255,255,0.5); color:#00ffff;">⚡</div>
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

    <!-- RESULTS -->
    {% if result %}
        <div class="result-box">
            <div style="color:#00aa2b; font-size:12px; margin-bottom:5px;">> SYSTEM OUTPUT:</div>
            <div style="color:#fff;">{{ result|safe }}</div>
        </div>
    {% endif %}
    {% if download_link %}
        <a href="{{ download_link }}" download class="download-btn">[ DOWNLOAD IMAGE ]</a>
    {% endif %}
</div>

<!-- FOOTER -->
<div class="footer">
    <div>Total Tools<br><span>2 Modules</span></div>
    <div>Secure Mode<br><span>Activated</span></div>
    <div>Developed By<br><span>M_Setup</span></div>
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
        return render_template_string(HTML_MAIN, result="ERROR: No hidden data detected.")

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
        return render_template_string(HTML_MAIN, result="SUCCESS: Pixels corrupted.", download_link=link)

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
        return render_template_string(HTML_MAIN, result="SUCCESS: Image restored.", download_link=link)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
