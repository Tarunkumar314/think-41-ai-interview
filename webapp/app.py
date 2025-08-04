from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_db_connection

app = Flask(__name__)
CORS(app)

# Route 1: List all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, first_name, last_name, email
        FROM users
        LIMIT ? OFFSET ?
    """, (limit, offset))
    customers = cursor.fetchall()
    conn.close()

    if not customers:
        return jsonify({'error': 'No customers found'}), 404

    result = []
    for customer in customers:
        result.append({
            'id': customer['id'],
            'first_name': customer['first_name'],
            'last_name': customer['last_name'],
            'email': customer['email']
        })

    return jsonify(result), 200

# Route 2: Get specific customer details + order count
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer_details(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (customer_id,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({'error': 'Customer not found'}), 404

    cursor.execute("SELECT COUNT(*) AS order_count FROM orders WHERE user_id = ?", (customer_id,))
    order_data = cursor.fetchone()

    conn.close()

    customer_info = {
        'id': user['id'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'email': user['email'],
        'order_count': order_data['order_count']
    }

    return jsonify(customer_info), 200
@app.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_orders_for_customer(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE id = ?", (customer_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'Customer not found'}), 404

    cursor.execute("""
        SELECT order_id, status, created_at, shipped_at, delivered_at, returned_at, num_of_item
        FROM orders
        WHERE user_id = ?
    """, (customer_id,))
    orders = cursor.fetchall()
    conn.close()

    return jsonify([
        dict(order) for order in orders
    ]), 200

# Get specific order details
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get order info
    cursor.execute("""
        SELECT * FROM orders WHERE order_id = ?
    """, (order_id,))
    order = cursor.fetchone()

    if not order:
        conn.close()
        return jsonify({'error': 'Order not found'}), 404

    # Get items in this order
    cursor.execute("""
        SELECT oi.id AS order_item_id,
               oi.product_id,
               oi.status,
               oi.created_at,
               oi.shipped_at,
               oi.delivered_at,
               oi.returned_at,
               p.name AS product_name,
               p.brand,
               p.category,
               p.retail_price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    """, (order_id,))
    items = cursor.fetchall()
    conn.close()

    return jsonify({
        'order_id': order['order_id'],
        'user_id': order['user_id'],
        'status': order['status'],
        'created_at': order['created_at'],
        'shipped_at': order['shipped_at'],
        'delivered_at': order['delivered_at'],
        'returned_at': order['returned_at'],
        'num_of_item': order['num_of_item'],
        'items': [dict(item) for item in items]
    }), 200
# Error handler for invalid endpoints
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
