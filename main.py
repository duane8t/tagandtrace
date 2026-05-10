from flask import Flask, request, redirect, Response, render_template
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ADMIN_USER = "admin"
ADMIN_PASS = "changeme123"


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

    return render_template(
        "index.html",
        error=error
    )


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

        os.makedirs("static/qrcodes", exist_ok=True)

        qr_path = f"static/qrcodes/{code}.png"

        qr = qrcode.make(
            f"https://www.tagscanreturn.co.uk/profile/{code}"
        )

        qr.save(qr_path)

        return f"""
<html>
<body style="background:#050816;color:white;font-family:Arial;display:flex;justify-content:center;align-items:center;min-height:100vh;">
<div style="background:#0f172a;padding:40px;border-radius:28px;text-align:center;">
<h1>QR Code Ready</h1>
<p>Your QR code is now active and your stickers are in the post.</p>
<div style="background:white;padding:20px;border-radius:24px;display:inline-block;">
<img src="/{qr_path}" width="240">
</div>
<a href="/{qr_path}" download style="display:block;margin-top:24px;background:#d4af37;color:black;padding:18px;border-radius:16px;text-decoration:none;font-weight:800;">
Download QR Code
</a>
</div>
</body>
</html>
"""

    return """
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body {
    margin:0;
    background:#050816;
    font-family:Arial;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
    padding:20px;
}

.form-card {
    background:#0f172a;
    padding:40px;
    border-radius:28px;
    max-width:520px;
    width:100%;
}

input, textarea {
    width:100%;
    box-sizing:border-box;
    padding:16px;
    margin-top:16px;
    border:none;
    border-radius:14px;
    background:#1e293b;
    color:white;
}

textarea {
    height:140px;
    resize:none;
}

button {
    width:100%;
    padding:16px;
    margin-top:20px;
    border:none;
    border-radius:14px;
    background:#d4af37;
    color:black;
    font-size:20px;
    font-weight:800;
}

</style>
</head>

<body>

<form method="POST" class="form-card">

<h1 style="color:white;">Create Recovery Profile</h1>

<input name="name" placeholder="First Name" required>

<input name="phone" placeholder="Primary Phone Number" required>

<input name="phone2" placeholder="Secondary Phone Number">

<textarea
name="details"
placeholder="Pet or Item Details"
required
></textarea>

<button>
Generate QR Code
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

    backup = ""

    if profile.phone2:
        backup = f'<a href="tel:{profile.phone2}" class="btn">Backup Contact</a>'

    return f"""
<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body {{
    margin:0;
    background:#050816;
    color:white;
    font-family:Arial;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
    padding:20px;
}}

.card {{
    width:100%;
    max-width:520px;
    background:#0f172a;
    border-radius:28px;
    padding:38px;
    text-align:center;
}}

.btn {{
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
}}

.details {{
    margin-top:28px;
    background:#111827;
    padding:24px;
    border-radius:20px;
    text-align:left;
}}

</style>

</head>

<body>

<div class="card">

<h1>Item Located</h1>

<p>Please contact the owner below.</p>

<a href="tel:{profile.phone}" class="btn">
Call Owner
</a>

{backup}

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

        new_code = request.form.get("code", "").strip().upper()

        if new_code:

            existing = Code.query.filter_by(code=new_code).first()

            if not existing:

                db.session.add(Code(code=new_code, used=False))
                db.session.commit()

    codes = Code.query.order_by(Code.id.desc()).all()

    code_html = ""

    for c in codes:
        status = "USED" if c.used else "AVAILABLE"
        code_html += f"<div style='padding:12px;background:#111827;border-radius:12px;margin-top:12px;'>{c.code} - {status}</div>"

    return f"""
<html>

<body style="background:#050816;color:white;font-family:Arial;padding:40px;">

<div style="max-width:900px;margin:auto;background:#0f172a;padding:40px;border-radius:28px;">

<h1>Admin Dashboard</h1>

<form method="POST">

<input
name="code"
placeholder="Create Activation Code"
required
style="padding:16px;width:320px;border:none;border-radius:14px;background:#1e293b;color:white;"
>

<button style="padding:16px 24px;border:none;border-radius:14px;background:#d4af37;font-weight:800;margin-left:12px;width:auto;">
Add Code
</button>

</form>

<h2 style="margin-top:40px;">
Existing Codes
</h2>

{code_html}

</div>

</body>

</html>
"""


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
