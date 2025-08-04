from flask import Flask, jsonify, abort, request
from db import get_db_connection
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# GET /customers - List all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    conn = get_db_connection()
    customers = conn.execute(
        'SELECT id, first_name, last_name, email, created_at FROM users LIMIT ? OFFSET ?',
        (limit, offset)
    ).fetchall()
    conn.close()

    result = [dict(row) for row in customers]
    return jsonify(result), 200

# GET /customers/<id> - Get customer detail with order count
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    conn = get_db_connection()

    # Fetch customer
    user = conn.execute(
        'SELECT id, first_name, last_name, email, created_at FROM users WHERE id = ?',
        (customer_id,)
    ).fetchone()

    if user is None:
        conn.close()
        abort(404, description="Customer not found")

    # Fetch order count
    order_count = conn.execute(
        'SELECT COUNT(*) as total FROM orders WHERE user_id = ?',
        (customer_id,)
    ).fetchone()

    conn.close()

    customer_data = dict(user)
    customer_data["order_count"] = order_count["total"]

    return jsonify(customer_data), 200

# Handle 404
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(debug=True)
