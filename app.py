from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for
import io, os, random, string, base64
from PIL import Image

app = Flask(__name__)
app.secret_key = "cyber_secret_key"
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 # 20 MB Limit for safety

# Folder banate hain file save karne ke liye
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ==========================================
# CSS DESIGN (Wahi Hacker Theme)
# ==========================================
BASE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background-color: #050505; color: #00ff41; font-family: 'Share Tech Mono', monospace; min-height: 100vh; display: flex; flex-direction: column; background-image: linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px); background-size: 50px 50px; }
    .cyber-header { width: 100%; background: #000; border-bottom: 2px solid #00ff41; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 5px 20px rgba(0, 255, 65, 0.2); }
    .header-left h1 { font-family: 'Orbitron', sans-serif; font-size: 28px; font-style: italic; color: #fff; text-shadow: 0 0 10px #00ff41; line-height: 1; }
    .header-left h1 span { color: #00ff41; }
    .header-left .sub { font-size: 12px; color: #00ff41; letter-spacing: 2px; }
    .header-right { text-align: right; color: #00ff41; font-size: 14px; line-height: 1.5; font-weight: bold; }
    .dashboard { flex: 1; display: flex; flex-direction: column; padding: 20px; max-width: 1200px; margin: 0 auto; width: 100%; gap: 20px; }
    
    /* Tabs */
    .tabs { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; }
    .tab-btn { background: transparent; border: 1px solid #00ff41; color: #00ff41; padding: 10px 20px; cursor: pointer; font-family: 'Share Tech Mono'; font-size: 16px; text-transform: uppercase; }
    .tab-btn.active { background: #00ff41; color: #000; font-weight: bold; }

    .modules-container { display: flex; flex-direction: row; gap: 20px; flex: 1; }
    .module-card { flex: 1; background: rgba(0, 0, 0, 0.85); border: 2px solid #00ff41; border-radius: 8px; padding: 25px; display: flex; flex-direction: column; box-shadow: 0 0 20px rgba(0, 255, 65, 0.1); }
    .module-card.share-card { border-color: #ff00ff; box-shadow: 0 0 20px rgba(255, 0, 255, 0.1); }
    .module-header { display: flex; align-items: center; gap: 15px; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 15px; }
    .module-icon { width: 50px; height: 50px; border: 2px solid #00ff41; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; background: rgba(0,255,65,0.1); }
    .share-card .module-icon { border-color: #ff00ff; background: rgba(255,0,255,0.1); }
    .module-title h2 { font-family: 'Orbitron', sans-serif; font-size: 20px; color: #00ff41; }
    .share-card .module-title h2 { color: #ff00ff; }
    
    .form-group { margin-bottom: 15px; }
    .form-group label { display: block; margin-bottom: 5px; font-size: 12px; color: #00aa2b; text-transform: uppercase; }
    .input-wrapper { display: flex; background: #000; border: 1px solid #00ff41; border-radius: 4px; }
    .share-card .input-wrapper { border-color: #ff00ff; }
    .input-icon { padding: 10px; background: rgba(0,255,65,0.2); border-right: 1px solid #00ff41; }
    .share-card .input-icon { background: rgba(255,0,255,0.2); border-color: #ff00ff; }
    input[type="text"], input[type="file"] { width: 100%; background: transparent; border: none; color: #fff; padding: 10px; font-family: 'Share Tech Mono'; outline: none; font-size: 14px; }
    input[type="file"]::file-selector-button { background: #00ff41; color: #000; border: none; padding: 5px 10px; cursor: pointer; font-weight: bold; }
    
    .radio-group { display: flex; gap: 15px; margin-bottom: 20px; }
    .radio-group label { display: flex; align-items: center; cursor: pointer; font-size: 14px; color: #fff;}
    .radio-group input[type="radio"] { display: none; }
    .radio-btn { width: 14px; height: 14px; border: 2px solid #00ff41; border-radius: 50%; margin-right: 6px; }
    .radio-group input[type="radio"]:checked + .radio-btn { background: #00ff41; }
    
    .action-btn { width: 100%; background: #00ff41; color: #000; border: none; padding: 15px; font-family: 'Orbitron', sans-serif; font-size: 16px; font-weight: 900; cursor: pointer; text-transform: uppercase; margin-top: auto; }
    .share-card .action-btn { background: #ff00ff; color: #fff; }
    
    .result-box { margin-top: 15px; background: #000; border-left: 4px solid #00ff41; padding: 15px; font-size: 13px; }
    .share-card .result-box { border-color: #ff00ff; }
    
    .footer { width: 100%; background: #000; border-top: 1px solid #00ff41; padding: 15px; display: flex; justify-content: space-around; text-align: center; font-size: 11px;}
    .footer span { display: block; font-size: 14px; color: #fff; font-family: 'Orbitron'; margin-top: 5px; }
    @media (max-width: 768px) { .modules-container { flex-direction: column; } }
    .hidden { display: none; }
</style>
"""

# ==========================================
# HTML LAYOUT
# ==========================================
HTML_MAIN = BASE_CSS + """
<div class="cyber-header">
    <div class="header-left">
        <h1>CYBER<br><span>TOOLS</span></h1>
        <div class="sub">HACKER EDITION ///</div>
    </div>
    <div class="header-right">Encrypt<br>Share<br>Protect...</div>
</div>

<div class="dashboard">
    <div class="tabs">
        <button class="tab-btn active" onclick="showTab('img-tools')">Image Tools</button>
        <button class="tab-btn" onclick="showTab('share-tool')">File Share</button>
    </div>

    <!-- IMAGE TOOLS TAB -->
    <div id="img-tools" class="modules-container">
        <!-- STEGO MODULE -->
        <div class="module-card">
            <div class="module-header">
                <div class="module-icon">📸</div>
                <div class="module-title"><h2>STEGO MODULE</h2></div>
            </div>
            <form method="POST" action="/stego" enctype="multipart/form-data" style="display:flex; flex-direction:column; height:100%;">
                <div class="form-group"><label>> Image</label><div class="input-wrapper"><span class="input-icon">📁</span><input type="file" name="image" required></div></div>
                <div class="form-group"><label>> Message</label><div class="input-wrapper"><span class="input-icon">💬</span><input type="text" name="message"></div></div>
                <div class="form-group"><div class="radio-group"><label><input type="radio" name="action" value="hide" checked><span class="radio-btn"></span> Hide</label><label><input type="radio" name="action" value="extract"><span class="radio-btn"></span> Extract</label></div></div>
                <button type="submit" class="action-btn">🔒 EXECUTE STEGO</button>
            </form>
            {% if result and result_type == 'stego' %}<div class="result-box"><div style="color:#fff;">{{ result|safe }}</div>{% if download_link %}<a href="{{ download_link }}" download class="download-btn">[ DOWNLOAD ]</a>{% endif %}</div>{% endif %}
        </div>

        <!-- GLITCH MODULE -->
        <div class="module-card">
            <div class="module-header"><div class="module-icon">⚡</div><div class="module-title"><h2>GLITCH MODULE</h2></div></div>
            <form method="POST" action="/glitch" enctype="multipart/form-data" style="display:flex; flex-direction:column; height:100%;">
                <div class="form-group"><label>> Key</label><div class="input-wrapper"><span class="input-icon">🔑</span><input type="text" name="key" required></div></div>
                <div class="form-group"><label>> Image</label><div class="input-wrapper"><span class="input-icon">📁</span><input type="file" name="image" required></div></div>
                <div class="form-group"><div class="radio-group"><label><input type="radio" name="action" value="glitch" checked><span class="radio-btn"></span> Glitch</label><label><input type="radio" name="action" value="restore"><span class="radio-btn"></span> Restore</label></div></div>
                <button type="submit" class="action-btn">⚡ APPLY GLITCH</button>
            </form>
            {% if result and result_type == 'glitch' %}<div class="result-box"><div style="color:#fff;">{{ result|safe }}</div>{% if download_link %}<a href="{{ download_link }}" download class="download-btn">[ DOWNLOAD ]</a>{% endif %}</div>{% endif %}
        </div>
    </div>

    <!-- FILE SHARE TAB -->
    <div id="share-tool" class="modules-container hidden">
        <div class="module-card share-card">
            <div class="module-header"><div class="module-icon">☁️</div><div class="module-title"><h2>FILE SHARING</h2><p>Max 20MB File</p></div></div>
            <form method="POST" action="/upload" enctype="multipart/form-data" style="display:flex; flex-direction:column; height:100%;">
                <div class="form-group"><label>> Select File (Max 20MB)</label><div class="input-wrapper"><span class="input-icon">📁</span><input type="file" name="file" required></div></div>
                <button type="submit" class="action-btn">📤 UPLOAD & GET LINK</button>
            </form>
            {% if share_link %}
                <div class="result-box">
                    <div style="color:#ff00ff;">> UPLOAD SUCCESSFUL:</div>
                    <div style="margin-top:10px; background:#111; padding:10px; border:1px solid #ff00ff; word-break:break-all;">
                        <a href="{{ share_link }}" target="_blank" style="color:#00ffff; text-decoration:none;">{{ share_link }}</a>
                    </div>
                    <div style="font-size:11px; color:#888; margin-top:5px;">(Copy link and share with anyone)</div>
                </div>
            {% endif %}
        </div>
    </div>

</div>
<div class="footer">
    <div>Total Tools<br><span>3 Modules</span></div>
    <div>Secure Mode<br><span>Activated</span></div>
    <div>Developed By<br><span>M_Setup</span></div>
</div>
<script>
    function showTab(tabId) {
        document.getElementById('img-tools').classList.add('hidden');
        document.getElementById('share-tool').classList.add('hidden');
        document.getElementById(tabId).classList.remove('hidden');
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
    }
</script>
"""

# ==========================================
# LOGIC & ROUTES
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

def random_name(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def index():
    return render_template_string(HTML_MAIN)

# STEGO
@app.route('/stego', methods=['POST'])
def stego():
    action = request.form.get('action')
    file = request.files.get('image')
    message = request.form.get('message', '')
    if not file: return render_template_string(HTML_MAIN, result="ERROR: File upload failed.", result_type='stego')
    
    original_format = file.filename.split('.')[-1].lower()
    if original_format not in ['jpg', 'jpeg', 'png']: original_format = 'png'
    img = Image.open(file).convert('RGB')
    if img.width > 1500 or img.height > 1500: img.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
    
    if action == 'hide':
        if not message: return render_template_string(HTML_MAIN, result="ERROR: Message empty.", result_type='stego')
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
        return render_template_string(HTML_MAIN, result="SUCCESS: Payload injected.", download_link=f"data:{mime};base64,{b64}", result_type='stego')
    elif action == 'extract':
        pixels = img.load()
        binary_data = ""
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1) + str(g & 1) + str(b & 1)
                if binary_data.endswith('1111111111111110'):
                    return render_template_string(HTML_MAIN, result=f"DECRYPTED:<br><span style='color:#0f0; font-size:18px;'>\"{bin_to_text(binary_data[:-16])}\"</span>", result_type='stego')
        return render_template_string(HTML_MAIN, result="ERROR: No hidden data found.", result_type='stego')

# GLITCH
@app.route('/glitch', methods=['POST'])
def glitch():
    action = request.form.get('action')
    file = request.files.get('image')
    key = request.form.get('key', '')
    if not file or not key: return render_template_string(HTML_MAIN, result="ERROR: Missing input.", result_type='glitch')
    
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
        return render_template_string(HTML_MAIN, result="SUCCESS: Pixels corrupted.", download_link=f"data:{mime};base64,{b64}", result_type='glitch')
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
        return render_template_string(HTML_MAIN, result="SUCCESS: Image restored.", download_link=f"data:{mime};base64,{b64}", result_type='glitch')

# FILE SHARE
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file: return render_template_string(HTML_MAIN, share_link="ERROR: No file selected.")
    
    # Generate random filename
    ext = file.filename.split('.')[-1]
    filename = random_name() + "." + ext
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # Create download link
    host = request.host_url.rstrip('/')
    link = f"{host}/download/{filename}"
    return render_template_string(HTML_MAIN, share_link=link)

@app.route('/download/<filename>')
def download_file(filename):
    # Security: Prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        return "Invalid File"
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
