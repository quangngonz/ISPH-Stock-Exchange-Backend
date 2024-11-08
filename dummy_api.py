from pyexpat.errors import messages

from flask import Flask, request, redirect
from flask_restx import Api, Resource, fields
import json, os

app = Flask(__name__)

@app.route('/')
def redirect_to_docs():
    return redirect('/docs', code=302)

api = Api(app, doc='/docs')  # Enable Swagger UI at /docs

# Utility function to retrieve parameters
def get_param(param_name, default=None):
    """Retrieve parameter from query params or JSON body, with optional default."""
    # Check query params first
    value = request.args.get(param_name)
    if value is not None:
        return value
    # Check JSON body if query param is not found
    data = request.get_json(silent=True) or {}
    return data.get(param_name, default)

# Load data from JSON files in the 'data' folder
def load_data():
    base_dir = os.path.dirname(__file__)  # Get the current directory of the script
    data_dir = os.path.join(base_dir, 'data')  # Path to 'data' folder

    with open(os.path.join(data_dir, 'users.json')) as f:
        users_json = json.load(f)
    with open(os.path.join(data_dir, 'portfolios.json')) as f:
        portfolios_json = json.load(f)
    with open(os.path.join(data_dir, 'houses.json')) as f:
        houses_json = json.load(f)

    return users_json, portfolios_json, houses_json

users, portfolios, houses = load_data()

# Define API Models for input validation and documentation
user_model = api.model('User', {
    'username': fields.String(required=True, description='The user\'s username'),
    'house': fields.String(required=True, description='The house the user belongs to'),
    'points_balance': fields.Integer(required=True, description='User\'s points balance')
})

portfolio_model = api.model('Portfolio', {
    'username': fields.String(required=True, description='The user\'s username'),
    'portfolio': fields.List(fields.String, description='The stocks in the user\'s portfolio'),
    'points_balance': fields.Integer(description='User\'s points balance')
})

house_model = api.model('House', {
    'name': fields.String(required=True, description='The name of the house'),
    'current_price': fields.Float(required=True, description='Current stock price for the house'),
    'price_history': fields.List(fields.Float, description='The price history of the house\'s stock'),
    'volume': fields.Integer(description='Volume of stocks available')
})

# Define models for each POST request
register_model = api.model('RegisterModel', {
    'username': fields.String(required=True, description='The user\'s username'),
    'house': fields.String(required=True, description='The house the user belongs to'),
    'points_balance': fields.Integer(required=True, description='User\'s points balance')
})

buy_model = api.model('BuyModel', {
    'username': fields.String(required=True, description='The username of the student'),
    'house_name': fields.String(required=True, description='The name of the house to buy stocks from'),
    'quantity': fields.Integer(required=True, description='The number of stocks to buy')
})

earn_points_model = api.model('EarnPointsModel', {
    'username': fields.String(required=True, description='The username of the student'),
    'points': fields.Integer(required=True, description='The number of points to add'),
    'code': fields.String(required=True, description='The secret code to verify the request (default: "secret")')
})

# Resource classes
class Register(Resource):
    @api.doc(description='Register a new user with house assignment')
    @api.expect(register_model)
    def post(self):
        # Use get_param to retrieve parameters from query params or JSON body
        username = get_param('username')
        house = get_param('house')
        points_balance = get_param('points_balance')

        # Validate that all required data is present
        if not username or not house or points_balance is None:
            return {"message": "Missing required data (username, house, or points_balance)"}, 400

        # Ensure points_balance is an integer
        try:
            points_balance = int(points_balance)
        except ValueError:
            return {"message": "Points balance must be a valid integer"}, 400

        # Check if user already exists
        if username in users:
            return {"message": f"User {username} already exists."}, 400

        # Register the user
        users[username] = {'house': house, 'points_balance': points_balance}

        # Save updated users data to file
        with open('data/users.json', 'w') as f:
            f.write(json.dumps(users, indent=4))

        return {"message": f"User {username} registered successfully."}, 200

class Buy(Resource):
    @api.doc(description='Buy stocks for a specific house')
    @api.expect(buy_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        house_name = data.get('house_name')
        quantity = data.get('quantity')

        # Validate that we have the necessary data
        if not username or not house_name or not quantity:
            return {"message": "Missing required data (username, house_name, or quantity)"}, 400

        # Validation checks
        if username not in users:
            return {"message": "User not found"}, 404

        if house_name not in houses:
            return {"message": "House not found"}, 404

        if int(quantity) <= 0:
            return {"message": "Invalid quantity"}, 400

        message = f"{quantity} stocks bought for {house_name} by {username} successfully."
        return {"message": message}, 200


class Sell(Resource):
    @api.doc(description='Sell stocks from a user\'s portfolio')
    @api.expect(buy_model)  # Reusing buy_model for simplicity
    def post(self):
        username = get_param('username')
        house_name = get_param('house_name')
        quantity = get_param('quantity')

        # Validate that all required data is present
        if not username or not house_name or quantity is None:
            return {"message": "Missing required data (username, house_name, or quantity)"}, 400

        # Validation checks
        if username not in users:
            return {"message": "User not found"}, 404
        if house_name not in houses:
            return {"message": "House not found"}, 404

        message = f"{quantity} stocks sold for {house_name} by {username} successfully."
        return {"message": message}, 200

class Portfolio(Resource):
    @api.doc(description='Get the portfolio of a specific user')
    @api.param('username', 'The username of the user')
    def get(self):
        username = get_param('username')

        if not username:
            return {"message": "Username is required"}, 400

        if username not in users:
            return {"message": "User not found"}, 404

        portfolio = portfolios.get(username, [])
        return {"portfolio": portfolio}, 200


class EarnPoints(Resource):
    @api.doc(description='Update student points based on good performance')
    @api.expect(earn_points_model)
    def post(self):
        username = get_param('username')
        points = get_param('points')
        code = get_param('code')

        if code != "secret":
            return {"message": "Invalid code"}, 401
        if username not in users:
            return {"message": "User not found"}, 404
        users[username]["points_balance"] += int(points)

        with open('data/users.json', 'w') as f:
            f.write(json.dumps(users, indent=4))

        return {"message": f"{points} points added to {username}"}, 200


class Leaderboard(Resource):
    @api.doc(description='Display top students or houses based on stock performance and points')
    def get(self):
        sorted_leaderboard = sorted(users.items(), key=lambda x: x[1]["points_balance"], reverse=True)
        return {"leaderboard": sorted_leaderboard}, 200


class PriceHistory(Resource):
    @api.doc(description='Get historical stock price data for a specific house')
    @api.param('house_name', 'The name of the house')
    def get(self):
        house_name = get_param('house_name')
        if house_name not in houses:
            return {"message": "House not found"}, 404
        return {"price_history": houses[house_name]["price_history"]}, 200


class AllHouses(Resource):
    @api.doc(description='Get the entire house data')
    def get(self):
        return {"houses": houses}, 200


class Houses(Resource):
    @api.doc(description='Get a list of all available houses')
    def get(self):
        return {"houses": list(houses.keys())}, 200


# API Resource Routing
api.add_resource(Register, '/register')
api.add_resource(Houses, '/houses')
api.add_resource(Buy, '/buy')
api.add_resource(Sell, '/sell')  
api.add_resource(Portfolio, '/portfolio')
api.add_resource(EarnPoints, '/earn-points')
api.add_resource(Leaderboard, '/leaderboard')
api.add_resource(PriceHistory, '/price-history')
api.add_resource(AllHouses, '/all-houses')

if __name__ == '__main__':
    app.run(debug=True)
