from flask import Flask, request, redirect, url_for, render_template_string, flash
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# EDIT THESE DETAILS FOR YOUR BUSINESS
BUSINESS_NAME = "FLEX CHAIR"
OWNER_NAME = "Shweta Kulkarni"
PHONE = "8149736651"
EMAIL = "shwetakulkarni685@gmail.com"
ADDRESS = "Your city, Maharashtra, India"

PRODUCTS = [
    {"name": "Executive Office Chair", "description": "Premium seating for offices and workspaces.", "price": "Ask for price", "image": "https://images.unsplash.com/photo-150360,0"},
    {"name": "Manager Chair", "description": "A stylish chair for managers and professionals.", "price": "Ask for price", "image": ""},
    {"name": "Study Chair", "description": "Practical seating for study spaces.", "price": "Ask for price", "image": ""},
    {"name": "Plastic Chair", "description": "Lightweight seating for everyday use.", "price": "Ask for price", "image": ""},
]

STYLE = """
:root { --gold:#c9a34a; --black:#101010; --panel:#191919; --white:#f7f5ef; }
* { box-sizing:border-box; }
body { margin:0; font-family:Arial, sans-serif; background:var(--black); color:var(--white); line-height:1.6; }
header { background:#080808; border-bottom:1px solid #6d5728; position:sticky; top:0; z-index:5; }
.nav { max-width:1100px; margin:auto; padding:18px 22px; display:flex; justify-content:space-between; align-items:center; gap:18px; flex-wrap:wrap; }
.logo { color:var(--gold); font-size:25px; font-weight:800; letter-spacing:2px; text-decoration:none; }
nav { display:flex; gap:16px; flex-wrap:wrap; }
nav a { color:#eee; text-decoration:none; font-size:14px; }
nav a:hover, nav a.active { color:var(--gold); }
.container { max-width:1100px; margin:auto; padding:42px 22px; }
.hero { min-height:440px; display:flex; align-items:center; background:linear-gradient(90deg,rgba(0,0,0,.92),rgba(0,0,0,.40)),url('https://images.unsplash.com/photo-1598300056393-4aac492f4344?auto=format&fit=crop&w=1600&q=85') center/cover; }
.hero-inner { max-width:1100px; width:100%; margin:auto; padding:65px 22px; }
h1,h2,h3 { line-height:1.2; }
h1 { font-size:clamp(38px,7vw,68px); margin:8px 0 16px; }
h2 { color:var(--gold); }
.gold { color:var(--gold); letter-spacing:2px; font-weight:bold; }
.muted { color:#c5c1b8; }
.btn { display:inline-block; background:var(--gold); color:#151515; padding:12px 20px; border:0; border-radius:4px; font-weight:bold; text-decoration:none; cursor:pointer; }
.btn:hover { background:#e1bd68; }
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:20px; }
.card { background:var(--panel); border:1px solid #3b3321; border-radius:9px; overflow:hidden; }
.card img { width:100%; height:190px; object-fit:cover; background:#282828; }
.card-content { padding:18px; }
section { margin-bottom:28px; }
form { max-width:650px; }
label { display:block; margin:14px 0 6px; color:var(--gold); }
input,select,textarea { width:100%; padding:12px; border-radius:4px; border:1px solid #625333; background:#202020; color:white; font:inherit; }
textarea { min-height:110px; }
.notice { padding:12px 15px; background:#263522; border:1px solid #597348; border-radius:5px; margin:15px 0; }
footer { border-top:1px solid #6d5728; padding:25px 22px; text-align:center; color:#bbb; }
@media(max-width:600px) { .nav { justify-content:center; } nav { justify-content:center; } .container { padding-top:28px; } }
"""

