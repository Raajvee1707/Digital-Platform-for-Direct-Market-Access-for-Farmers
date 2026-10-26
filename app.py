
from flask import Flask, jsonify, render_template, request
import oracledb

app = Flask(__name__)

def get_connection():
    return oracledb.connect(
        user="USERNAME",
        password="your password",
        dsn="pathOfContainer"
    )

@app.route("/")
def home():
    return "Farmer Digital Platform backend is running!"

@app.route("/api/products")
def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT PRODUCT_ID, NAME, PRICE, AVAILABLE_QUANTITY
        FROM PRODUCT
        ORDER BY PRODUCT_ID
    """)

    products = [
        {
            "product_id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "available_quantity": row[3]
        }
        for row in cursor.fetchall()
    ]

    cursor.close()
    connection.close()

    return jsonify(products)


@app.route("/api/orders", methods=["POST"])
def place_order():
    data = request.get_json(silent=True) or {}

    # Validate the input
    try:
        buyer_id = int(data["buyer_id"])
        product_id = int(data["product_id"])
        quantity = int(data["quantity"])

        if buyer_id <= 0 or product_id <= 0 or quantity <= 0:
            return jsonify({"error": "IDs and quantity must be positive."}), 400

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Provide valid buyer_id, product_id and quantity."
        }), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Confirm that the buyer exists
        cursor.execute(
            "SELECT BUYER_ID FROM BUYER WHERE BUYER_ID = :buyer_id",
            {"buyer_id": buyer_id}
        )

        if cursor.fetchone() is None:
            connection.rollback()
            return jsonify({"error": "Buyer not found."}), 404

        # Read the product's current price
        cursor.execute("""
            SELECT NAME, PRICE
            FROM PRODUCT
            WHERE PRODUCT_ID = :product_id
        """, {"product_id": product_id})

        product = cursor.fetchone()

        if product is None:
            connection.rollback()
            return jsonify({"error": "Product not found."}), 404

        product_name, price = product
        total_amount = price * quantity

        # Atomically deduct stock only if sufficient quantity remains
        cursor.execute("""
            UPDATE PRODUCT
            SET AVAILABLE_QUANTITY = AVAILABLE_QUANTITY - :quantity
            WHERE PRODUCT_ID = :product_id
              AND AVAILABLE_QUANTITY >= :quantity
        """, {
            "quantity": quantity,
            "product_id": product_id
        })

        if cursor.rowcount != 1:
            connection.rollback()
            return jsonify({
                "error": "Insufficient stock. Please refresh and try again."
            }), 409

        # Generate IDs for this prototype.
        # Use database sequences for a production/concurrent application.
        cursor.execute("SELECT NVL(MAX(ORDER_ID), 0) + 1 FROM ORDERS")
        order_id = cursor.fetchone()[0]

        # Create the order
        cursor.execute("""
            INSERT INTO ORDERS
                (ORDER_ID, BUYER_ID, ORDER_DATE,
                 TOTAL_AMOUNT, ORDER_STATUS)
            VALUES
                (:order_id, :buyer_id, SYSDATE,
                 :total_amount, 'Confirmed')
        """, {
            "order_id": order_id,
            "buyer_id": buyer_id,
            "total_amount": total_amount
        })

        # Generate an order-item ID from the composite key.
        # ORDER_ITEM uses (ORDER_ID, PRODUCT_ID) as its primary key.
        cursor.execute("""
            INSERT INTO ORDER_ITEM
                (ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE)
            VALUES
                (:order_id, :product_id, :quantity, :unit_price)
        """, {
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": price
        })

        connection.commit()

        return jsonify({
            "message": "Order placed successfully.",
            "order_id": order_id,
            "product": product_name,
            "quantity": quantity,
            "unit_price": float(price),
            "total_amount": float(total_amount)
        }), 201

    except Exception:
        if connection is not None:
            connection.rollback()

        app.logger.exception("Order placement failed")

        return jsonify({
            "error": "Order could not be completed. No changes were saved."
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

@app.route("/api/buyers", methods=["POST"])
def create_buyer():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    email = str(data.get("email", "")).strip()
    address = str(data.get("address", "")).strip()

    if not all([name, phone, email, address]):
        return jsonify({
            "error": "Name, phone, email and address are required."
        }), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Generate the next buyer ID for this prototype
        cursor.execute(
            "SELECT NVL(MAX(BUYER_ID), 0) + 1 FROM BUYER"
        )
        buyer_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO BUYER (BUYER_ID, NAME, PHONE, EMAIL, ADDRESS)
            VALUES (:buyer_id, :name, :phone, :email, :address)
        """, {
            "buyer_id": buyer_id,
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        })

        connection.commit()

        return jsonify({
            "message": "Buyer registered successfully.",
            "buyer_id": buyer_id,
            "name": name
        }), 201

    except Exception:
        if connection is not None:
            connection.rollback()

        app.logger.exception("Buyer registration failed")

        return jsonify({
            "error": "Registration failed. Check the server logs."
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

@app.route("/api/farmers", methods=["POST"])
def register_farmer():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    phone = data.get("phone", "").strip()

    if not name or not email or not phone:
        return jsonify({"error": "Name, email, and phone are required"}), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT NVL(MAX(FARMER_ID), 0) + 1 FROM FARMER"
        )
        farmer_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO FARMER (FARMER_ID, NAME, PHONE, EMAIL)
            VALUES (:1, :2, :3, :4)
            """,
            (farmer_id, name, phone, email)
        )

        connection.commit()

        return jsonify({
            "message": "Farmer registered successfully",
            "farmer_id": farmer_id
        }), 201

    except Exception as e:
        if connection:
            connection.rollback()
        print("Farmer registration error:", e)
        return jsonify({"error": "Could not register farmer"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route("/marketplace")
def marketplace():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    
