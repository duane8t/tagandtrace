from flask import Flask, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# DATABASE
# =========================

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    used = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# =========================
# HOME
# =========================

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        user_code = request.form["code"].strip().upper()

        code = Code.query.filter_by(
            code=user_code,
            used=False
        ).first()

        if code:
            code.used = True
            db.session.commit()
            return redirect(f"/create/{user_code}")

    collage_url = url_for('static', filename='collage.jpg')

    return f"""

<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

body{{
    margin:0;
    background:#050505;
    color:white;
    font-family:-apple-system,Segoe UI,Arial,sans-serif;
    overflow-y:auto;
    overflow-x:hidden;
}}

.wrapper{{
    max-width:1180px;
    margin:auto;
    padding:8px 18px 10px;
}}

.header{{
    text-align:center;
    margin-bottom:8px;
}}

.header-inner{{
    display:inline-block;
    padding:8px 24px;
    border-radius:22px;
    border:1px solid rgba(255,255,255,0.08);
    background:rgba(255,255,255,0.02);
    box-shadow:0 4px 18px rgba(0,0,0,0.25);
}}

.header h1{{
    margin:0;
    font-size:32px;
    font-weight:800;
}}

.header p{{
    margin-top:4px;
    color:#a0a0a0;
    font-size:12px;
}}

.grid{{
    display:flex;
    justify-content:center;
    align-items:flex-start;
    gap:22px;
    flex-wrap:nowrap;
}}

.left{{
    width:360px;
    display:flex;
    flex-direction:column;
}}

.box{{
    background:#121722;
    border-radius:16px;
    padding:20px;
    box-shadow:0 4px 18px rgba(0,0,0,0.35);
}}

.box h3{{
    margin-top:0;
    margin-bottom:10px;
    font-size:22px;
}}

.box p{{
    color:#c8c8c8;
    font-size:14px;
    line-height:1.4;
}}

input{{
    width:100%;
    box-sizing:border-box;
    padding:14px;
    border:none;
    border-radius:12px;
    background:#1c2230;
    color:white;
    margin-top:12px;
    font-size:16px;
}}

button{{
    width:100%;
    padding:14px;
    border:none;
    border-radius:12px;
    background:#d4af37;
    color:black;
    font-weight:800;
    margin-top:14px;
    font-size:20px;
    cursor:pointer;
}}

.steps{{
    margin-top:16px;
    background:#121722;
    border-radius:16px;
    padding:20px;
    box-shadow:0 4px 18px rgba(0,0,0,0.35);
}}

.step{{
    display:flex;
    gap:10px;
    padding:7px 0;
    color:#f1f1f1;
    line-height:1.35;
    font-size:15px;
    align-items:flex-start;
}}

.step span{{
    color:#d4af37;
    font-weight:800;
    min-width:28px;
    font-size:17px;
}}

.features{{
    margin-top:16px;
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:12px;
}}

.feature{{
    background:#121722;
    border-radius:14px;
    padding:8px 10px;
    color:white;
    text-align:left;
    box-shadow:0 4px 18px rgba(0,0,0,0.25);
}}

.feature-title{{
    color:#d4af37;
    font-weight:800;
    margin-bottom:4px;
    font-size:14px;
}}

.feature-text{{
    color:#d8d8d8;
    font-size:12px;
    line-height:1.4;
}}

.products{{
    display:flex;
    justify-content:center;
}}

.card{{
    background:white;
    color:#111;
    width:470px;
    border-radius:18px;
    padding:10px;
    text-align:center;
    box-shadow:0 8px 24px rgba(0,0,0,0.45);
}}

.mockup-grid{{
    width:100%;
    overflow:hidden;
    border-radius:14px;
    margin-bottom:8px;
    line-height:0;
}}

.mockup-grid img{{
    width:100%;
    height:auto;
    display:block;
    border-radius:14px;
}}

.card h2{{
    margin:8px 0 4px;
    font-size:28px;
    font-weight:800;
}}

.price{{
    font-size:34px;
    font-weight:800;
    margin-bottom:4px;
}}

.small{{
    font-size:13px;
    color:#666;
    line-height:1.5;
}}

.waterproof{{
    margin-top:10px;
    border:1px solid #ececec;
    border-radius:12px;
    padding:10px;
    background:#fafafa;
}}

.waterproof-title{{
    font-weight:800;
    font-size:16px;
}}

.waterproof-sub{{
    margin-top:4px;
    color:#666;
    font-size:13px;
    line-height:1.4;
}}

.buy-btn{{
    width:100%;
    border:none;
    border-radius:12px;
    padding:12px;
    background:#d4af37;
    color:black;
    font-size:20px;
    font-weight:800;
    margin-top:12px;
    cursor:pointer;
}}

.disclaimer{{
    font-size:12px;
    color:#777;
    margin-top:10px;
    margin-bottom:8px;
    line-height:1.5;
    text-align:center;
    padding:0 8px;
}}

@media(max-width:900px){{
    .grid{{
        flex-direction:column;
        align-items:center;
    }}

    .left{{
        width:100%;
        max-width:500px;
    }}

    .card{{
        width:100%;
        max-width:470px;
    }}
}}

</style>

</head>

<body>

<div class="wrapper">

<div class="header">

<div class="header-inner">
<h1>Tag & Trace</h1>
<p>Stick it. Scan it. Get it back.</p>
</div>

</div>

<div class="grid">

<div class="left">

<div class="box">

<h3>Activate your sticker</h3>

<p>
Enter the code included in your pack
</p>

<form method="post">

<input
name="code"
placeholder="Enter code"
required
>

<button>
Activate
</button>

</form>

</div>

<div class="steps">

<div class="step">
<span>01</span>
<div>Purchase your sticker pack</div>
</div>

<div class="step">
<span>02</span>
<div>Enter your activation code</div>
</div>

<div class="step">
<span>03</span>
<div>Create your recovery profile</div>
</div>

<div class="step">
<span>04</span>
<div>Stick it on your item or pet</div>
</div>

<div class="step">
<span>05</span>
<div>If found, it can be scanned and returned</div>
</div>

</div>

<div class="features">

<div class="feature">
<div class="feature-title">
Secure & Private
</div>
<div class="feature-text">
Your data is encrypted and never shared publicly.
</div>
</div>

<div class="feature">
<div class="feature-title">
Increase Recovery
</div>
<div class="feature-text">
Boost the chances of getting lost items returned quickly.
</div>
</div>

<div class="feature">
<div class="feature-title">
Waterproof
</div>
<div class="feature-text">
Designed to survive weather and daily wear.
</div>
</div>

<div class="feature">
<div class="feature-title">
Pet Tags
</div>
<div class="feature-text">
Perfect for dogs and cats with scannable recovery stickers.
</div>
</div>

</div>

</div>

<div class="products">

<div class="card">

<div class="mockup-grid">
<img src="{collage_url}">
</div>

<h2>Sticker Pack (10)</h2>

<div class="price">
£9.99
</div>

<div class="small">
Free delivery • Secure checkout
</div>

<div class="small" style="margin-top:4px;">
Powered by PayPal • UK GDPR compliant
</div>

<div class="waterproof">

<div class="waterproof-title">
High resolution, waterproof stickers
</div>

<div class="waterproof-sub">
Durable, weatherproof and built to last
</div>

</div>

<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_blank">

<input type="hidden" name="cmd" value="_xclick">

<input
type="hidden"
name="business"
value="duane@sisco.co.uk"
>

<input
type="hidden"
name="item_name"
value="Tag & Trace Sticker Pack (10)"
>

<input
type="hidden"
name="amount"
value="9.99"
>

<input
type="hidden"
name="currency_code"
value="GBP"
>

<button type="submit" class="buy-btn">
Buy Now
</button>

</form>

<div class="disclaimer">
Tag & Trace assists with item recovery but cannot guarantee return.
</div>

</div>

</div>

</div>

</div>

</body>

</html>

"""

