from flask import Flask, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "tags.db"

# =========================
# DATABASE SETUP
# =========================

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        owner_name TEXT,
        email TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# MAIN WEBSITE
# =========================

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        code = request.form.get("code")

        if code:
            return redirect(f"/tag/{code}")

    return """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Tag & Trace | QR Recovery Stickers UK</title>

<meta name="description" content="Waterproof QR recovery stickers for pets, bikes, keys and valuables.">

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
scroll-behavior:smooth;
}

body{
font-family:'Inter',sans-serif;
background:#050816;
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
background:rgba(5,8,22,0.92);
backdrop-filter:blur(10px);
border-bottom:1px solid rgba(255,255,255,0.08);
}

.nav{
display:flex;
justify-content:space-between;
align-items:center;
padding:22px 0;
}

.logo{
font-size:34px;
font-weight:800;
color:#facc15;
}

.nav-links{
display:flex;
gap:28px;
}

.nav-links a{
color:white;
text-decoration:none;
font-weight:600;
}

.hero{
padding:90px 0;
display:grid;
grid-template-columns:1fr 1fr;
gap:60px;
align-items:center;
}

.hero h1{
font-size:72px;
line-height:1.05;
font-weight:800;
margin-bottom:24px;
}

.highlight{
color:#facc15;
}

.hero p{
font-size:20px;
color:#cbd5e1;
line-height:1.6;
margin-bottom:30px;
}

.btn-row{
display:flex;
gap:16px;
flex-wrap:wrap;
}

.btn{
padding:16px 32px;
border-radius:14px;
font-weight:700;
text-decoration:none;
display:inline-block;
transition:0.3s;
cursor:pointer;
border:none;
}

.btn-primary{
background:#facc15;
color:black;
}

.btn-primary:hover{
transform:translateY(-2px);
}

.btn-secondary{
border:1px solid rgba(255,255,255,0.15);
color:white;
}

.hero-card{
background:linear-gradient(180deg,#111827,#1e293b);
padding:24px;
border-radius:28px;
box-shadow:0 20px 60px rgba(0,0,0,0.45);
}

.hero-card img{
width:100%;
border-radius:18px;
display:block;
}

.section{
padding:100px 0;
}

.section-title{
text-align:center;
font-size:48px;
font-weight:800;
margin-bottom:20px;
}

.section-sub{
text-align:center;
color:#cbd5e1;
max-width:800px;
margin:auto auto 60px;
font-size:18px;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
gap:24px;
}

.card{
background:#111827;
padding:30px;
border-radius:24px;
border:1px solid rgba(255,255,255,0.06);
}

.card img{
width:100%;
height:220px;
object-fit:cover;
border-radius:16px;
margin-bottom:18px;
}

.card h3{
margin-bottom:10px;
font-size:24px;
}

.price{
font-size:32px;
font-weight:800;
color:#facc15;
margin:16px 0;
}

.steps{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
gap:24px;
}

.step{
background:#111827;
padding:30px;
border-radius:22px;
position:relative;
}

.step-number{
position:absolute;
top:-14px;
left:20px;
background:#facc15;
color:black;
padding:8px 14px;
border-radius:999px;
font-weight:800;
}

.activate-box{
background:#111827;
padding:35px;
border-radius:28px;
max-width:700px;
margin:auto;
}

.activate-box input{
width:100%;
padding:18px;
border:none;
border-radius:14px;
background:#1e293b;
color:white;
font-size:16px;
margin:20px 0;
}

footer{
background:black;
padding:70px 0;
margin-top:60px;
}

.footer-grid{
display:grid;
grid-template-columns:2fr 1fr 1fr;
gap:40px;
}

.small{
margin-top:30px;
color:#94a3b8;
font-size:14px;
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
<a href="#products">Products</a>
<a href="#how">How It Works</a>
<a href="#activate">Activate</a>
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
Secure recovery technology with instant QR scanning.
</p>

<div class="btn-row">

<a href="#products" class="btn btn-primary">
View Products
</a>

<a href="#how" class="btn btn-secondary">
How It Works
</a>

</div>

</div>

<div class="hero-card">

<img src="https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=1200&auto=format&fit=crop">

</div>

</section>

<section class="section" id="products">

<div class="container">

<h2 class="section-title">
Our Recovery Sticker Packs
</h2>

<p class="section-sub">
Perfect for pets, keys, electronics, luggage, bikes and personal valuables.
</p>

<div class="grid">

<div class="card">

<img src="https://images.unsplash.com/photo-1517849845537-4d257902454a?q=80&w=1200&auto=format&fit=crop">

<h3>Pet Recovery Tags</h3>

<p>
Waterproof QR stickers for collars and pet accessories.
</p>

<div class="price">
£9.99
</div>

</div>

<div class="card">

<img src="https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?q=80&w=1200&auto=format&fit=crop">

<h3>Key & Wallet Tags</h3>

<p>
Fast scan recovery for everyday valuables.
</p>

<div class="price">
£9.99
</div>

</div>

<div class="card">

<img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=1200&auto=format&fit=crop">

<h3>Tech & Electronics</h3>

<p>
Protect headphones, laptops, tablets and devices.
</p>

<div class="price">
£9.99
</div>

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
<p>Order your waterproof QR sticker pack.</p>
</div>

<div class="step">
<div class="step-number">02</div>
<h3>Activate</h3>
<p>Enter your activation code online.</p>
</div>

<div class="step">
<div class="step-number">03</div>
<h3>Apply Sticker</h3>
<p>Stick it to valuables, pets or equipment.</p>
</div>

<div class="step">
<div class="step-number">04</div>
<h3>Get It Returned</h3>
<p>If found, the QR code helps reconnect it to you.</p>
</div>

</div>

</div>

</section>

<section class="section" id="activate">

<div class="container">

<h2 class="section-title">
Activate Your Sticker
</h2>

<div class="activate-box">

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

</section>

<footer id="contact">

<div class="container footer-grid">

<div>

<h2 class="logo">
Tag & Trace
</h2>

<p class="small">
Professional QR recovery stickers for modern protection.
</p>

</div>

<div>

<h3>Quick Links</h3>

<br>

<p>Products</p>
<p>How It Works</p>
<p>Activate</p>

</div>

<div>

<h3>Contact</h3>

<br>

<p>support@tagandtrace.co.uk</p>
<p>www.tagandtrace.co.uk</p>

</div>

</div>

<div class="container small">
© 2026 Tag & Trace UK
</div>

</footer>

</body>

</html>

"""

# =========================
# TAG PAGE
# =========================

@app.route("/tag/<code>")
def tag(code):

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT owner_name,email,phone FROM tags WHERE code=?", (code,))
    row = c.fetchone()

    conn.close()

    if row:

        owner, email, phone = row

        return f"""

        <html>
        <body style='font-family:Arial;background:#111827;color:white;padding:40px;'>

        <h1>Item Found</h1>

        <p>This item belongs to:</p>

        <h2>{owner}</h2>

        <p>Email: {email}</p>
        <p>Phone: {phone}</p>

        </body>
        </html>

        """

    return """

    <html>
    <body style='font-family:Arial;background:#111827;color:white;padding:40px;'>

    <h1>Tag Not Activated</h1>

    <p>This QR code has not been activated yet.</p>

    </body>
    </html>

    """

# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)