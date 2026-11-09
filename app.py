from flask import Flask, request, render_template_string, send_from_directory
import io, os, random, string, base64, time, threading
from PIL import Image

app = Flask(__name__)
app.secret_key = "cyber_secret_key"
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 # 20 MB Limit

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ==========================================
# PROFESSIONAL APP-STYLE CSS
# ==========================================
BASE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    
    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
    
    body {
        background-color: #050505;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        padding-bottom: 80px; /* Space for bottom nav */
    }

    /* --- HEADER --- */
    .cyber-header {
        width: 100%;
        background: #000;
        border-bottom: 2px solid #00ff41;
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .header-left h1 { font-family: 'Orbitron', sans-serif; font-size: 22px; font-style: italic; color: #fff; text-shadow: 0 0 10px #00ff41; line-height: 1; }
    .header-left h1 span { color: #00ff41; }
    .header-left .sub { font-size: 10px; color: #00ff41; letter-spacing: 2px; }
    
    /* --- MAIN CONTENT AREA --- */
    .content {
        flex: 1;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center; /* Center everything vertically */
        align-items: center;
    }

    /* --- MODULE CARD (Form Area) --- */
    .module-card {
        width: 100%;
        max-width: 500px;
        background: rgba(0, 0, 0, 0.9);
        border: 2px solid #00ff41;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.15);
        animation: slideUp 0.3s ease-out;
    }

    .module-header { display: flex; align-items: center; gap: 15px; margin-bottom: 25px; border-bottom: 1px solid #333; padding-bottom: 15px; }
    .module-icon { width: 50px; height: 50px; border: 2px solid #00ff41; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; background: rgba(0,255,65,0.1); }
    .module-title h2 { font-family: 'Orbitron', sans-serif; font-size: 22px; color: #00ff41; }
    .module-title p { font-size: 12px; color: #00aa2b; }

    /* --- FORM ELEMENTS --- */
    .form-group { margin-bottom: 20px; }
    .form-group label { display: block; margin-bottom: 8px; font-size: 12px; color: #00aa2b; text-transform: uppercase; letter-spacing: 1px; }
    .input-wrapper { display: flex; background: #000; border: 1px solid #00ff41; border-radius: 6px; overflow: hidden; }
    .input-icon { padding: 12px; background: rgba(0,255,65,0.2); border-right: 1px solid #00ff41; }
    
    input[type="text"], input[type="file"] {
        width: 100%; background: transparent; border: none; color: #fff; padding: 12px;
        font-family: 'Share Tech Mono', monospace; outline: none; font-size: 15px;
    }
    input[type="file"]::file-selector-button { background: #00ff41; color: #000; border: none; padding: 5px 10px; cursor: pointer; font-weight: bold; }

    /* --- RADIO BUTTONS --- */
    .radio-group { display: flex; gap: 20px; margin-top: 10px; }
    .radio-group label { display: flex; align-items: center; cursor: pointer; font-size: 15px; color: #fff; }
    .radio-group input[type="radio"] { display: none; }
    .radio-btn { width: 18px; height: 18px; border: 2px solid #00ff41; border-radius: 50%; margin-right: 8px; }
    .radio-group input[type="radio"]:checked + .radio-btn { background: #00ff41; box-shadow: 0 0 10px #00ff41; }

    /* --- SUBMIT BUTTON --- */
    .action-btn {
        width: 100%; background: #00ff41; color: #000; border: none; padding: 16px;
        font-family: 'Orbitron', sans-serif; font-size: 16px; font-weight: 900;
        cursor: pointer; text-transform: uppercase; letter-spacing: 2px; border-radius: 6px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.4); transition: 0.2s;
    }
    .action-btn:active { transform: scale(0.98); }

    /* --- RESULT BOX --- */
    .result-box { margin-top: 25px; background: #000; border-left: 4px solid #00ff41; padding: 15px; border-radius: 4px; font-size: 14px; }
    .download-btn { display: block; margin-top: 15px; background: transparent; border: 1px solid #00ffff; color: #00ffff; padding: 12px; text-align: center; text-decoration: none; border-radius: 4px; }

    /* --- BOTTOM NAVIGATION BAR --- */
    .bottom-nav {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #000;
        border-top: 2px solid #00ff41;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 100;
        box-shadow: 0 -5px 20px rgba(0, 255, 65, 0.2);
    }

    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-decoration: none;
        color: #005a17;
        font-size: 12px;
        transition: 0.3s;
        cursor: pointer;
    }
    
    .nav-icon {
        font-size: 24px;
        margin-bottom: 5px;
        transition: 0.3s;
    }

    /* Active State for Nav */
    .nav-item.active { color: #00ff41; text-shadow: 0 0 10px #00ff41; }
    .nav-item.active .nav-icon { transform: translateY(-3px); filter: drop-shadow(0 0 5px #00ff41); }

    @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .hidden { display: none !important; }
</style>
"""

# ==========================================
# HTML TEMPLATE
# ==========================================
HTML_TEMPLATE = BASE_CSS + """
<!-- HEADER -->
<div class="cyber-header">
    <div class="header-left">
        <h1>CYBER<br><span>TOOLS</span></h1>
        <div class="sub">HACKER EDITION ///</div>
    </div>
</div>

<!-- MAIN CONTENT -->
<div class="content">
    {% if active_tab == 'stego' %}
    <!-- STEGO MODULE -->
    <div class="module-card">
        <div class="module-header">
            <div class="module-icon">📸</div>
            <div class="module-title"><h2>STEGO MODULE</h2><p>Hide / Extract Payload</p></div>
        </div>
        <form method="POST" action="/stego" enctype="multipart/form-data">
            <div class="form-group"><label>> Image</label><div class="input-wrapper"><span class="input-icon">📁</span><input type="file" name="image" required></div></div>
            <div class="form-group"><label>> Message</label><div class="input-wrapper"><span class="input-icon">💬</span><input type="text" name="message"></div></div>
            <div class="radio-group">
                <label><input type="radio" name="action" value="hide" checked><span class="radio-btn"></span> Hide</label>
                <label><input type="radio" name="action" value="extract"><span class="radio-btn"></span> Extract</label>
            </div>
            <button type="submit" class="action-btn" style="margin-top:20px;">🔒 EXECUTE</button>
        </form>
        {% if result and result_type == 'stego' %}
        <div class="result-box"><div style="color:#fff;">{{ result|safe }}</div>{% if download_link %}<a href="{{ download_link }}" download class="download-btn">[ DOWNLOAD IMAGE ]</a>{% endif %}</div>
        {% endif %}
    </div>
    
    {% elif active_tab == 'glitch' %}
    <!-- GLITCH MODULE -->
    <div class="module-card" style="border-color:#00ffff;">
        <div class="module-header" style="border-color:#005555;">
            <div class="module-icon" style="border-color:#00ffff; background:rgba(0,255,255,0.1);">⚡</div>
            <div class="module-title"><h2 style="color:#00ffff;">GLITCH MODULE</h2><p style="color:#008f8f;">Corrupt / Restore Pixels</p></div>
        </div>
        <form method="POST" action="/glitch" enctype="multipart/form-data">
            <div class="form-group"><label>> Encryption Key</label><div class="input-wrapper" style="border-color:#00ffff;"><span class="input-icon" style="background:rgba(0,255,255,0.2); border-color:#00ffff;">🔑</span><input type="text" name="key" required></div></div>
            <div class="form-group"><label>> Image</label><div class="input-wrapper" style="border-color:#00ffff;"><span class="input-icon" style="background:rgba(0,255,255,0.2); border-color:#00ffff;">📁</span><input type="file" name="image" required></div></div>
            <div class="radio-group" style="color:#00ffff;">
                <label><input type="radio" name="action" value="glitch" checked><span class="radio-btn" style="border-color:#00ffff;"></span> Glitch</label>
                <label><input type="radio" name="action" value="restore"><span class="radio-btn" style="border-color:#00ffff;"></span> Restore</label>
            </div>
            <button type="submit" class="action-btn" style="margin-top:20px; background:#00ffff;">⚡ APPLY</button>
        </form>
        {% if result and result_type == 'glitch' %}
        <div class="result-box" style="border-color:#00ffff;"><div style="color:#fff;">{{ result|safe }}</div>{% if download_link %}<a href="{{ download_link }}" download class="download-btn">[ DOWNLOAD IMAGE ]</a>{% endif %}</div>
        {% endif %}
    </div>

    {% elif active_tab == 'share' %}
    <!-- FILE SHARE MODULE -->
    <div class="module-card" style="border-color:#ff00ff;">
        <div class="module-header" style="border-color:#550055;">
            <div class="module-icon" style="border-color:#ff00ff; background:rgba(255,0,255,0.1);">☁️</div>
            <div class="module-title"><h2 style="color:#ff00ff;">FILE SHARE</h2><p style="color:#8f008f;">Secure File Transfer (20MB)</p></div>
        </div>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <div class="form-group"><label>> Select File</label><div class="input-wrapper" style="border-color:#ff00ff;"><span class="input-icon" style="background:rgba(255,0,255,0.2); border-color:#ff00ff;">📁</span><input type="file" name="file" required></div></div>
            <button type="submit" class="action-btn" style="margin-top:20px; background:#ff00ff; color:#fff;">📤 UPLOAD & GET LINK</button>
        </form>
        {% if share_link %}
        <div class="result-box" style="border-color:#ff00ff;">
            <div style="color:#ff00ff; font-size:12px;">> LINK GENERATED:</div>
            <div style="margin-top:10px; background:#111; padding:10px; border:1px solid #ff00ff; word-break:break-all; border-radius:4px;">
                <a href="{{ share_link }}" target="_blank" style="color:#00ffff; text-decoration:none;">{{ share_link }}</a>
            </div>
            <div style="font-size:11px; color:#888; margin-top:8px;">(One-Time Download Link)</div>
        </div>
        {% endif %}
    </div>
    {% endif %}
</div>

<!-- BOTTOM NAVIGATION BAR -->
<div class="bottom-nav">
    <a href="/?tab=stego" class="nav-item {% if active_tab == 'stego' %}active{% endif %}">
        <div class="nav-icon">📸</div>
        <div>Stego</div>
    </a>
    <a href="/?tab=glitch" class="nav-item {% if active_tab == 'glitch' %}active{% endif %}">
        <div class="nav-icon">⚡</div>
        <div>Glitch</div>
    </a>
    <a href="/?tab=share" class="nav-item {% if active_tab == 'share' %}active{% endif %}">
        <div class="nav-icon">☁️</div>
        <div>Share</div>
    </a>
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
def random_name(length=8): return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ==========================================
# ROUTES
# ==========================================
@app.route('/')
def index():
    # Get active tab from URL, default to stego
    tab = request.args.get('tab', 'stego')
    if tab not in ['stego', 'glitch', 'share']:
        tab = 'stego'
    return render_template_string(HTML_TEMPLATE, active_tab=tab)

# STEGO
@app.route('/stego', methods=['POST'])
def stego():
    action = request.form.get('action')
    file = request.files.get('image')
    message = request.form.get('message', '')
    if not file: return render_template_string(HTML_TEMPLATE, active_tab='stego', result="ERROR: File upload failed.", result_type='stego')
    
    original_format = file.filename.split('.')[-1].lower()
    if original_format not in ['jpg', 'jpeg', 'png']: original_format = 'png'
    img = Image.open(file).convert('RGB')
    if img.width > 1500 or img.height > 1500: img.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
    
    if action == 'hide':
        if not message: return render_template_string(HTML_TEMPLATE, active_tab='stego', result="ERROR: Message empty.", result_type='stego')
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
        if original_format in ['jpg', 'jpeg']: img.save(img_io, 'JPEG', quality=85); mime = 'image/jpeg'
        else: img.save(img_io, 'PNG'); mime = 'image/png'
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        return render_template_string(HTML_TEMPLATE, active_tab='stego', result="SUCCESS: Payload injected.", download_link=f"data:{mime};base64,{b64}", result_type='stego')
    elif action == 'extract':
        pixels = img.load()
        binary_data = ""
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1) + str(g & 1) + str(b & 1)
                if binary_data.endswith('1111111111111110'):
                    return render_template_string(HTML_TEMPLATE, active_tab='stego', result=f"DECRYPTED:<br><span style='color:#0f0; font-size:18px;'>\"{bin_to_text(binary_data[:-16])}\"</span>", result_type='stego')
        return render_template_string(HTML_TEMPLATE, active_tab='stego', result="ERROR: No hidden data found.", result_type='stego')

# GLITCH
@app.route('/glitch', methods=['POST'])
def glitch():
    action = request.form.get('action')
    file = request.files.get('image')
    key = request.form.get('key', '')
    if not file or not key: return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="ERROR: Missing input.", result_type='glitch')
    
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
        if original_format in ['jpg', 'jpeg']: new_img.save(img_io, 'JPEG', quality=85); mime = 'image/jpeg'
        else: new_img.save(img_io, 'PNG'); mime = 'image/png'
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="SUCCESS: Pixels corrupted.", download_link=f"data:{mime};base64,{b64}", result_type='glitch')
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
        if original_format in ['jpg', 'jpeg']: new_img.save(img_io, 'JPEG', quality=85); mime = 'image/jpeg'
        else: new_img.save(img_io, 'PNG'); mime = 'image/png'
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="SUCCESS: Image restored.", download_link=f"data:{mime};base64,{b64}", result_type='glitch')

# FILE SHARE
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file: return render_template_string(HTML_TEMPLATE, active_tab='share', share_link="ERROR: No file selected.")
    
    ext = file.filename.split('.')[-1]
    filename = random_name() + "." + ext
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    host = request.host_url.rstrip('/')
    link = f"{host}/download/{filename}"
    return render_template_string(HTML_TEMPLATE, active_tab='share', share_link=link)

# ONE-TIME DOWNLOAD LOGIC
@app.route('/download/<filename>')
def download_file(filename):
    if '..' in filename or filename.startswith('/'): return "Invalid File"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath): return "File not found or already downloaded/deleted!"
    try:
        response = send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
        def delete_file():
            time.sleep(2)
            if os.path.exists(filepath): os.remove(filepath)
        threading.Thread(target=delete_file).start()
        return response
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
