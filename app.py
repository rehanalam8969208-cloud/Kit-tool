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
# PREMIUM iOS GLASSMORPHISM CSS
# ==========================================
BASE_CSS = """
<style>
    :root {
        --glass-bg: rgba(255, 255, 255, 0.15);
        --glass-border: rgba(255, 255, 255, 0.3);
        --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.7);
        --accent: #007aff;
    }

    * { 
        box-sizing: border-box; 
        margin: 0; 
        padding: 0; 
        -webkit-tap-highlight-color: transparent; 
    }
    
    body {
        background: linear-gradient(45deg, #100e17, #1a1a2e, #16213e, #0f3460);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: var(--text-primary);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        padding-bottom: 90px;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* --- HEADER --- */
    .app-header {
        width: 100%;
        background: rgba(20, 20, 30, 0.4);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--glass-border);
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .app-header h1 { 
        font-size: 20px; 
        font-weight: 700; 
        letter-spacing: 0.5px;
    }
    .app-header .sub { 
        font-size: 11px; 
        color: var(--text-secondary); 
        margin-top: 2px;
    }
    
    /* --- MAIN CONTENT AREA --- */
    .content {
        flex: 1;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* --- MODULE CARD (Glass Form Area) --- */
    .module-card {
        width: 100%;
        max-width: 450px;
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 25px;
        box-shadow: var(--glass-shadow);
        animation: fadeUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .module-header { 
        display: flex; 
        align-items: center; 
        gap: 15px; 
        margin-bottom: 25px; 
    }
    .module-icon { 
        width: 50px; 
        height: 50px; 
        background: linear-gradient(135deg, rgba(255,255,255,0.3), rgba(255,255,255,0.05));
        border: 1px solid var(--glass-border); 
        border-radius: 16px; 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        font-size: 24px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .module-title h2 { font-size: 20px; font-weight: 600; }
    .module-title p { font-size: 13px; color: var(--text-secondary); margin-top: 4px;}

    /* --- FORM ELEMENTS --- */
    .form-group { margin-bottom: 20px; }
    .form-group label { 
        display: block; 
        margin-bottom: 8px; 
        font-size: 13px; 
        color: var(--text-secondary); 
        font-weight: 500;
    }
    .input-wrapper { 
        display: flex; 
        background: rgba(0, 0, 0, 0.2); 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        border-radius: 14px; 
        overflow: hidden; 
        transition: all 0.3s ease;
    }
    .input-wrapper:focus-within {
        border-color: rgba(255, 255, 255, 0.5);
        background: rgba(0, 0, 0, 0.3);
    }
    .input-icon { 
        padding: 14px; 
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    input[type="text"], input[type="file"] {
        width: 100%; 
        background: transparent; 
        border: none; 
        color: #fff; 
        padding: 14px 14px 14px 0;
        font-family: inherit; 
        outline: none; 
        font-size: 15px;
    }
    input[type="file"]::file-selector-button { 
        background: var(--glass-bg); 
        color: #fff; 
        border: 1px solid var(--glass-border); 
        border-radius: 8px;
        padding: 6px 12px; 
        margin-right: 10px;
        cursor: pointer; 
        font-weight: 500; 
        transition: 0.2s;
    }

    /* --- RADIO BUTTONS (iOS Segmented Style) --- */
    .radio-group { 
        display: flex; 
        gap: 10px; 
        margin-top: 10px; 
        background: rgba(0,0,0,0.2);
        padding: 4px;
        border-radius: 12px;
    }
    .radio-group label { 
        flex: 1;
        text-align: center;
        padding: 10px;
        cursor: pointer; 
        font-size: 14px; 
        font-weight: 500;
        color: var(--text-secondary); 
        border-radius: 10px;
        transition: 0.3s;
    }
    .radio-group input[type="radio"] { display: none; }
    .radio-group input[type="radio"]:checked + span { 
        color: #fff; 
    }
    .radio-group label:has(input[type="radio"]:checked) {
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* --- SUBMIT BUTTON --- */
    .action-btn {
        width: 100%; 
        background: rgba(255, 255, 255, 0.9); 
        color: #000; 
        border: none; 
        padding: 16px;
        font-family: inherit; 
        font-size: 16px; 
        font-weight: 600;
        cursor: pointer; 
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2); 
        transition: 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .action-btn:active { transform: scale(0.96); background: #fff; }

    /* --- RESULT BOX --- */
    .result-box { 
        margin-top: 25px; 
        background: rgba(0, 0, 0, 0.2); 
        border: 1px solid var(--glass-border); 
        padding: 18px; 
        border-radius: 16px; 
        font-size: 14px; 
        text-align: center;
    }
    .download-btn { 
        display: block; 
        margin-top: 15px; 
        background: var(--glass-bg); 
        border: 1px solid var(--glass-border); 
        color: #fff; 
        padding: 14px; 
        text-align: center; 
        text-decoration: none; 
        border-radius: 12px; 
        font-weight: 500;
    }

    /* --- BOTTOM NAVIGATION BAR --- */
    .bottom-nav {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: rgba(20, 20, 30, 0.65);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-top: 1px solid rgba(255,255,255,0.1);
        display: flex;
        justify-content: space-around;
        padding: 15px 0 calc(15px + env(safe-area-inset-bottom));
        z-index: 100;
    }

    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-decoration: none;
        color: var(--text-secondary);
        font-size: 11px;
        font-weight: 500;
        transition: 0.3s;
        cursor: pointer;
    }
    
    .nav-icon {
        font-size: 22px;
        margin-bottom: 4px;
        transition: 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        opacity: 0.7;
    }

    /* Active State for Nav */
    .nav-item.active { color: #fff; }
    .nav-item.active .nav-icon { 
        transform: translateY(-4px) scale(1.1); 
        opacity: 1;
    }

    @keyframes fadeUp { 
        from { opacity: 0; transform: translateY(30px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
</style>
"""

