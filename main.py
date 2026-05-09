from flask import Flask, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os

app = Flask(__name__)

# =========================================================
# CONFIG
# =========================================================

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "changeme123")

# =========================================================
# DATABASE
# =========================================================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True)
    used = db.Column(db.Boolean, default=False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(50), unique=True)

    name = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    phone2 = db.Column(db.String(50))
    email = db.Column(db.String(120))
    details = db.Column(db.String(500))

with app.app_context():
    db.create_all()

# =========================================================
# HOME PAGE
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    error = ""

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
        else:
            error = "Invalid or already used activation code"

    collage_url = url_for('static', filename='collage2.jpg')

    error_html = ""

    if error:
        error_html = f'''
        <div class="error">
        {error}
        </div>
        '''

    return f"""

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Tag Scan Return UK</title>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>

body{{
    margin:0;
    background:#050505;
    color:white;
    font-family:'Inter',sans-serif;
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

.error{{
    background:#7f1d1d;
    padding:12px;
    border-radius:12px;
    margin-top:12px;
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
    display:block;
    border-radius:14px;
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
        margin:auto;
    }}

    .wrapper{{
        padding:12px;
    }}
}}

</style>

</head>

<body>

<div class="wrapper">

<div class="header">

<div class="header-inner">
<h1>Tag <span style="color:#d4af37;">SCAN</span> Return</h1>
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

{error_html}

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

</div>

<div class="products">

<div class="card">

<div class="mockup-grid">
<img src="{collage_url}">
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
value="TagScanReturn Sticker Pack (10)"
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

</div>

</div>

</div>

</div>

</body>

</html>

"""

# =========================================================
# CREATE PROFILE
# =========================================================

@app.route("/create/<code>", methods=["GET", "POST"])
def create(code):

    if request.method == "POST":

        existing = Profile.query.filter_by(code=code).first()

        if existing:
            return redirect(f"/profile/{code}")

        profile = Profile(
            code=code,
            name=request.form.get("name"),
            phone=request.form.get("phone"),
            phone2=request.form.get("phone2"),
            email=request.form.get("email"),
            details=request.form.get("details")
        )

        db.session.add(profile)
        db.session.commit()

        profile_url = f"https://www.tagscanreturn.co.uk/profile/{code}"

        qr = qrcode.make(profile_url)

        os.makedirs("static/qrcodes", exist_ok=True)

        qr_path = f"static/qrcodes/{code}.png"

        qr.save(qr_path)

        return redirect(f"/profile/{code}")

    return '''

<html>

<body style="
background:#020617;
color:white;
font-family:Arial;
display:flex;
justify-content:center;
align-items:center;
min-height:100vh;
padding:20px;
">

<form method="POST" style="
background:#111827;
padding:40px;
border-radius:24px;
width:100%;
max-width:460px;
">

<h1>Create Profile</h1>

<input
name="name"
placeholder="Full Name"
required
style="
width:100%;
padding:14px;
margin-top:14px;
border:none;
border-radius:12px;
background:#1e293b;
color:white;
"
>

<input
name="phone"
placeholder="Primary Phone Number"
required
style="
width:100%;
padding:14px;
margin-top:14px;
border:none;
border-radius:12px;
background:#1e293b;
color:white;
"
>

<input
name="phone2"
placeholder="Secondary Phone Number"
style="
width:100%;
padding:14px;
margin-top:14px;
border:none;
border-radius:12px;
background:#1e293b;
color:white;
"
>

<input
name="email"
placeholder="Email Address"
style="
width:100%;
padding:14px;
margin-top:14px;
border:none;
border-radius:12px;
background:#1e293b;
color:white;
"
>

<input
name="details"
placeholder="Item / Pet Details"
required
style="
width:100%;
padding:14px;
margin-top:14px;
border:none;
border-radius:12px;
background:#1e293b;
color:white;
"
>

<button style="
width:100%;
padding:14px;
margin-top:18px;
border:none;
border-radius:12px;
background:#d4af37;
font-weight:bold;
">
Generate QR
</button>

</form>

</body>

</html>

'''

# =========================================================
# PROFILE
# =========================================================

@app.route("/profile/<code>")
def profile(code):

    profile = Profile.query.filter_by(code=code).first()

    if not profile:
        return "Profile not found"

    phone2_html = ""

    if profile.phone2:
        phone2_html = f'''
        <a
        href="tel:{profile.phone2}"
        class="btn"
        >
        Backup Contact
        </a>
        '''

    email_html = ""

    if profile.email:
        email_html = f'''
        <a
        href="mailto:{profile.email}"
        class="btn"
        >
        Email Owner
        </a>
        '''

    return f'''

<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body{{
    margin:0;
    background:#050816;
    color:white;
    font-family:Arial,sans-serif;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
    padding:20px;
    box-sizing:border-box;
}}

.card{{
    width:100%;
    max-width:520px;
    background:#0f172a;
    border-radius:28px;
    padding:38px;
    text-align:center;
}}

.btn{{
    display:block;
    width:100%;
    background:#d4af37;
    color:black;
    text-decoration:none;
    padding:18px;
    border-radius:16px;
    font-size:20px;
    font-weight:800;
    margin-top:16px;
    box-sizing:border-box;
}}

.details{{
    margin-top:28px;
    background:#111827;
    padding:24px;
    border-radius:20px;
    text-align:left;
    line-height:1.8;
}}

</style>

</head>

<body>

<div class="card">

<h1>
Item Located
</h1>

<p>
Please contact the owner below.
</p>

<a
href="tel:{profile.phone}"
class="btn"
>
Call Owner
</a>

{phone2_html}

{email_html}

<div class="details">

<strong>Owner:</strong><br>
{profile.name}

<br><br>

<strong>Item / Pet Details:</strong><br>
{profile.details}

</div>

</div>

</body>

</html>

'''

# =========================================================
# ADMIN PANEL
# =========================================================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    auth = request.authorization

    if not auth or not (
        auth.username == ADMIN_USER and
        auth.password == ADMIN_PASS
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

    codes_html = ""

    for c in codes:
        status = "USED" if c.used else "AVAILABLE"
        codes_html += f"<div>{c.code} — {status}</div>"

    return f"""

<html>

<body style="
background:#020617;
color:white;
font-family:Arial;
padding:40px;
">

<h1>
Admin Dashboard
</h1>

<form method="POST">

<input
name="code"
placeholder="Enter new activation code"
style="
padding:14px;
width:300px;
border:none;
border-radius:12px;
background:#1e293b;
color:white;
"
>

<button style="
padding:14px 24px;
border:none;
border-radius:12px;
background:#facc15;
font-weight:bold;
margin-left:10px;
">
Add Code
</button>

</form>

<br><br>

<h2>
Existing Codes
</h2>

<div style="line-height:2;">

{codes_html}

</div>

</body>

</html>

"""

# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)