# =========================
# CREATE PROFILE
# =========================

@app.route("/create/<code>", methods=["GET", "POST"])
def create(code):

    if request.method == "POST":

        profile_url = f"https://tagandtrace-production.up.railway.app/profile/{code}"

        qr = qrcode.make(profile_url)

        os.makedirs("static/qrcodes", exist_ok=True)

        qr_path = f"static/qrcodes/{code}.png"

        qr.save(qr_path)

        return f'''

        <html>

        <body style="
        background:#050505;
        color:white;
        font-family:Arial;
        text-align:center;
        padding-top:80px;
        ">

        <h1>QR Code Created</h1>

        <p>Your Tag & Trace sticker is now active.</p>

        <img src="/{qr_path}" width="260">

        <br><br>

        <a
        href="/{qr_path}"
        download
        style="
        background:#d4af37;
        color:black;
        padding:14px 24px;
        border-radius:12px;
        text-decoration:none;
        font-weight:bold;
        ">
        Download QR Code
        </a>

        </body>

        </html>

        '''

    return '''

    <html>

    <body style="
    background:#050505;
    color:white;
    font-family:Arial;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
    ">

    <form method="post" style="
    background:#121722;
    padding:30px;
    border-radius:20px;
    width:420px;
    ">

    <h2 style="font-size:28px;">
    Create Your Profile
    </h2>

    <input
    name="name"
    placeholder="Name"
    required
    >

    <input
    name="details"
    placeholder="Item / Pet Details"
    required
    >

    <input
    name="phone1"
    placeholder="Primary Phone"
    required
    >

    <input
    name="phone2"
    placeholder="Secondary Phone"
    >

    <button>
    Create QR Code
    </button>

    </form>

    </body>

    </html>

    '''

