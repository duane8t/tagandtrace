from flask import Flask, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os

app = Flask(__name__)

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

with app.app_context():
    db.create_all()

# =========================================================
# HOME PAGE
# =========================================================

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

    return """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Tag & Trace | QR Lost Property Stickers UK</title>

<meta name="description" content="Professional QR recovery stickers for pets, bikes, keys, luggage and valuables across the UK.">

<meta name="keywords" content="QR pet tags UK, QR lost property stickers, QR recovery labels, waterproof QR stickers">

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
}

body{
font-family:'Inter',sans-serif;
background:#020617;
color:white;
overflow-x:hidden;
}

.container{
max-width:1280px;
margin:auto;
padding:0 20px;
}

header{
position:sticky;
top:0;
z-index:1000;
background:rgba(2,6,23,0.95);
backdrop-filter:blur(10px);
border-bottom:1px solid rgba(255,255,255,0.08);
}

.nav{
display:flex;
justify-content:space-between;
align-items:center;
padding:20px 0;
}

.logo{
font-size:34px;
font-weight:800;
color:#facc15;
}

.nav-links{
display:flex;
gap:25px;
}

.nav-links a{
color:white;
text-decoration:none;
font-weight:500;
}

.hero{
padding:90px 0;
display:grid;
grid-template-columns:1.1fr 1fr;
gap:50px;
align-items:center;
}

.hero h1{
font-size:68px;
line-height:1.05;
margin-bottom:25px;
font-weight:800;
}

.highlight{
color:#facc15;
}

.hero p{
font-size:21px;
color:#cbd5e1;
margin-bottom:35px;
}

.cta-row{
display:flex;
gap:15px;
flex-wrap:wrap;
}

.btn{
padding:16px 32px;
border-radius:14px;
font-weight:700;
text-decoration:none;
display:inline-block;
transition:0.3s;
}

.btn-primary{
background:#facc15;
color:black;
border:none;
cursor:pointer;
}

.btn-secondary{
border:1px solid rgba(255,255,255,0.2);
color:white;
}

.hero-card{
background:linear-gradient(180deg,#111827,#1e293b);
padding:30px;
border-radius:28px;
box-shadow:0 20px 60px rgba(0,0,0,0.4);
}

.hero-card img{
width:100%;
border-radius:18px;
margin-bottom:20px;
}

.price{
font-size:54px;
font-weight:800;
color:#facc15;
margin:20px 0;
}

.activate-box{
margin-top:30px;
background:#111827;
padding:25px;
border-radius:22px;
}

.activate-box input{
width:100%;
padding:16px;
border:none;
border-radius:12px;
margin-top:15px;
margin-bottom:15px;
font-size:16px;
background:#1e293b;
color:white;
}

.section{
padding:90px 0;
}

.section-title{
text-align:center;
font-size:44px;
margin-bottom:20px;
font-weight:800;
}

.section-sub{
text-align:center;
max-width:850px;
margin:auto auto 50px;
color:#cbd5e1;
font-size:18px;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
gap:24px;
}

.card{
background:#111827;
padding:28px;
border-radius:24px;
border:1px solid rgba(255,255,255,0.06);
}

.icon{
font-size:42px;
margin-bottom:15px;
}

.steps{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
gap:25px;
margin-top:50px;
}

.step{
background:#111827;
padding:25px;
border-radius:22px;
position:relative;
}

.step-number{
position:absolute;
top:-15px;
left:20px;
background:#facc15;
color:black;
padding:8px 14px;
font-weight:800;
border-radius:999px;
}

.faq{
max-width:900px;
margin:auto;
}

.faq-item{
background:#111827;
padding:24px;
border-radius:18px;
margin-bottom:18px;
}

footer{
background:black;
padding:60px 0;
margin-top:70px;
}

.footer-grid{
display:grid;
grid-template-columns:2fr 1fr 1fr;
gap:40px;
}

footer a{
display:block;
color:#cbd5e1;
text-decoration:none;
margin-bottom:10px;
}

.small{
margin-top:30px;
font-size:14px;
color:#94a3b8;
}

@media(max-width:900px){

.hero{
grid-template-columns:1fr;
}

.hero h1{
font-size:48px;
}

.nav-links{
display:none;
}

.footer-grid{
grid-template-columns:1fr;
}

}

</style>
</head>

<body>

<header>

<div class="container nav">

<div class="logo">
Tag & Trace
</div>

<div class="nav-links">
<a href="#features">Features</a>
<a href="#how">How It Works</a>
<a href="#faq">FAQ</a>
<a href="#contact">Contact</a>
</div>

</div>

</header>

<section class="hero container">

<div>

<h1>
Never Lose Your
<span class="highlight">Valuables</span>
Again.
</h1>

<p>
Professional waterproof QR recovery stickers for pets, keys, luggage, bikes and valuables.
Fast activation. Secure recovery. No app required.
</p>

<div class="cta-row">
<a href="#buy" class="btn btn-secondary">How It Works</a>
</div>

<div class="activate-box">

<h2>
Activate Your Sticker
</h2>

<form method="POST">

<input
type="text"
name="code"
placeholder="Enter activation code"
required
>

<button type="submit" class="btn btn-primary">
Activate Sticker
</button>

</form>

</div>

</div>

<div class="hero-card">

<img src="https://images.unsplash.com/photo-1517849845537-4d257902454a?q=80&w=1200&auto=format&fit=crop">

<h2>
Starter Sticker Pack
</h2>

<div class="price">
£9.99
</div>

<p>
10 waterproof high-quality QR recovery stickers.
</p>

<br>

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
value="Tag & Trace Sticker Pack"
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

<button type="submit" class="btn btn-primary">
Buy Now
</button>

</form>

</div>

</section>

<section class="section" id="features">

<div class="container">

<h2 class="section-title">
Why People Choose Tag & Trace
</h2>

<p class="section-sub">
Perfect for pets, keys, luggage, bikes, tools, electronics and valuables.
</p>

<div class="grid">

<div class="card">
<div class="icon">🔒</div>
<h3>Private & Secure</h3>
<p>Your information stays encrypted and protected.</p>
</div>

<div class="card">
<div class="icon">💧</div>
<h3>Waterproof</h3>
<p>Weatherproof stickers built for outdoor use.</p>
</div>

<div class="card">
<div class="icon">📱</div>
<h3>No App Needed</h3>
<p>Any smartphone can instantly scan the QR code.</p>
</div>

<div class="card">
<div class="icon">⚡</div>
<h3>Fast Recovery</h3>
<p>Boost the chances of getting lost items returned quickly.</p>
</div>

</div>

</div>

</section>

<section class="section" id="how">

<div class="container">

<h2 class="section-title">
How It Works
</h2>

<div class="steps">

<div class="step">
<div class="step-number">01</div>
<h3>Purchase</h3>
<p>Choose your QR sticker pack.</p>
</div>

<div class="step">
<div class="step-number">02</div>
<h3>Activate</h3>
<p>Enter your unique activation code online.</p>
</div>

<div class="step">
<div class="step-number">03</div>
<h3>Create Profile</h3>
<p>Add secure recovery details.</p>
</div>

<div class="step">
<div class="step-number">04</div>
<h3>Stick & Protect</h3>
<p>Apply stickers to valuables and pets.</p>
</div>

</div>

</div>

</section>

<section class="section" id="faq">

<div class="container">

<h2 class="section-title">
Frequently Asked Questions
</h2>

<div class="faq">

<div class="faq-item">
<h3>Do I need an app?</h3>
<p>No. Any smartphone can scan the QR code.</p>
</div>

<div class="faq-item">
<h3>Are the stickers waterproof?</h3>
<p>Yes. They are designed for long-term outdoor use.</p>
</div>

<div class="faq-item">
<h3>What can I use them on?</h3>
<p>Pets, keys, bikes, luggage, electronics and valuables.</p>
</div>

<div class="faq-item">
<h3>Is my information public?</h3>
<p>No. Your information remains secure and private.</p>
</div>

</div>

</div>

</section>

<footer id="contact">

<div class="container footer-grid">

<div>

<h2 class="logo">
Tag & Trace
</h2>

<p class="small">
QR lost property stickers and pet recovery tags designed for modern protection.
</p>

</div>

<div>

<h3>Links</h3>

<br>

<a href="#">Home</a>
<a href="#features">Features</a>
<a href="#faq">FAQ</a>

</div>

<div>

<h3>Contact</h3>

<br>

<a href="mailto:support@tagandtrace.co.uk">
support@tagandtrace.co.uk
</a>

<a href="https://www.tagandtrace.co.uk">
www.tagandtrace.co.uk
</a>

</div>

</div>

<div class="container small">
© 2026 Tag & Trace UK. All rights reserved.
</div>

</footer>

</body>

</html>

"""

