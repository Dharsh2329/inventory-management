from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL)

# Create table automatically
with get_db() as db:
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT,
            quantity INTEGER,
            price NUMERIC
        )
    """)
    db.commit()

@app.route("/", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        with get_db() as db:
            cur = db.cursor()
            cur.execute(
                "INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)",
                (name, quantity, price)
            )
            db.commit()

        return redirect("/products")

    return render_template("index.html")

@app.route("/products")
def products():
    with get_db() as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM products")
        data = cur.fetchall()
    return render_template("products.html", products=data)

@app.route("/delete/<int:id>")
def delete(id):
    with get_db() as db:
        cur = db.cursor()
        cur.execute("DELETE FROM products WHERE id=%s", (id,))
        db.commit()
    return redirect("/products")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