# ==========================================
# HTML TEMPLATE (Added Meta Viewport & Cleaned tags)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Tools</title>
    """ + BASE_CSS + """
</head>
<body>

<!-- HEADER -->
<div class="app-header">
    <div class="header-left">
        <h1>Utility Tools</h1>
        <div class="sub">Secure Module</div>
    </div>
</div>

<!-- MAIN CONTENT -->
<div class="content">
    {% if active_tab == 'stego' %}
    <!-- STEGO MODULE -->
    <div class="module-card">
        <div class="module-header">
            <div class="module-icon">📸</div>
            <div class="module-title"><h2>Steganography</h2><p>Hide or Extract Data</p></div>
        </div>
        <form method="POST" action="/stego" enctype="multipart/form-data">
            <div class="form-group"><label>Select Image</label><div class="input-wrapper"><span class="input-icon">📁</span><input type="file" name="image" required></div></div>
            <div class="form-group"><label>Secret Message</label><div class="input-wrapper"><span class="input-icon">💬</span><input type="text" name="message" placeholder="Enter payload..."></div></div>
            <div class="radio-group">
                <label><input type="radio" name="action" value="hide" checked><span>Hide Data</span></label>
                <label><input type="radio" name="action" value="extract"><span>Extract Data</span></label>
            </div>
            <button type="submit" class="action-btn" style="margin-top:20px;">Execute</button>
        </form>
        {% if result and result_type == 'stego' %}
        <div class="result-box"><div>{{ result|safe }}</div>{% if download_link %}<a href="{{ download_link }}" download class="download-btn">Save Image</a>{% endif %}</div>
        {% endif %}
    </div>
    
    {% elif active_tab == 'glitch' %}
    <!-- GLITCH MODULE -->
    <div class="module-card">
        <div class="module-header">
            <div class="module-icon">⚡</div>
            <div class="module-title"><h2>Glitch Module</h2><p>Corrupt or Restore Pixels</p></div>
        </div>
        <form method="POST" action="/glitch" enctype="multipart/form-data">
            <div class="form-group"><label>Encryption Key</label><div class="input-wrapper"><span class="input-icon">🔑</span><input type="text" name="key" placeholder="Enter key..." required></div></div>
            <div class="form-group"><label>Select Image</label><div class="input-wrapper"><span class="input-icon">📁</span><input type="file" name="image" required></div></div>
            <div class="radio-group">
                <label><input type="radio" name="action" value="glitch" checked><span>Glitch</span></label>
                <label><input type="radio" name="action" value="restore"><span>Restore</span></label>
            </div>
            <button type="submit" class="action-btn" style="margin-top:20px;">Apply</button>
        </form>
        {% if result and result_type == 'glitch' %}
        <div class="result-box"><div>{{ result|safe }}</div>{% if download_link %}<a href="{{ download_link }}" download class="download-btn">Save Image</a>{% endif %}</div>
        {% endif %}
    </div>

    {% elif active_tab == 'share' %}
    <!-- FILE SHARE MODULE -->
    <div class="module-card">
        <div class="module-header">
            <div class="module-icon">☁️</div>
            <div class="module-title"><h2>File Share</h2><p>Secure File Transfer (20MB)</p></div>
        </div>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <div class="form-group"><label>Select File</label><div class="input-wrapper"><span class="input-icon">📁</span><input type="file" name="file" required></div></div>
            <button type="submit" class="action-btn" style="margin-top:20px;">Upload & Generate Link</button>
        </form>
        {% if share_link %}
        <div class="result-box">
            <div style="font-size:12px; color:rgba(255,255,255,0.7);">Link Generated:</div>
            <div style="margin-top:10px; background:rgba(0,0,0,0.3); padding:12px; word-break:break-all; border-radius:10px;">
                <a href="{{ share_link }}" target="_blank" style="color:#007aff; text-decoration:none; font-weight:500;">{{ share_link }}</a>
            </div>
            <div style="font-size:11px; color:rgba(255,255,255,0.5); margin-top:8px;">(One-Time Download Link)</div>
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
def random_name(length=8): return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ==========================================
# ROUTES
# ==========================================
@app.route('/')
def index():
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
    if not file: return render_template_string(HTML_TEMPLATE, active_tab='stego', result="Error: File upload failed.", result_type='stego')
    
    original_format = file.filename.split('.')[-1].lower()
    if original_format not in ['jpg', 'jpeg', 'png']: original_format = 'png'
    img = Image.open(file).convert('RGB')
    if img.width > 1500 or img.height > 1500: img.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
    
    if action == 'hide':
        if not message: return render_template_string(HTML_TEMPLATE, active_tab='stego', result="Error: Message empty.", result_type='stego')
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
        return render_template_string(HTML_TEMPLATE, active_tab='stego', result="Success: Payload injected.", download_link=f"data:{mime};base64,{b64}", result_type='stego')
    elif action == 'extract':
        pixels = img.load()
        binary_data = ""
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1) + str(g & 1) + str(b & 1)
                if binary_data.endswith('1111111111111110'):
                    return render_template_string(HTML_TEMPLATE, active_tab='stego', result=f"Decrypted Data:<br><span style='color:#007aff; font-size:18px; font-weight:600; margin-top:8px; display:inline-block;'>\"{bin_to_text(binary_data[:-16])}\"</span>", result_type='stego')
        return render_template_string(HTML_TEMPLATE, active_tab='stego', result="Error: No hidden data found.", result_type='stego')

# GLITCH
@app.route('/glitch', methods=['POST'])
def glitch():
    action = request.form.get('action')
    file = request.files.get('image')
    key = request.form.get('key', '')
    if not file or not key: return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="Error: Missing input.", result_type='glitch')
    
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
        return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="Success: Pixels corrupted.", download_link=f"data:{mime};base64,{b64}", result_type='glitch')
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
        return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="Success: Image restored.", download_link=f"data:{mime};base64,{b64}", result_type='glitch')

# FILE SHARE
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file: return render_template_string(HTML_TEMPLATE, active_tab='share', share_link="Error: No file selected.")
    
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