# =========================
# PROFILE
# =========================

@app.route("/profile/<code>")
def profile(code):

    return f'''

    <html>

    <body style="
    background:#050505;
    color:white;
    font-family:Arial;
    text-align:center;
    padding-top:100px;
    ">

    <h1>Item Located</h1>

    <p>Please contact the owner.</p>

    <h2>{code}</h2>

    </body>

    </html>

    '''

# =========================
# ADMIN
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    auth = request.authorization

    if not auth or not (
        auth.username == "admin" and
        auth.password == "tagtrace123"
    ):
        return Response(
            "Login required",
            401,
            {
                "WWW-Authenticate":
                'Basic realm="Login Required"'
            }
        )

    if request.method == "POST":

        new_code = request.form["code"].strip().upper()

        if not Code.query.filter_by(code=new_code).first():

            db.session.add(
                Code(
                    code=new_code,
                    used=False
                )
            )

            db.session.commit()

    codes = Code.query.order_by(Code.id.desc()).all()

    return f"""

<html>

<body style="
background:#050505;
color:white;
font-family:Arial;
padding:40px;
">

<h1>Admin Panel</h1>

<form method="post">

<input
name="code"
placeholder="Enter new code"
style="
padding:12px;
width:240px;
border:none;
border-radius:10px;
background:#1c2230;
color:white;
"
>

<button style="
padding:12px 20px;
border:none;
border-radius:10px;
background:#d4af37;
font-weight:700;
margin-left:10px;
cursor:pointer;
">
Add Code
</button>

</form>

<h3 style="margin-top:40px;">
Existing Codes
</h3>

<div style="line-height:2;">
{"".join([f"<div>{c.code} — {'USED' if c.used else 'AVAILABLE'}</div>" for c in codes])}
</div>

</body>

</html>

"""

if __name__ == "__main__":
    app.run(debug=True)