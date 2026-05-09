from flask import Flask, request, redirect, url_for, Response, render_template_string
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================================================
# DATABASE
# =========================================================

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    phone2 = db.Column(db.String(50))
    email = db.Column(db.String(120))
    details = db.Column(db.String(500))

with app.app_context():
    db.create_all()

# =========================================================
# CONFIG
# =========================================================

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "duanepipe")

DOMAIN = os.environ.get(
    "DOMAIN",
    "https://www.tagscanreturn.co.uk"
)

# =========================================================
# HOME
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    error = ""

    if request.method == "POST":

        user_code = request.form.get("code", "").strip().upper()

        code = Code.query.filter_by(
            code=user_code,
            used=False
        ).first()

        if code:
            return redirect(f"/create/{user_code}")
        else:
            error = "Invalid or already used activation code"

    collage_url = url_for('static', filename='collage2.jpg')

    return render_template_string("""

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Tag Scan Return UK</title>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

<style>

*{
    box-sizing:border-box;
}

body{
    margin:0;
    background:#050816;
    color:white;
    font-family:'Inter',sans-serif;
    overflow-x:hidden;
}

.hero{
    position:relative;
    padding:90px 20px 50px;
    text-align:center;
    background:
    radial-gradient(circle at top right,#d4af3720,transparent 30%),
    radial-gradient(circle at bottom left,#ffffff10,transparent 30%);
}

.logo{
    font-size:72px;
    font-weight:900;
    letter-spacing:-2px;
}

.logo span{
    color:#d4af37;
}

.subtitle{
    margin-top:14px;
    font-size:22px;
    color:#c8c8c8;
    line-height:1.6;
}

.container{
    max-width:1320px;
    margin:auto;
    padding:20px;
}

.grid{
    display:grid;
    grid-template-columns:460px 1fr;
    gap:28px;
    align-items:start;
}

.card{
    background:#0f172a;
    border-radius:28px;
    padding:34px;
    border:1px solid rgba(255,255,255,0.06);
    box-shadow:0 12px 40px rgba(0,0,0,0.45);
}

.activate-title{
    font-size:38px;
    font-weight:800;
    margin-top:0;
}

.activate-sub{
    color:#bdbdbd;
    line-height:1.7;
    margin-top:10px;
}

input{
    width:100%;
    padding:18px;
    border:none;
    border-radius:16px;
    background:#1e293b;
    color:white;
    font-size:17px;
    margin-top:20px;
    outline:none;
}

textarea{
    width:100%;
    padding:16px;
    margin-top:16px;
    border:none;
    border-radius:14px;
    background:#1e293b;
    color:white;
    height:130px;
    resize:none;
}

button{
    width:100%;
    margin-top:20px;
    padding:18px;
    border:none;
    border-radius:16px;
    background:#d4af37;
    color:black;
    font-size:20px;
    font-weight:800;
    cursor:pointer;
}

.error{
    background:#7f1d1d;
    padding:14px;
    border-radius:14px;
    margin-top:18px;
}

.feature-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:14px;
    margin-top:26px;
}

.feature{
    background:#111827;
    border-radius:18px;
    padding:18px;
}

.feature-title{
    color:#d4af37;
    font-weight:800;
    margin-bottom:6px;
}

.feature-text{
    color:#d0d0d0;
    line-height:1.5;
    font-size:14px;
}

.collage{
    overflow:hidden;
    border-radius:24px;
}

.collage img{
    width:100%;
    display:block;
}

.product-bar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-top:20px;
    flex-wrap:wrap;
    gap:20px;
}

.price{
    font-size:64px;
    font-weight:900;
}

.price-sub{
    color:#bdbdbd;
    margin-top:8px;
}

.buy-btn{
    width:auto;
    padding:18px 30px;
}

.bottom{
    max-width:1320px;
    margin:30px auto 60px;
    padding:0 20px;
}

.bottom-grid{
    display:grid;
    grid-template-columns:1fr 1fr 1fr;
    gap:20px;
}

.bottom-card{
    background:#0f172a;
    border-radius:24px;
    padding:28px;
}

.bottom-title{
    color:#d4af37;
    font-size:22px;
    font-weight:800;
    margin-bottom:10px;
}

.bottom-text{
    color:#c8c8c8;
    line-height:1.7;
}

.footer{
    text-align:center;
    color:#777;
    padding:30px 20px 50px;
    font-size:14px;
}

@media(max-width:1100px){

    .grid{
        grid-template-columns:1fr;
        justify-items:center;
    }

    .bottom-grid{
        grid-template-columns:1fr;
    }

    .logo{
        font-size:50px;
        text-align:center;
    }

    .subtitle{
        font-size:18px;
    }

    .price{
        font-size:52px;
    }

    .container{
        padding:14px;
    }

    .card{
        padding:24px;
        width:100%;
    }

    .product-bar{
        justify-content:center;
        text-align:center;
    }
}

</style>

</head>

<body>

<div class="hero">

<div class="logo">
Tag <span>SCAN</span> Return
</div>

<div class="subtitle">
Professional QR recovery stickers for pets, luggage,
keys, bikes and valuables across the UK.
</div>

</div>

<div class="container">

<div class="grid">

<div class="card">

<div class="activate-title">
Activate Sticker
</div>

<div class="activate-sub">
Enter your activation code below.
</div>

<form method="POST">

<input
name="code"
placeholder="Enter activation code"
required
>

<button>
Activate Sticker
</button>

</form>

{% if error %}
<div class="error">
{{ error }}
</div>
{% endif %}

<div class="feature-grid">

<div class="feature">
<div class="feature-title">Waterproof</div>
<div class="feature-text">
Built to survive rain and daily wear.
</div>
</div>

<div class="feature">
<div class="feature-title">Secure</div>
<div class="feature-text">
Private recovery details protected safely.
</div>
</div>

<div class="feature">
<div class="feature-title">Fast Recovery</div>
<div class="feature-text">
Instant owner contact when scanned.
</div>
</div>

<div class="feature">
<div class="feature-title">Premium Quality</div>
<div class="feature-text">
High resolution durable QR stickers.
</div>
</div>

</div>

</div>

<div>

<div class="collage">
<img src="{{ collage_url }}">
</div>

<div class="product-bar">

<div>

<div class="price">
£9.99
</div>

<div class="price-sub">
10 waterproof premium QR recovery stickers
</div>

</div>

</div>

</div>

</div>

</div>

<div class="bottom">

<div class="bottom-grid">

<div class="bottom-card">

<div class="bottom-title">
Protect Your Pets
</div>

<div class="bottom-text">
Attach QR recovery tags to pet collars for fast owner contact.
</div>

</div>

<div class="bottom-card">

<div class="bottom-title">
Secure Your Valuables
</div>

<div class="bottom-text">
Perfect for keys, bikes, laptops, luggage and phones.
</div>

</div>

<div class="bottom-card">

<div class="bottom-title">
Easy To Use
</div>

<div class="bottom-text">
Scan the QR code instantly to contact the owner through their secure recovery profile.
</div>

</div>

</div>

</div>

<div class="footer">
© Tag Scan Return UK • Secure QR Recovery System
</div>

</body>

</html>

    """, error=error, collage_url=collage_url)