BASE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }} | FLEX CHAIR</title>
<style>{{ style }}</style>
</head>
<body>
<header><div class="nav">
<a class="logo" href="{{ url_for('home') }}">FLEX CHAIR</a>
<nav>
{% for endpoint, label in [('home','Home'),('about','About Us'),('products','Products'),('gallery','Gallery'),('orders','Orders'),('contact','Contact')] %}
<a href="{{ url_for(endpoint) }}" class="{{ 'active' if active == endpoint else '' }}">{{ label }}</a>
{% endfor %}
</nav></div></header>
{% with messages = get_flashed_messages() %}
{% if messages %}<div class="container">{% for message in messages %}<div class="notice">{{ message }}</div>{% endfor %}</div>{% endif %}
{% endwith %}
{{ content|safe }}
<footer><strong class="gold">FLEX CHAIR</strong><br>Comfort. Quality. Confidence.<br><small>© {{ year }} FLEX CHAIR. All rights reserved.</small></footer>
</body></html>
"""

def page(title, active, content, **context):
    inner = render_template_string(content, products=PRODUCTS, business_name=BUSINESS_NAME,
                                   phone=PHONE, email=EMAIL, address=ADDRESS, **context)
    return render_template_string(BASE, title=title, active=active, content=inner,
                                  style=STYLE, year=datetime.now().year)

@app.route("/")
def home():
    return page("Home", "home", """
    <div class="hero"><div class="hero-inner">
      <div class="gold">COMFORT • QUALITY • CONFIDENCE</div>
      <h1>COMFORT MEETS<br><span class="gold">QUALITY.</span></h1>
      <p class="muted">Discover modern, stylish and comfortable seating solutions for homes, offices and businesses.</p>
      <a class="btn" href="{{ url_for('products') }}">EXPLORE OUR PRODUCTS</a>
    </div></div>
    <main class="container">
      <section><h2>Welcome to FLEX CHAIR</h2>
      <p>We manufacture and sell seating solutions designed around comfort, quality and everyday performance. Explore our collection and contact us for product enquiries and bulk orders.</p></section>
      <section><h2>Why Choose Us?</h2><div class="grid">
        <div class="card card-content"><h3>Quality</h3><p class="muted">A focus on dependable materials and finish.</p></div>
        <div class="card card-content"><h3>Comfort</h3><p class="muted">Seating options for different spaces and needs.</p></div>
        <div class="card card-content"><h3>Customer Support</h3><p class="muted">Get help with product selection and enquiries.</p></div>
      </div></section>
    </main>
    """)

@app.route("/about")
def about():
    return page("About Us", "about", """
    <main class="container"><div class="gold">GET TO KNOW US</div><h1>About <span class="gold">FLEX CHAIR</span></h1>
    <p>Flex Chair is a chair manufacturing and selling business committed to providing quality seating solutions. We aim to combine modern designs, comfort and durability for homes, offices, schools and commercial spaces.</p>
    <div class="grid">
      <div class="card card-content"><h2>Our Mission</h2><p>To provide comfortable, durable and affordable seating solutions.</p></div>
      <div class="card card-content"><h2>Our Vision</h2><p>To become a trusted name in the chair manufacturing industry.</p></div>
      <div class="card card-content"><h2>Our Values</h2><p>Quality, customer satisfaction, innovation and reliability.</p></div>
    </div></main>
    """)

@app.route("/products")
def products():
    return page("Products", "products", """
    <main class="container"><div class="gold">OUR COLLECTION</div><h1>Our <span class="gold">Products</span></h1>
    <p class="muted">Browse our chair categories. Contact us for current prices, colours and availability.</p>
    <div class="grid">{% for product in products %}
      <article class="card">
        {% if product.image and product.image.startswith('http') and 'photo-150360,0' not in product.image %}
        <img src="{{ product.image }}" alt="{{ product.name }}">
        {% else %}<div style="height:190px;display:grid;place-items:center;color:#c9a34a;background:#25221b">FLEX CHAIR</div>{% endif %}
        <div class="card-content"><h3>{{ product.name }}</h3><p class="muted">{{ product.description }}</p><p class="gold">{{ product.price }}</p>
        <a class="btn" href="{{ url_for('orders', product=product.name) }}">Enquire now</a></div>
      </article>{% endfor %}
    </div></main>
    """)

@app.route("/gallery")
def gallery():
    return page("Gallery", "gallery", """
    <main class="container"><div class="gold">OUR WORK</div><h1>Product <span class="gold">Gallery</span></h1>
    <p class="muted">Add your own product, factory, showroom and packaging photographs here.</p>
    <div class="grid">
      <div class="card card-content"><h3>Our Products</h3><p class="muted">Showcase your latest chair models.</p></div>
      <div class="card card-content"><h3>Manufacturing</h3><p class="muted">Share photographs of your production process.</p></div>
      <div class="card card-content"><h3>Showroom & Delivery</h3><p class="muted">Show customers your showroom and finished orders.</p></div>
    </div></main>
    """)

@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        product = request.form.get("product", "").strip()
        quantity = request.form.get("quantity", "").strip()
        address = request.form.get("address", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not mobile or not product or not quantity:
            flash("Please fill in your name, mobile number, product and quantity.")
            return redirect(url_for("orders"))
        file_exists = os.path.isfile("orders.csv")
        with open("orders.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Name", "Mobile", "Product", "Quantity", "Address", "Message"])
            writer.writerow([datetime.now().isoformat(timespec="minutes"), name, mobile, product, quantity, address, message])
        flash("Thank you! Your enquiry has been saved. We will contact you soon.")
        return redirect(url_for("orders"))
    selected = request.args.get("product", "")
    return page("Orders", "orders", """
    <main class="container"><div class="gold">LET'S GET STARTED</div><h1>Place an <span class="gold">Enquiry</span></h1>
    <p class="muted">Fill out this form and our team can contact you about your chair order.</p>
    <form method="post">
      <label>Your name *</label><input name="name" required placeholder="Enter your full name">
      <label>Mobile number *</label><input name="mobile" required type="tel" placeholder="Enter your mobile number">
      <label>Select product *</label><select name="product" required>
        <option value="">Choose a chair</option>
        {% for p in products %}<option value="{{ p.name }}" {% if selected == p.name %}selected{% endif %}>{{ p.name }}</option>{% endfor %}
      </select>
      <label>Quantity *</label><input name="quantity" type="number" min="1" required placeholder="e.g. 2">
      <label>Delivery address</label><textarea name="address" placeholder="Enter your delivery address"></textarea>
      <label>Additional requirements</label><textarea name="message" placeholder="Colour, bulk order or other details"></textarea>
      <p><button class="btn" type="submit">SUBMIT ENQUIRY</button></p>
      <small class="muted">* Required fields. This form saves enquiries to orders.csv on the website computer/server.</small>
    </form></main>
    """, selected=selected)

@app.route("/contact")
def contact():
    return page("Contact", "contact", """
    <main class="container"><div class="gold">WE ARE HERE TO HELP</div><h1>Contact <span class="gold">Us</span></h1>
    <p>Contact Flex Chair for product details, current prices, bulk orders and business enquiries.</p>
    <div class="card card-content">
      <p><strong class="gold">Business:</strong> {{ business_name }}</p>
      <p><strong class="gold">Company Owner:</strong> Shweta Kulkarni</p>
      <p><strong class="gold">Phone:</strong> {{ phone }}</p>
      <p><strong class="gold">Email:</strong> {{ email }}</p>
      <p><strong class="gold">Address:</strong> {{ address }}</p>
      <a class="btn" href="{{ url_for('orders') }}">SEND AN ENQUIRY</a>
    </div></main>
    """)
@app.route("/practicals")
def practicals():
    return page("Practical Work", "practicals", """
    <main class="container">
      <div class="gold">FLEX CHAIR INDIA</div>
      <h1>Business <span class="gold">Practicals</span></h1>

      <section class="card card-content">
        <h2>1. Sustainability Audit of a Startup</h2>
        <p>This practical evaluates the environmental, social and economic sustainability of Flex Chair India.</p>
        <ul>
          <li>Use raw materials efficiently and reduce manufacturing waste.</li>
          <li>Explore recyclable and eco-friendly materials.</li>
          <li>Maintain safe and fair working conditions.</li>
          <li>Control production costs while maintaining product quality.</li>
        </ul>
        <p><strong>Outcome:</strong> A responsible and sustainable chair manufacturing business.</p>
      </section>

      <section class="card card-content">
        <h2>2. Scalable Business Model Redesign</h2>
        <p>The business model can be improved to increase production and sales.</p>
        <ul>
          <li>Develop online sales through the company website.</li>
          <li>Use digital tools to manage orders and customer enquiries.</li>
          <li>Build partnerships with furniture dealers and offices.</li>
          <li>Increase production gradually according to demand.</li>
        </ul>
        <p><strong>Outcome:</strong> A business model that can grow without losing quality.</p>
      </section>

      <section class="card card-content">
        <h2>3. Supply Chain and Operations Scaling Plan</h2>
        <p>A reliable supply chain helps the company manufacture and deliver chairs on time.</p>
        <ul>
          <li>Identify dependable raw material suppliers.</li>
          <li>Compare material prices and quality before purchasing.</li>
          <li>Maintain stock records of raw materials and finished chairs.</li>
          <li>Plan production according to customer orders.</li>
          <li>Monitor packaging, transport and delivery costs.</li>
        </ul>
        <p><strong>Outcome:</strong> Better inventory control and timely customer delivery.</p>
      </section>

      <section class="card card-content">
        <h2>4. Financial Projections for Scaling</h2>
        <p>The following figures are illustrative sample estimates for an academic project, not actual company financial records.</p>
        <table>
          <tr><th>Particulars</th><th>Sample Amount</th></tr>
          <tr><td>Initial investment</td><td>₹2,00,000</td></tr>
          <tr><td>Cost per chair</td><td>₹2,000</td></tr>
          <tr><td>Selling price per chair</td><td>₹3,000</td></tr>
          <tr><td>Monthly sales (50 chairs)</td><td>₹1,50,000</td></tr>
          <tr><td>Monthly production cost</td><td>₹1,00,000</td></tr>
          <tr><td>Gross contribution</td><td>₹50,000</td></tr>
        </table>
        <p><strong>Break-even:</strong> The business must sell enough chairs to recover its fixed costs and initial investment. Actual break-even depends on fixed expenses and other operating costs.</p>
        <p><strong>Outcome:</strong> Financial planning can help estimate investment needs, costs, revenue and future growth.</p>
      </section>
    </main>
    """)

if __name__ == "__main__":
    app.run(debug=True)
