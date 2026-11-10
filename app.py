from flask import Flask, request, render_template_string, send_from_directory
import io, os, random, string, base64, time, threading
from PIL import Image

app = Flask(__name__)
app.secret_key = "cyber_secret_key"
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ==========================================
# CSS (Same 90% Ultra-Glassy Theme)
# ==========================================
BASE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    :root { --glass-surface: rgba(10, 10, 15, 0.15); --glass-border: rgba(255, 255, 255, 0.15); --glass-blur: blur(40px); --text-primary: #ffffff; --text-secondary: rgba(255, 255, 255, 0.7); --accent-color: #00e5ff; --accent-glow: 0 0 20px rgba(0, 229, 255, 0.4); --radius-large: 24px; --radius-pill: 999px; }
    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; font-family: 'Outfit', sans-serif; }
    body { background: #050505; color: var(--text-primary); min-height: 100vh; display: flex; flex-direction: column; padding-bottom: 90px; overflow-x: hidden; position: relative; }
    body::before, body::after { content: ''; position: absolute; width: 300px; height: 300px; border-radius: 50%; filter: blur(90px); z-index: -1; animation: floatBg 15s infinite alternate ease-in-out; }
    body::before { background: rgba(0, 229, 255, 0.3); top: 10%; left: 10%; }
    body::after { background: rgba(162, 0, 255, 0.3); bottom: 20%; right: 10%; animation-delay: -5s; }
    @keyframes floatBg { 0% { transform: translate(0, 0) scale(1); } 100% { transform: translate(50px, 50px) scale(1.2); } }
    .app-header { width: 100%; background: rgba(0, 0, 0, 0.2); backdrop-filter: var(--glass-blur); border-bottom: 1px solid var(--glass-border); padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
    .header-left h1 { font-size: 24px; font-weight: 700; background: linear-gradient(90deg, #fff, var(--accent-color)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .header-left .sub { font-size: 12px; color: var(--text-secondary); font-weight: 400; letter-spacing: 1px; }
    .menu-btn { font-size: 24px; color: var(--text-primary); cursor: pointer; padding: 5px; }
    .content { flex: 1; padding: 24px 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .module-card { width: 100%; max-width: 450px; background: var(--glass-surface); backdrop-filter: var(--glass-blur); border: 1px solid var(--glass-border); border-radius: var(--radius-large); padding: 30px 24px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); animation: cardEntrance 0.6s forwards; opacity: 0; transform: translateY(30px); }
    @keyframes cardEntrance { to { opacity: 1; transform: translateY(0); } }
    .module-header { display: flex; align-items: center; gap: 16px; margin-bottom: 30px; }
    .module-icon { width: 56px; height: 56px; background: rgba(0, 229, 255, 0.1); border: 1px solid rgba(0, 229, 255, 0.3); border-radius: 20px; display: flex; justify-content: center; align-items: center; font-size: 26px; color: var(--accent-color); box-shadow: var(--accent-glow); }
    .module-title h2 { font-size: 22px; font-weight: 600; }
    .module-title p { font-size: 13px; color: var(--text-secondary); }
    .form-group { margin-bottom: 22px; }
    .form-group label { display: block; margin-bottom: 10px; font-size: 13px; color: var(--text-secondary); font-weight: 500; }
    .input-wrapper { display: flex; background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; overflow: hidden; transition: 0.3s; }
    .input-wrapper:focus-within { border-color: var(--accent-color); background: rgba(0, 0, 0, 0.4); }
    .input-icon { padding: 16px; display: flex; align-items: center; justify-content: center; color: var(--text-secondary); }
    .input-wrapper:focus-within .input-icon { color: var(--accent-color); }
    input[type="text"], input[type="file"] { width: 100%; background: transparent; border: none; color: var(--text-primary); padding: 16px 16px 16px 0; font-family: inherit; outline: none; font-size: 15px; }
    input[type="file"]::file-selector-button { background: rgba(255,255,255,0.1); color: var(--text-primary); border: 1px solid var(--glass-border); border-radius: var(--radius-pill); padding: 8px 16px; margin-right: 12px; cursor: pointer; }
    .radio-group { display: flex; gap: 12px; margin-top: 10px; }
    .radio-group label { flex: 1; text-align: center; padding: 14px; cursor: pointer; font-size: 14px; font-weight: 500; color: var(--text-secondary); background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; transition: 0.3s; }
    .radio-group input[type="radio"] { display: none; }
    .radio-group label:has(input[type="radio"]:checked) { background: rgba(0, 229, 255, 0.15); border-color: var(--accent-color); color: var(--accent-color); }
    .action-btn { width: 100%; background: linear-gradient(135deg, var(--accent-color), #009dff); color: #000; border: none; padding: 18px; font-size: 16px; font-weight: 700; cursor: pointer; border-radius: var(--radius-pill); margin-top: 24px; text-transform: uppercase; box-shadow: 0 10px 20px rgba(0, 229, 255, 0.3); }
    .action-btn:active { transform: scale(0.95); }
    .result-box { margin-top: 24px; background: rgba(0, 0, 0, 0.3); border: 1px solid var(--accent-color); padding: 20px; border-radius: 20px; font-size: 14px; text-align: center; word-wrap: break-word; }
    .download-btn { display: block; margin-top: 16px; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); color: var(--text-primary); padding: 16px; text-align: center; text-decoration: none; border-radius: var(--radius-pill); font-weight: 500; }
    .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(5, 5, 8, 0.6); backdrop-filter: blur(50px); border-top: 1px solid var(--glass-border); display: flex; justify-content: space-around; padding: 16px 0 calc(16px + env(safe-area-inset-bottom)); z-index: 99; }
    .nav-item { display: flex; flex-direction: column; align-items: center; text-decoration: none; color: var(--text-secondary); font-size: 12px; font-weight: 500; gap: 6px; }
    .nav-icon { font-size: 20px; padding: 8px 24px; border-radius: var(--radius-pill); }
    .nav-item.active { color: var(--accent-color); }
    .nav-item.active .nav-icon { background: rgba(0, 229, 255, 0.15); }
    .menu-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); backdrop-filter: blur(8px); z-index: 1000; opacity: 0; visibility: hidden; transition: 0.4s; }
    .menu-overlay.active { opacity: 1; visibility: visible; }
    .side-drawer { position: fixed; top: 0; right: -320px; width: 300px; height: 100%; background: rgba(10, 10, 15, 0.4); backdrop-filter: blur(50px); border-left: 1px solid rgba(255,255,255,0.1); z-index: 1001; transition: 0.5s; padding: 24px; overflow-y: auto; }
    .side-drawer.active { right: 0; }
    .drawer-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid var(--glass-border); padding-bottom: 15px; }
    .close-btn { font-size: 24px; color: var(--text-secondary); cursor: pointer; }
    .drawer-section { margin-bottom: 25px; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 16px; }
    .drawer-section h3 { font-size: 13px; color: var(--accent-color); margin-bottom: 12px; }
    .contact-list { list-style: none; }
    .contact-list li { display: flex; align-items: center; gap: 12px; font-size: 14px; margin-bottom: 12px; color: #fff;}
    .contact-list i { color: var(--accent-color); width: 20px; text-align: center; }
</style>
"""

# ==========================================
# HTML TEMPLATE
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Utility Tools Pro</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """ + BASE_CSS + """
</head>
<body>
<div class="app-header">
    <div class="header-left">
        <h1>Utility Tools</h1>
        <div class="sub">Ultra Secure Protocol</div>
    </div>
    <div class="menu-btn" onclick="toggleMenu()"><i class="fa-solid fa-bars-staggered"></i></div>
</div>

<div class="menu-overlay" id="menuOverlay" onclick="toggleMenu()"></div>
<div class="side-drawer" id="sideDrawer">
    <div class="drawer-header"><h2>App Menu</h2><i class="fa-solid fa-xmark close-btn" onclick="toggleMenu()"></i></div>
    <div class="drawer-section">
        <h3><i class="fa-solid fa-address-card"></i> Contact Dev</h3>
        <ul class="contact-list">
            <li><i class="fa-solid fa-user-ninja"></i> <span>Rehan</span></li>
            <li><i class="fa-solid fa-phone"></i> <span>+91 8271162035</span></li>
            <li><i class="fa-brands fa-telegram"></i> <a href="https://t.me/REHAN_OWNER" style="color:#fff;text-decoration:none;">@REHAN_OWNER</a></li>
        </ul>
    </div>
</div>

<div class="content">
    {% if active_tab == 'stego' %}
    <div class="module-card">
        <div class="module-header">
            <div class="module-icon"><i class="fa-solid fa-shield-halved"></i></div>
            <div class="module-title"><h2>Steganography</h2><p>Hide or Extract Secret Data</p></div>
        </div>
        <form method="POST" action="/stego" enctype="multipart/form-data">
            <div class="form-group">
                <label>Select Image</label>
                <div class="input-wrapper">
                    <span class="input-icon"><i class="fa-regular fa-image"></i></span>
                    <input type="file" name="image" accept="image/*" required>
                </div>
            </div>
            <div class="form-group">
                <label>Secret Message</label>
                <div class="input-wrapper">
                    <span class="input-icon"><i class="fa-regular fa-comment-dots"></i></span>
                    <input type="text" name="message" placeholder="Enter payload...">
                </div>
            </div>
            <div class="radio-group">
                <label><input type="radio" name="action" value="hide" checked><span>Hide Data</span></label>
                <label><input type="radio" name="action" value="extract"><span>Extract Data</span></label>
            </div>
            <button type="submit" class="action-btn">Execute Protocol</button>
        </form>
        {% if result and result_type == 'stego' %}
        <div class="result-box"><div>{{ result|safe }}</div>{% if download_link %}<a href="{{ download_link }}" download="secured_image.png" class="download-btn"><i class="fa-solid fa-download"></i> Save Image</a>{% endif %}</div>
        {% endif %}
    </div>
    
    {% elif active_tab == 'glitch' %}
    <div class="module-card">
        <div class="module-header">
            <div class="module-icon"><i class="fa-solid fa-bolt"></i></div>
            <div class="module-title"><h2>Glitch Module</h2><p>Corrupt or Restore Pixels</p></div>
        </div>
        <form method="POST" action="/glitch" enctype="multipart/form-data">
            <div class="form-group">
                <label>Encryption Key</label>
                <div class="input-wrapper">
                    <span class="input-icon"><i class="fa-solid fa-key"></i></span>
                    <input type="text" name="key" placeholder="Enter security key..." required>
                </div>
            </div>
            <div class="form-group">
                <label>Select Image</label>
                <div class="input-wrapper">
                    <span class="input-icon"><i class="fa-regular fa-image"></i></span>
                    <input type="file" name="image" accept="image/*" required>
                </div>
            </div>
            <div class="radio-group">
                <label><input type="radio" name="action" value="glitch" checked><span>Glitch</span></label>
                <label><input type="radio" name="action" value="restore"><span>Restore</span></label>
            </div>
            <button type="submit" class="action-btn">Apply Effect</button>
        </form>
        {% if result and result_type == 'glitch' %}
        <div class="result-box"><div>{{ result|safe }}</div>{% if download_link %}<a href="{{ download_link }}" download="glitched_image.png" class="download-btn"><i class="fa-solid fa-download"></i> Save Image</a>{% endif %}</div>
        {% endif %}
    </div>
    
    {% elif active_tab == 'share' %}
    <div class="module-card">
        <div class="module-header">
            <div class="module-icon"><i class="fa-solid fa-cloud-arrow-up"></i></div>
            <div class="module-title"><h2>File Share</h2><p>Secure File Transfer</p></div>
        </div>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <div class="form-group">
                <label>Select File (Max 20MB)</label>
                <div class="input-wrapper">
                    <span class="input-icon"><i class="fa-regular fa-folder-open"></i></span>
                    <input type="file" name="file" required>
                </div>
            </div>
            <button type="submit" class="action-btn">Upload & Generate Link</button>
        </form>
        {% if share_link %}
        <div class="result-box">
            <div style="font-size:13px; color:var(--text-secondary); margin-bottom:10px;">Link Generated:</div>
            <div style="background:rgba(0,0,0,0.5); padding:16px; word-break:break-all; border-radius:12px; border:1px solid var(--accent-color);"><a href="{{ share_link }}" target="_blank" style="color:var(--accent-color); text-decoration:none; font-weight:600;">{{ share_link }}</a></div>
            <div style="font-size:12px; color:var(--text-secondary); margin-top:12px;">(One-Time Download Link)</div>
        </div>
        {% endif %}
    </div>
    {% endif %}
</div>

<div class="bottom-nav">
    <a href="/?tab=stego" class="nav-item {% if active_tab == 'stego' %}active{% endif %}"><div class="nav-icon"><i class="fa-solid fa-camera-retro"></i></div><div>Stego</div></a>
    <a href="/?tab=glitch" class="nav-item {% if active_tab == 'glitch' %}active{% endif %}"><div class="nav-icon"><i class="fa-solid fa-bolt"></i></div><div>Glitch</div></a>
    <a href="/?tab=share" class="nav-item {% if active_tab == 'share' %}active{% endif %}"><div class="nav-icon"><i class="fa-solid fa-cloud"></i></div><div>Share</div></a>
</div>

<script>
    function toggleMenu() {
        document.getElementById('menuOverlay').classList.toggle('active');
        document.getElementById('sideDrawer').classList.toggle('active');
    }
</script>
</body>
</html>
"""

# ==========================================
# MAGIC WORD & LOGIC (100% Fixed)
# ==========================================
SECRET_MARKER = "1101101110111011" # Binary for "MAGIC"

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

def random_name(length=8): 
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ==========================================
# ROUTES
# ==========================================
@app.route('/')
def index():
    tab = request.args.get('tab', 'stego')
    if tab not in ['stego', 'glitch', 'share']: 
        tab = 'stego'
    return render_template_string(HTML_TEMPLATE, active_tab=tab)

@app.route('/stego', methods=['POST'])
def stego():
    action = request.form.get('action')
    file = request.files.get('image')
    message = request.form.get('message', '')
    
    # CHECK 1: File Uploaded?
    if not file or file.filename == '':
        return render_template_string(HTML_TEMPLATE, active_tab='stego', result="<span style='color:#ff4757;'>Error: Please select an image first!</span>", result_type='stego')
    
    try:
        img = Image.open(file).convert('RGB')
        # FIX: Resize image so it doesn't crash the server/browser memory
        img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    except:
        return render_template_string(HTML_TEMPLATE, active_tab='stego', result="<span style='color:#ff4757;'>Error: Invalid Image File.</span>", result_type='stego')
    
    # ================= HIDE =================
    if action == 'hide':
        if not message or message.strip() == '': 
            return render_template_string(HTML_TEMPLATE, active_tab='stego', result="<span style='color:#ff4757;'>Error: Message cannot be empty.</span>", result_type='stego')
        
        # Format: [MAGIC MARKER] + [MESSAGE BINARY] + [END MARKER (00000000)]
        binary_msg = SECRET_MARKER + text_to_bin(message) + '00000000'
        
        data_index = 0
        pixels = img.load()
        
        # Loop through pixels and hide 1 bit per pixel in Red channel
        for y in range(img.height):
            for x in range(img.width):
                if data_index < len(binary_msg):
                    r, g, b = pixels[x, y]
                    r = r & ~1 | int(binary_msg[data_index])
                    pixels[x, y] = (r, g, b)
                    data_index += 1
                else: break
            if data_index >= len(binary_msg): break
            
        img_io = io.BytesIO()
        img.save(img_io, 'PNG') # Force Lossless
        mime = 'image/png'
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        return render_template_string(HTML_TEMPLATE, active_tab='stego', result="<span style='color:#00e5ff;'>Success: Payload injected securely.</span>", download_link=f"data:{mime};base64,{b64}", result_type='stego')
    
    # ================= EXTRACT =================
    elif action == 'extract':
        pixels = img.load()
        binary_data = ""
        
        # Read Red channel bits
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1)
                
                # Check for Magic Marker only when we have enough bits
                if len(binary_data) >= len(SECRET_MARKER):
                    if binary_data.startswith(SECRET_MARKER):
                        # We found our marker! Now extract message until end marker
                        remaining_data = binary_data[len(SECRET_MARKER):]
                        if remaining_data.endswith('00000000'):
                            clean_binary = remaining_data[:-8]
                            if len(clean_binary) % 8 == 0:
                                decrypted = bin_to_text(clean_binary)
                                if decrypted.strip() != "":
                                    return render_template_string(HTML_TEMPLATE, active_tab='stego', result=f"<span style='color:var(--accent-color); font-size:18px; font-weight:600;'>\"{decrypted}\"</span>", result_type='stego')
                    else:
                        # If first bits don't match marker, it's not our image
                        if len(binary_data) == len(SECRET_MARKER) and not binary_data.startswith(SECRET_MARKER):
                            return render_template_string(HTML_TEMPLATE, active_tab='stego', result="<span style='color:#ff4757;'>Error: No hidden data found.</span>", result_type='stego')
                            
        return render_template_string(HTML_TEMPLATE, active_tab='stego', result="<span style='color:#ff4757;'>Error: No hidden data found.</span>", result_type='stego')

@app.route('/glitch', methods=['POST'])
def glitch():
    action = request.form.get('action')
    file = request.files.get('image')
    key = request.form.get('key', '')
    
    if not file or file.filename == '' or not key or key.strip() == '': 
        return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="<span style='color:#ff4757;'>Error: Please enter a key and select an image.</span>", result_type='glitch')
    
    try:
        img = Image.open(file).convert('RGB')
        # FIX: Resize image so it doesn't crash the server/browser memory
        img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    except:
        return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="<span style='color:#ff4757;'>Error: Invalid Image File.</span>", result_type='glitch')
    
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
        new_img.save(img_io, 'PNG') 
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="<span style='color:#00e5ff;'>Success: Pixels corrupted.</span>", download_link=f"data:image/png;base64,{b64}", result_type='glitch')
        
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
        new_img.save(img_io, 'PNG') 
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="<span style='color:#00e5ff;'>Success: Image restored.</span>", download_link=f"data:image/png;base64,{b64}", result_type='glitch')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file or file.filename == '': 
        return render_template_string(HTML_TEMPLATE, active_tab='share', share_link="<span style='color:#ff4757;'>Error: No file selected.</span>")
    
    ext = file.filename.split('.')[-1]
    filename = random_name() + "." + ext
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    host = request.host_url.rstrip('/')
    link = f"{host}/download/{filename}"
    return render_template_string(HTML_TEMPLATE, active_tab='share', share_link=link)

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
