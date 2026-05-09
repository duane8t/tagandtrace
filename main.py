from flask import Flask, request, redirect, url_for, Response, render_template_string
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "changeme123")

DOMAIN = "https://www.tagscanreturn.co.uk"

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
    details = db.Column(db.String(500))

with app.app_context():
    db.create_all()

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
            code.used = True
            db.session.commit()
            return redirect(f"/create/{user_code}")
        else:
            error = "Invalid or already used activation code"

    collage_url = url_for("static", filename="collage2.jpg")

    return render_template_string("""

<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Tag Scan Return</title>

<style>

body{
    margin:0;
    background:#050816;
    color:white;
    font-family:Arial,sans-serif;
}

.wrapper{
    max-width:1300px;
    margin:auto;
    padding:30px 20px;
}

.hero{
    text-align:center;
    margin-bottom:30px;
}

.hero h1{
    font-size:64px;
    margin-bottom:10px;
}

.hero span{
    color:#d4af37;
}

.hero p{
    color:#cbd5e1;
    font-size:20px;
}

.grid{
    display:grid;
    grid-template-columns:420px 1fr;
    gap:24px;
}

.card{
    background:#0f172a;
    border-radius:28px;
    padding:30px;
    box-shadow:0 12px 40px rgba(0,0,0,0.45);
}

input, textarea{
    width:100%;
    box-sizing:border-box;
    padding:16px;
    margin-top:16px;
    border:none;
    border-radius:14px;
    background:#1e293b;
    color:white;
    font-size:16px;
}

button{
    width:100%;
    padding:16px;
    margin-top:18px;
    border:none;
    border-radius:14px;
    background:#d4af37;
    color:black;
    font-size:20px;
    font-weight:800;
    cursor:pointer;
}

.error{
    margin-top:16px;
    background:#7f1d1d;
    padding:14px;
    border-radius:14px;
}

.product img{
    width:100%;
    border-radius:20px;
}

.feature-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:14px;
    margin-top:20px;
}

.feature{
    background:#111827;
    border-radius:16px;
    padding:16px;
}

.feature h3{
    color:#d4af37;
    margin-top:0;
}

.admin-btn{
    position:fixed;
    top:20px;
    right:20px;
    background:#111827;
    color:white;
    text-decoration:none;
    padding:12px 18px;
    border-radius:14px;
}

@media(max-width:900px){

    .grid{
        grid-template-columns:1fr;
    }

    .hero h1{
        font-size:46px;
    }

}

</style>

</head>

<body>

<a href="/admin" class="admin-btn">Admin</a>

<div class="wrapper">

<div class="hero">
<h1>Tag <span>SCAN</span> Return</h1>
<p>Stick it. Scan it. Get it back.</p>
</div>

<div class="grid">

<div class="card">

<h2>Activate Sticker</h2>

<p>Enter your activation code to create your recovery profile.</p>

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
<h3>Fast Recovery</h3>
<p>Instant contact when scanned.</p>
</div>

<div class="feature">
<h3>Waterproof</h3>
<p>Durable weather resistant stickers.</p>
</div>

<div class="feature">
<h3>Secure</h3>
<p>Your contact details stay protected.</p>
</div>

<div class="feature">
<h3>Premium Quality</h3>
<p>High resolution QR labels.</p>
</div>

</div>

</div>

<div class="card product">

<img src="{{ collage_url }}">

<h2>10 Sticker Pack</h2>

<h1 style="color:#d4af37;">£9.99</h1>

<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_blank">

<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="duane@sisco.co.uk">
<input type="hidden" name="item_name" value="Tag Scan Return Sticker Pack">
<input type="hidden" name="amount" value="9.99">
<input type="hidden" name="currency_code" value="GBP">

<button type="submit">
Buy Sticker Pack
</button>

</form>

</div>

</div>

</div>

</body>

</html>

    """, error=error, collage_url=collage_url)

@app.route("/create/<code>", methods=["GET", "POST"])
def create(code):

    if request.method == "POST":

        profile = Profile(
            code=code,
            name=request.form.get("name"),
            phone=request.form.get("phone"),
            phone2=request.form.get("phone2"),
            details=request.form.get("details")
        )

        db.session.add(profile)
        db.session.commit()

        profile_url = f"{DOMAIN}/profile/{code}"

        os.makedirs("static/qrcodes", exist_ok=True)

        qr_path = f"static/qrcodes/{code}.png"

        qr = qrcode.make(profile_url)

        qr.save(qr_path)

        return f"""
<html>
<body style="background:#050816;color:white;font-family:Arial;text-align:center;padding-top:80px;">
<h1>QR Code Ready</h1>
<div style="background:white;padding:20px;border-radius:24px;display:inline-block;">
<img src="/{qr_path}" width="240">
</div>
<br><br>
<a href="/{qr_path}" download style="background:#d4af37;color:black;padding:16px 24px;border-radius:14px;text-decoration:none;font-weight:bold;">
Download QR Code
</a>
</body>
</html>
"""

    return """
<html>
<body style="background:#050816;font-family:Arial;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px;">
<form method="POST" style="background:#0f172a;padding:40px;border-radius:28px;max-width:480px;width:100%;">
<h1 style="color:white;">Create Recovery Profile</h1>

<input name="name" placeholder="First Name" required>
<input name="phone" placeholder="Primary Phone Number" required>
<input name="phone2" placeholder="Secondary Phone Number">

<textarea
name="details"
placeholder="Pet or Item Details"
required
style="height:140px;resize:none;"
></textarea>

<button>
Generate QR
</button>

</form>
</body>
</html>
"""

@app.route("/profile/<code>")
def profile(code):

    profile = Profile.query.filter_by(code=code).first()

    if not profile:
        return "Profile not found"

    phone2_html = ""

    if profile.phone2:
        phone2_html = f"""
<a
href="tel:{profile.phone2}"
class="btn"
>
Backup Contact
</a>
"""

    return f"""
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

<div class="details">

<strong>Owner:</strong><br>
{profile.name.split()[0]}

<br><br>

<strong>Item / Pet Details:</strong><br>
{profile.details}

</div>

</div>

</body>

</html>
"""

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

    codes_html = ""

    for code in codes:

        status = "USED" if code.used else "AVAILABLE"

        codes_html += f"<div style='padding:12px;background:#111827;border-radius:12px;margin-top:12px;'>{code.code} — {status}</div>"

    return f"""
<html>

<body style="
background:#050816;
color:white;
font-family:Arial;
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

<h2 style="margin-top:40px;">
Existing Codes
</h2>

{codes_html}

</div>

</body>

</html>
"""

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