# =========================================================
# CREATE PROFILE
# =========================================================

@app.route("/create/<code>", methods=["GET", "POST"])
def create(code):

    activation = Code.query.filter_by(code=code).first()

    if not activation:
        return "Invalid activation code"

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

        activation.used = True

        db.session.commit()

        profile_url = f"{DOMAIN}/profile/{code}"

        os.makedirs("static/qrcodes", exist_ok=True)

        qr_path = f"static/qrcodes/{code}.png"

        qr = qrcode.make(profile_url)

        qr.save(qr_path)

        return redirect(f"/profile/{code}")

    return '''

<html>
<body style="background:#050816;color:white;font-family:Inter,sans-serif;padding:30px;">

<div style="max-width:600px;margin:auto;background:#0f172a;padding:40px;border-radius:24px;">

<h1>Create Recovery Profile</h1>

<form method="POST">

<input name="name" placeholder="Full Name" required>
<input name="phone" placeholder="Phone Number" required>
<input name="phone2" placeholder="Backup Phone Number">
<input name="email" placeholder="Email Address">

<textarea
name="details"
placeholder="Pet or Item Details"
required
></textarea>

<button>
Generate QR Profile
</button>

</form>

</div>

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

    return f"""
    <html>
    <body style='background:#050816;color:white;font-family:Inter,sans-serif;padding:30px;'>

    <div style='max-width:700px;margin:auto;background:#0f172a;padding:40px;border-radius:24px;'>

    <h1>Item Located</h1>

    <p>Please contact the owner below.</p>

    <a href='tel:{profile.phone}' style='display:block;background:#d4af37;padding:18px;border-radius:14px;color:black;text-decoration:none;font-weight:800;'>
    Call Owner
    </a>

    <br>

    <strong>Owner:</strong><br>
    {profile.name}

    <br><br>

    <strong>Details:</strong><br>
    {profile.details}

    </div>

    </body>
    </html>
    """

# =========================================================
# ADMIN
# =========================================================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    auth = request.authorization

    if not auth or not (
        auth.username == ADMIN_USER and
        auth.password == ADMIN_PASS
    ):
        return Response(
            "Login Required",
            401,
            {
                "WWW-Authenticate":
                'Basic realm="Login Required"'
            }
        )

    if request.method == "POST":

        new_code = request.form.get("code", "").strip().upper()

        if new_code:

            existing = Code.query.filter_by(code=new_code).first()

            if not existing:

                db.session.add(
                    Code(
                        code=new_code,
                        used=False
                    )
                )

                db.session.commit()

    codes = Code.query.order_by(Code.id.desc()).all()

    return render_template_string("""

<html>

<body style="
background:#050816;
color:white;
font-family:Inter,sans-serif;
padding:40px;
">

<div style="
max-width:900px;
margin:auto;
background:#0f172a;
padding:40px;
border-radius:28px;
">

<h1>
Admin Dashboard
</h1>

<form method="POST">

<input
name="code"
placeholder="Create Activation Code"
required
style="
padding:16px;
width:320px;
border:none;
border-radius:14px;
background:#1e293b;
color:white;
"
>

<button style="
padding:16px 24px;
border:none;
border-radius:14px;
background:#d4af37;
font-weight:800;
margin-left:12px;
width:auto;
">
Add Code
</button>

</form>

<br><br>

<h2>
Existing Codes
</h2>

{% for code in codes %}

<div style="
background:#111827;
padding:16px;
border-radius:14px;
margin-top:12px;
">

<strong>{{ code.code }}</strong>

—
{% if code.used %}
USED
{% else %}
AVAILABLE
{% endif %}

</div>

{% endfor %}

</div>

</body>

</html>

    """, codes=codes)

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )