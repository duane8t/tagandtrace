from flask import Flask, request, redirect, url_for, Response, render_template_string
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os
from werkzeug.security import generate_password_hash, check_password_hash

# =========================================================
# APP
# =========================================================

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================================================
# DATABASE MODELS
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
ADMIN_PASS = os.environ.get("ADMIN_PASS", "tagscan123")

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

    collage_url = url_for('static', filename='collage.jpg')

    return render_template_string("""

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>TagScanReturn UK</title>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>

*{
    box-sizing:border-box;
}

body{
    margin:0;
    font-family:'Inter',sans-serif;
    background:#050816;
    color:white;
    overflow-x:hidden;
}

.hero{
    width:100%;
    padding:60px 20px 40px;
    text-align:center;
    background:
    radial-gradient(circle at top right,#d4af3730,transparent 30%),
    radial-gradient(circle at bottom left,#ffffff10,transparent 30%);
}

.logo{
    font-size:46px;
    font-weight:800;
    margin-bottom:10px;
}

.tag{
    color:#d4af37;
}

.subtitle{
    color:#cfcfcf;
    font-size:18px;
    max-width:700px;
    margin:auto;
    line-height:1.6;
}

.container{
    max-width:1200px;
    margin:auto;
    padding:20px;
}

.grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:28px;
}

.card{
    background:#0f172a;
    border:1px solid rgba(255,255,255,0.06);
    border-radius:24px;
    padding:28px;
    box-shadow:0 10px 30px rgba(0,0,0,0.35);
}

.card h2{
    margin-top:0;
    font-size:32px;
}

.card p{
    color:#c9c9c9;
    line-height:1.7;
}

input{
    width:100%;
    padding:16px;
    border:none;
    border-radius:14px;
    background:#1e293b;
    color:white;
    margin-top:14px;
    font-size:16px;
}

button{
    width:100%;
    margin-top:18px;
    border:none;
    border-radius:14px;
    padding:16px;
    background:#d4af37;
    color:black;
    font-size:18px;
    font-weight:800;
    cursor:pointer;
    transition:0.2s;
}

button:hover{
    transform:translateY(-2px);
}

.error{
    background:#7f1d1d;
    color:white;
    padding:12px;
    border-radius:12px;
    margin-top:16px;
}

.features{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:16px;
    margin-top:22px;
}

.feature{
    background:#111827;
    border-radius:16px;
    padding:18px;
}

.feature h3{
    margin-top:0;
    color:#d4af37;
}

.mockup img{
    width:100%;
    border-radius:20px;
}

.price{
    font-size:44px;
    font-weight:800;
    margin-top:12px;
}

.buy{
    display:inline-block;
    margin-top:20px;
    width:100%;
}

.buy button{
    width:100%;
}

.footer{
    text-align:center;
    color:#8f8f8f;
    padding:40px 20px;
    font-size:14px;
}

@media(max-width:900px){

    .grid{
        grid-template-columns:1fr;
    }

    .logo{
        font-size:34px;
    }
}

</style>

</head>

<body>

<div class="hero">

<div class="logo">
<span class="tag">Tag</span>ScanReturn
</div>

<div class="subtitle">
Professional QR recovery stickers for pets, luggage,
keys, bikes and valuables across the UK.
</div>

</div>

<div class="container">

<div class="grid">

<div class="card">

<h2>Activate Your Sticker</h2>

<p>
Enter the activation code from your sticker pack.
</p>

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

<div class="features">

<div class="feature">
<h3>Secure</h3>
<div>Private owner data protected securely.</div>
</div>

<div class="feature">
<h3>Waterproof</h3>
<div>Built for real-world outdoor use.</div>
</div>

<div class="feature">
<h3>Fast Recovery</h3>
<div>Instant owner contact when scanned.</div>
</div>

<div class="feature">
<h3>UK Based</h3>
<div>Designed for UK pet & item recovery.</div>
</div>

</div>

</div>

<div class="card">

<div class="mockup">
<img src="{{ collage_url }}">
</div>

<div class="price">
£9.99
</div>

<p>
10 premium waterproof QR recovery stickers.
Perfect for pets, keys, luggage, bikes and valuables.
</p>

<form
action="https://www.paypal.com/cgi-bin/webscr"
method="post"
target="_blank"
class="buy"
>

<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="duane@sisco.co.uk">
<input type="hidden" name="item_name" value="TagScanReturn Sticker Pack">
<input type="hidden" name="amount" value="9.99">
<input type="hidden" name="currency_code" value="GBP">

<button type="submit">
Buy Sticker Pack
</button>

</form>

</div>

</div>

</div>

<div class="footer">
© TagScanReturn UK
</div>

</body>
</html>

    """, error=error, collage_url=collage_url)

# =========================================================
# CREATE PROFILE
# =========================================================

@app.route("/create/<code>", methods=["GET", "POST"])
def create(code):

    activation = Code.query.filter_by(
        code=code
    ).first()

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

        return render_template_string("""

        <html>

        <head>

        <style>

        body{
            background:#050816;
            color:white;
            font-family:Inter,sans-serif;
            text-align:center;
            padding:50px;
        }

        .box{
            max-width:700px;
            margin:auto;
            background:#0f172a;
            padding:40px;
            border-radius:24px;
        }

        img{
            width:300px;
            margin-top:20px;
            border-radius:20px;
            background:white;
            padding:10px;
        }

        a{
            display:inline-block;
            margin-top:30px;
            background:#d4af37;
            color:black;
            padding:16px 26px;
            border-radius:14px;
            text-decoration:none;
            font-weight:800;
        }

        </style>

        </head>

        <body>

        <div class="box">

        <h1>
        Sticker Activated Successfully
        </h1>

        <p>
        Your QR recovery profile is now live.
        </p>

        <img src="/{{ qr_path }}">

        <br>

        <a href="/{{ qr_path }}" download>
        Download QR Code
        </a>

        </div>

        </body>

        </html>

        """, qr_path=qr_path)

    return render_template_string("""

    <html>

    <head>

    <style>

    body{
        background:#050816;
        color:white;
        font-family:Inter,sans-serif;
        display:flex;
        justify-content:center;
        align-items:center;
        min-height:100vh;
        padding:20px;
    }

    .form{
        width:100%;
        max-width:520px;
        background:#0f172a;
        border-radius:24px;
        padding:36px;
    }

    h1{
        margin-top:0;
    }

    input, textarea{
        width:100%;
        padding:16px;
        border:none;
        border-radius:14px;
        background:#1e293b;
        color:white;
        margin-top:14px;
        font-size:15px;
    }

    textarea{
        min-height:120px;
        resize:vertical;
    }

    button{
        width:100%;
        margin-top:18px;
        padding:16px;
        border:none;
        border-radius:14px;
        background:#d4af37;
        font-size:18px;
        font-weight:800;
        cursor:pointer;
    }

    </style>

    </head>

    <body>

    <form method="POST" class="form">

    <h1>Create Recovery Profile</h1>

    <input name="name" placeholder="Full Name" required>

    <input name="phone" placeholder="Primary Phone Number" required>

    <input name="phone2" placeholder="Secondary Phone Number">

    <input name="email" placeholder="Email Address">

    <textarea
    name="details"
    placeholder="Describe your pet or item"
    required
    ></textarea>

    <button>
    Generate QR Profile
    </button>

    </form>

    </body>

    </html>

    """)

# =========================================================
# PROFILE PAGE
# =========================================================

@app.route("/profile/<code>")
def profile(code):

    profile = Profile.query.filter_by(code=code).first()

    if not profile:
        return "Profile not found"

    return render_template_string("""

    <html>

    <head>

    <style>

    body{
        background:#050816;
        color:white;
        font-family:Inter,sans-serif;
        margin:0;
        padding:40px 20px;
    }

    .box{
        max-width:700px;
        margin:auto;
        background:#0f172a;
        border-radius:24px;
        padding:40px;
        text-align:center;
    }

    h1{
        font-size:42px;
        margin-top:0;
    }

    .ref{
        margin-top:20px;
        color:#d4af37;
        font-weight:700;
    }

    .details{
        margin-top:30px;
        background:#111827;
        padding:24px;
        border-radius:18px;
        text-align:left;
        line-height:1.8;
    }

    a.button{
        display:block;
        margin-top:20px;
        padding:18px;
        border-radius:16px;
        text-decoration:none;
        font-weight:800;
        background:#d4af37;
        color:black;
    }

    </style>

    </head>

    <body>

    <div class="box">

    <h1>
    Item Located
    </h1>

    <p>
    This item has been registered with TagScanReturn.
    Please contact the owner using the details below.
    </p>

    <a class="button" href="tel:{{ profile.phone }}">
    Call Owner
    </a>

    {% if profile.phone2 %}
    <a class="button" href="tel:{{ profile.phone2 }}">
    Backup Contact
    </a>
    {% endif %}

    {% if profile.email %}
    <a class="button" href="mailto:{{ profile.email }}">
    Email Owner
    </a>
    {% endif %}

    <div class="details">

    <strong>Owner:</strong><br>
    {{ profile.name }}

    <br><br>

    <strong>Item / Pet Details:</strong><br>
    {{ profile.details }}

    </div>

    <div class="ref">
    Reference: {{ profile.code }}
    </div>

    </div>

    </body>

    </html>

    """, profile=profile)

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
            {"WWW-Authenticate": 'Basic realm="Login Required"'}
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

    <head>

    <style>

    body{
        background:#050816;
        color:white;
        font-family:Inter,sans-serif;
        padding:40px;
    }

    .panel{
        max-width:900px;
        margin:auto;
        background:#0f172a;
        border-radius:24px;
        padding:40px;
    }

    input{
        width:300px;
        padding:14px;
        border:none;
        border-radius:12px;
        background:#1e293b;
        color:white;
    }

    button{
        padding:14px 20px;
        border:none;
        border-radius:12px;
        background:#d4af37;
        font-weight:800;
        margin-left:10px;
    }

    .code{
        background:#111827;
        padding:14px;
        border-radius:14px;
        margin-top:10px;
    }

    </style>

    </head>

    <body>

    <div class="panel">

    <h1>
    Admin Dashboard
    </h1>

    <form method="POST">

    <input
    name="code"
    placeholder="Create activation code"
    required
    >

    <button>
    Add Code
    </button>

    </form>

    <br><br>

    <h2>
    Existing Codes
    </h2>

    {% for code in codes %}

    <div class="code">

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