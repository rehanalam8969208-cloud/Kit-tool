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
# 90% ULTRA-GLASSY & PRO ANIMATION CSS
# ==========================================
BASE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    :root { 
        /* 90% Transparent Glass */
        --glass-surface: rgba(10, 10, 15, 0.15); 
        --glass-border: rgba(255, 255, 255, 0.15); 
        --glass-blur: blur(40px); 
        
        /* Text & Accents */
        --text-primary: #ffffff; 
        --text-secondary: rgba(255, 255, 255, 0.7); 
        --accent-color: #00e5ff; 
        --accent-glow: 0 0 20px rgba(0, 229, 255, 0.4);
        
        --radius-large: 24px; 
        --radius-pill: 999px; 
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; font-family: 'Outfit', sans-serif; }
    
    /* Animated Aurora Background for Glass Effect */
    body { 
        background: #050505; 
        color: var(--text-primary); 
        min-height: 100vh; 
        display: flex; 
        flex-direction: column; 
        padding-bottom: 90px; 
        overflow-x: hidden; 
        position: relative;
    }
    
    body::before, body::after {
        content: ''; position: absolute; width: 300px; height: 300px;
        border-radius: 50%; filter: blur(90px); z-index: -1;
        animation: floatBg 15s infinite alternate ease-in-out;
    }
    body::before { background: rgba(0, 229, 255, 0.3); top: 10%; left: 10%; }
    body::after { background: rgba(162, 0, 255, 0.3); bottom: 20%; right: 10%; animation-delay: -5s; }

    @keyframes floatBg {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(50px, 50px) scale(1.2); }
    }

    /* --- HEADER --- */
    .app-header { 
        width: 100%; 
        background: rgba(0, 0, 0, 0.2); 
        backdrop-filter: var(--glass-blur); -webkit-backdrop-filter: var(--glass-blur);
        border-bottom: 1px solid var(--glass-border); 
        padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; 
        position: sticky; top: 0; z-index: 100; 
    }
    .header-left h1 { font-size: 24px; font-weight: 700; background: linear-gradient(90deg, #fff, var(--accent-color)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .header-left .sub { font-size: 12px; color: var(--text-secondary); font-weight: 400; letter-spacing: 1px; }
    .menu-btn { font-size: 24px; color: var(--text-primary); cursor: pointer; transition: 0.3s; padding: 5px; }
    .menu-btn:hover { color: var(--accent-color); transform: scale(1.1); }

    /* --- MAIN CONTENT --- */
    .content { flex: 1; padding: 24px 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    
    .module-card { 
        width: 100%; max-width: 450px; 
        background: var(--glass-surface); 
        backdrop-filter: var(--glass-blur); -webkit-backdrop-filter: var(--glass-blur);
        border: 1px solid var(--glass-border); 
        border-radius: var(--radius-large); 
        padding: 30px 24px; 
        box-shadow: 0 20px 50px rgba(0,0,0,0.5), inset 0 0 0 1px rgba(255,255,255,0.05); 
        animation: cardEntrance 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; 
        opacity: 0; transform: translateY(30px);
    }
    @keyframes cardEntrance { to { opacity: 1; transform: translateY(0); } }

    .module-header { display: flex; align-items: center; gap: 16px; margin-bottom: 30px; }
    .module-icon { width: 56px; height: 56px; background: rgba(0, 229, 255, 0.1); border: 1px solid rgba(0, 229, 255, 0.3); border-radius: 20px; display: flex; justify-content: center; align-items: center; font-size: 26px; color: var(--accent-color); box-shadow: var(--accent-glow); animation: pulseGlow 2s infinite alternate; }
    @keyframes pulseGlow { from { box-shadow: 0 0 10px rgba(0,229,255,0.2); } to { box-shadow: 0 0 25px rgba(0,229,255,0.6); } }
    .module-title h2 { font-size: 22px; font-weight: 600; }
    .module-title p { font-size: 13px; color: var(--text-secondary); }

    /* --- FORMS --- */
    .form-group { margin-bottom: 22px; }
    .form-group label { display: block; margin-bottom: 10px; font-size: 13px; color: var(--text-secondary); font-weight: 500; }
    .input-wrapper { display: flex; background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; overflow: hidden; transition: 0.3s ease; }
    .input-wrapper:focus-within { border-color: var(--accent-color); background: rgba(0, 0, 0, 0.4); box-shadow: 0 0 15px rgba(0,229,255,0.2); transform: translateY(-2px); }
    .input-icon { padding: 16px; display: flex; align-items: center; justify-content: center; color: var(--text-secondary); transition: 0.3s; }
    .input-wrapper:focus-within .input-icon { color: var(--accent-color); }
    
    input[type="text"], input[type="file"] { width: 100%; background: transparent; border: none; color: var(--text-primary); padding: 16px 16px 16px 0; font-family: inherit; outline: none; font-size: 15px; }
    input[type="file"]::file-selector-button { background: rgba(255,255,255,0.1); color: var(--text-primary); border: 1px solid var(--glass-border); border-radius: var(--radius-pill); padding: 8px 16px; margin-right: 12px; cursor: pointer; transition: 0.3s; }
    input[type="file"]::file-selector-button:hover { background: rgba(255,255,255,0.2); }

    /* --- RADIOS --- */
    .radio-group { display: flex; gap: 12px; margin-top: 10px; }
    .radio-group label { flex: 1; text-align: center; padding: 14px; cursor: pointer; font-size: 14px; font-weight: 500; color: var(--text-secondary); background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; transition: 0.3s; }
    .radio-group input[type="radio"] { display: none; }
    .radio-group label:has(input[type="radio"]:checked) { background: rgba(0, 229, 255, 0.15); border-color: var(--accent-color); color: var(--accent-color); box-shadow: inset 0 0 15px rgba(0,229,255,0.2); }

    /* --- BUTTONS --- */
    .action-btn { width: 100%; background: linear-gradient(135deg, var(--accent-color), #009dff); color: #000; border: none; padding: 18px; font-size: 16px; font-weight: 700; cursor: pointer; border-radius: var(--radius-pill); margin-top: 24px; transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 10px 20px rgba(0, 229, 255, 0.3); }
    .action-btn:hover { transform: translateY(-3px); box-shadow: 0 15px 25px rgba(0, 229, 255, 0.5); }
    .action-btn:active { transform: scale(0.95); }

    .result-box { margin-top: 24px; background: rgba(0, 0, 0, 0.3); border: 1px solid var(--accent-color); padding: 20px; border-radius: 20px; font-size: 14px; text-align: center; word-wrap: break-word; animation: fadeInUp 0.5s; box-shadow: 0 0 20px rgba(0,229,255,0.1); }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    
    .download-btn { display: block; margin-top: 16px; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); color: var(--text-primary); padding: 16px; text-align: center; text-decoration: none; border-radius: var(--radius-pill); font-weight: 500; transition: 0.3s; backdrop-filter: blur(10px); }
    .download-btn:hover { background: rgba(255,255,255,0.15); border-color: var(--accent-color); }

    /* --- BOTTOM NAV --- */
    .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(5, 5, 8, 0.6); backdrop-filter: blur(50px); -webkit-backdrop-filter: blur(50px); border-top: 1px solid var(--glass-border); display: flex; justify-content: space-around; padding: 16px 0 calc(16px + env(safe-area-inset-bottom)); z-index: 99; }
    .nav-item { display: flex; flex-direction: column; align-items: center; text-decoration: none; color: var(--text-secondary); font-size: 12px; font-weight: 500; transition: 0.3s; gap: 6px; }
    .nav-icon { font-size: 20px; padding: 8px 24px; border-radius: var(--radius-pill); transition: 0.4s cubic-bezier(0.2, 0.8, 0.2, 1); }
    .nav-item.active { color: var(--accent-color); }
    .nav-item.active .nav-icon { background: rgba(0, 229, 255, 0.15); box-shadow: inset 0 0 10px rgba(0,229,255,0.2); }
    
    /* --- SIDE DRAWER (PRO GLASS) --- */
    .menu-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); backdrop-filter: blur(8px); z-index: 1000; opacity: 0; visibility: hidden; transition: 0.4s; }
    .menu-overlay.active { opacity: 1; visibility: visible; }
    
    .side-drawer { position: fixed; top: 0; right: -320px; width: 300px; height: 100%; background: rgba(10, 10, 15, 0.4); backdrop-filter: blur(50px); -webkit-backdrop-filter: blur(50px); border-left: 1px solid rgba(255,255,255,0.1); z-index: 1001; transition: 0.5s cubic-bezier(0.2, 0.8, 0.2, 1); padding: 24px; box-shadow: -20px 0 50px rgba(0,0,0,0.5); overflow-y: auto; }
    .side-drawer.active { right: 0; }
    
    .drawer-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid var(--glass-border); padding-bottom: 15px; }
    .drawer-header h2 { font-size: 20px; font-weight: 700; color: var(--text-primary); }
    .close-btn { font-size: 24px; color: var(--text-secondary); cursor: pointer; transition: 0.3s; }
    .close-btn:hover { color: #ff4757; transform: rotate(90deg); }
    
    .drawer-section { margin-bottom: 25px; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); }
    .drawer-section h3 { font-size: 13px; color: var(--accent-color); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
    .drawer-section p { font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
    
    /* Contact List */
    .contact-list { list-style: none; }
    .contact-list li { display: flex; align-items: center; gap: 12px; font-size: 14px; margin-bottom: 12px; }
    .contact-list i { color: var(--accent-color); font-size: 16px; width: 20px; text-align: center; }
    .contact-list a { color: var(--text-primary); text-decoration: none; transition: 0.2s; }
    .contact-list a:hover { color: var(--accent-color); text-shadow: 0 0 10px rgba(0,229,255,0.5); }
    
    /* Instruction Manual styling */
    .instructions { list-style: none; }
    .instructions li { font-size: 12px; color: rgba(255,255,255,0.8); margin-bottom: 10px; padding-left: 15px; position: relative; }
    .instructions li::before { content: '>'; position: absolute; left: 0; color: var(--accent-color); font-weight: bold; }
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

<!-- HEADER -->
<div class="app-header">
    <div class="header-left">
        <h1>Utility Tools</h1>
        <div class="sub">Ultra Secure Protocol</div>
    </div>
    <div class="menu-btn" onclick="toggleMenu()">
        <i class="fa-solid fa-bars-staggered"></i>
    </div>
</div>

<!-- SIDE DRAWER MENU -->
<div class="menu-overlay" id="menuOverlay" onclick="toggleMenu()"></div>
<div class="side-drawer" id="sideDrawer">
    <div class="drawer-header">
        <h2>App Menu</h2>
        <i class="fa-solid fa-xmark close-btn" onclick="toggleMenu()"></i>
    </div>
    
    <div class="drawer-section">
        <h3><i class="fa-solid fa-book-open"></i> How To Use</h3>
        <ul class="instructions">
            <li><b>Stego:</b> Hide text inside an image using magic bits. To extract, upload the modified image and select Extract.</li>
            <li><b>Glitch:</b> Corrupt an image using a secret key. Use the exact same key in Restore mode to fix it.</li>
            <li><b>Share:</b> Upload up to 20MB file. The link works only once and auto-deletes the file.</li>
        </ul>
    </div>

    <div class="drawer-section">
        <h3><i class="fa-solid fa-address-card"></i> Contact Dev</h3>
        <ul class="contact-list">
            <li><i class="fa-solid fa-user-ninja"></i> <span>Developer: Rehan</span></li>
            <li><i class="fa-solid fa-phone"></i> <span>+91 8271162035</span></li>
            <li><i class="fa-solid fa-envelope"></i> <span style="font-size: 11px;">rehanalam8969208@gmail.com</span></li>
            <li><i class="fa-brands fa-telegram"></i> <a href="https://t.me/REHAN_OWNER" target="_blank">t.me/REHAN_OWNER</a></li>
        </ul>
    </div>
</div>

<!-- MAIN CONTENT -->
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
                    <input type="file" name="image" required>
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
        <div class="result-box"><div>{{ result|safe }}</div>{% if download_link %}<a href="{{ download_link }}" download class="download-btn"><i class="fa-solid fa-download"></i> Save Image</a>{% endif %}</div>
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
                    <input type="file" name="image" required>
                </div>
            </div>
            <div class="radio-group">
                <label><input type="radio" name="action" value="glitch" checked><span>Glitch</span></label>
                <label><input type="radio" name="action" value="restore"><span>Restore</span></label>
            </div>
            <button type="submit" class="action-btn">Apply Effect</button>
        </form>
        {% if result and result_type == 'glitch' %}
        <div class="result-box"><div>{{ result|safe }}</div>{% if download_link %}<a href="{{ download_link }}" download class="download-btn"><i class="fa-solid fa-download"></i> Save Image</a>{% endif %}</div>
        {% endif %}
    </div>
    
    {% elif active_tab == 'share' %}
    <div class="module-card">
        <div class="module-header">
            <div class="module-icon"><i class="fa-solid fa-cloud-arrow-up"></i></div>
            <div class="module-title"><h2>File Share</h2><p>Secure File Transfer (20MB)</p></div>
        </div>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <div class="form-group">
                <label>Select File</label>
                <div class="input-wrapper">
                    <span class="input-icon"><i class="fa-regular fa-folder-open"></i></span>
                    <input type="file" name="file" required>
                </div>
            </div>
            <button type="submit" class="action-btn">Upload & Generate Link</button>
        </form>
        {% if share_link %}
        <div class="result-box">
            <div style="font-size:13px; color:var(--text-secondary); margin-bottom:10px;">Link Generated Successfully:</div>
            <div style="background:rgba(0,0,0,0.5); padding:16px; word-break:break-all; border-radius:12px; border:1px solid rgba(0,229,255,0.3); box-shadow: inset 0 0 10px rgba(0,0,0,0.5);">
                <a href="{{ share_link }}" target="_blank" style="color:var(--accent-color); text-decoration:none; font-weight:600; letter-spacing:0.5px;">{{ share_link }}</a>
            </div>
            <div style="font-size:12px; color:var(--text-secondary); margin-top:12px;"><i class="fa-solid fa-stopwatch"></i> One-Time Download Link</div>
        </div>
        {% endif %}
    </div>
    {% endif %}
</div>

<!-- BOTTOM NAVIGATION -->
<div class="bottom-nav">
    <a href="/?tab=stego" class="nav-item {% if active_tab == 'stego' %}active{% endif %}">
        <div class="nav-icon"><i class="fa-solid fa-camera-retro"></i></div>
        <div>Stego</div>
    </a>
    <a href="/?tab=glitch" class="nav-item {% if active_tab == 'glitch' %}active{% endif %}">
        <div class="nav-icon"><i class="fa-solid fa-bolt"></i></div>
        <div>Glitch</div>
    </a>
    <a href="/?tab=share" class="nav-item {% if active_tab == 'share' %}active{% endif %}">
        <div class="nav-icon"><i class="fa-solid fa-cloud"></i></div>
        <div>Share</div>
    </a>
</div>

<script>
    // Drawer Logic
    function toggleMenu() {
        const overlay = document.getElementById('menuOverlay');
        const drawer = document.getElementById('sideDrawer');
        overlay.classList.toggle('active');
        drawer.classList.toggle('active');
    }
</script>

</body>
</html>
"""

# ==========================================
# MAGIC WORD & LOGIC (Foolproof)
# ==========================================
# Yeh raaz ka code hai. Har photo me message ke shuru me yeh chhip jayega.
SECRET_MARKER = "1101101110111011" # Binary for "MAGIC"

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
    if tab not in ['stego', 'glitch', 'share']: tab = 'stego'
    return render_template_string(HTML_TEMPLATE, active_tab=tab)

@app.route('/stego', methods=['POST'])
def stego():
    action = request.form.get('action')
    file = request.files.get('image')
    message = request.form.get('message', '')
    if not file: return render_template_string(HTML_TEMPLATE, active_tab='stego', result="Error: File upload failed.", result_type='stego')
    
    img = Image.open(file).convert('RGB')
    
    if action == 'hide':
        if not message: return render_template_string(HTML_TEMPLATE, active_tab='stego', result="Error: Message empty.", result_type='stego')
        
        # Format: [MAGIC MARKER] + [MESSAGE BINARY] + [END MARKER]
        binary_msg = SECRET_MARKER + text_to_bin(message) + '00000000'
        
        data_index = 0
        pixels = img.load()
        
        # Har pixel ke R channel (Red) me 1 bit chhipayenge
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
        img.save(img_io, 'PNG') # 100% Lossless
        mime = 'image/png'
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        return render_template_string(HTML_TEMPLATE, active_tab='stego', result="Success: Payload injected securely.", download_link=f"data:{mime};base64,{b64}", result_type='stego')
    
    elif action == 'extract':
        pixels = img.load()
        binary_data = ""
        
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1)
                
                # Check karo ki Magic Marker mila kya
                if len(binary_data) >= len(SECRET_MARKER):
                    if binary_data.startswith(SECRET_MARKER):
                        # Magic marker mil gaya, ab aage ka data nikaalo
                        remaining_data = binary_data[len(SECRET_MARKER):]
                        if remaining_data.endswith('00000000'):
                            clean_binary = remaining_data[:-8]
                            if len(clean_binary) % 8 == 0:
                                decrypted = bin_to_text(clean_binary)
                                if decrypted.strip() != "":
                                    return render_template_string(HTML_TEMPLATE, active_tab='stego', result=f"Decrypted Data:<br><span style='color:var(--accent-color); font-size:18px; font-weight:600; margin-top:10px; display:inline-block;'>\"{decrypted}\"</span>", result_type='stego')
                            
        return render_template_string(HTML_TEMPLATE, active_tab='stego', result="Error: No hidden data found (or file was compressed).", result_type='stego')

@app.route('/glitch', methods=['POST'])
def glitch():
    action = request.form.get('action')
    file = request.files.get('image')
    key = request.form.get('key', '')
    if not file or not key: return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="Error: Missing input.", result_type='glitch')
    
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
        new_img.save(img_io, 'PNG') 
        img_io.seek(0)
        b64 = base64.b64encode(img_io.getvalue()).decode()
        return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="Success: Pixels corrupted.", download_link=f"data:image/png;base64,{b64}", result_type='glitch')
        
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
        return render_template_string(HTML_TEMPLATE, active_tab='glitch', result="Success: Image restored.", download_link=f"data:image/png;base64,{b64}", result_type='glitch')

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