# =========================================================
# CREATE PROFILE
# =========================================================

@app.route("/create/<code>", methods=["GET", "POST"])
def create(code):

    if request.method == "POST":

        profile_url = f"https://www.tagandtrace.co.uk/profile/{code}"

        qr = qrcode.make(profile_url)

        os.makedirs("static/qrcodes", exist_ok=True)

        qr_path = f"static/qrcodes/{code}.png"

        qr.save(qr_path)

        return f'''

        <html>

        <body style="
        background:#020617;
        color:white;
        font-family:Arial;
        text-align:center;
        padding-top:100px;
        ">

        <h1>
        QR Code Created
        </h1>

        <p>
        Your Tag & Trace sticker is now active.
        </p>

        <br>

        <img src="/{qr_path}" width="280">

        <br><br>

        <a
        href="/{qr_path}"
        download
        style="
        background:#facc15;
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
    background:#020617;
    color:white;
    font-family:Arial;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
    ">

    <form method="POST" style="
    background:#111827;
    padding:40px;
    border-radius:24px;
    width:420px;
    ">

    <h1>
    Create Profile
    </h1>

    <input
    name="name"
    placeholder="Name"
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
    placeholder="Phone Number"
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
    background:#facc15;
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

    return f'''

    <html>

    <body style="
    background:#020617;
    color:white;
    font-family:Arial;
    text-align:center;
    padding-top:100px;
    ">

    <h1>
    Item Located
    </h1>

    <p>
    Please contact the owner regarding this item.
    </p>

    <h2>
    Reference:
    {code}
    </h2>

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

    {"".join([f"<div>{c.code} — {'USED' if c.used else 'AVAILABLE'}</div>" for c in codes])}

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