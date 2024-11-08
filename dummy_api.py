from flask import Flask, jsonify, request, redirect, url_for
from flask_restx import Api, Resource, fields
import json, os

app = Flask(__name__)

@app.route('/')
def redirect_to_docs():
    return redirect('/docs', code=302)

api = Api(app, doc='/docs')  # Enable Swagger UI at /docs

# Load data from JSON files in the 'data' folder
def load_data():
    base_dir = os.path.dirname(__file__)  # Get the current directory of the script
    data_dir = os.path.join(base_dir, 'data')  # Path to 'data' folder
    
    with open(os.path.join(data_dir, 'users.json')) as f:
        users = json.load(f)
    with open(os.path.join(data_dir, 'portfolios.json')) as f:
        portfolios = json.load(f)
    with open(os.path.join(data_dir, 'houses.json')) as f:
        houses = json.load(f)
    
    return users, portfolios, houses

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

# API Endpoints
class Register(Resource):
    @api.doc(description='Register a new user with house assignment')
    @api.expect(user_model)
    def post(self):
        return {"message": "This endpoint is for demonstration only."}, 200

class Houses(Resource):
    @api.doc(description='Fetch the list of houses and current stock values')
    @api.param('house_name', 'The name of the house to get the stock value for', type=str)
    def get(self):
        house_name = request.args.get('house_name', None)
        if house_name:
            house_data = houses.get(house_name)
            if house_data:
                return {house_name: house_data}, 200
            else:
                return {"message": "House not found"}, 404
        return {"houses": houses}, 200

class Buy(Resource):
    @api.doc(description='Buy stocks for a specific house')
    def post(self):
        return {"message": "This endpoint is for demonstration only."}, 200

class Sell(Resource):
    @api.doc(description='Sell stocks for a specific house')
    def post(self):
        return {"message": "This endpoint is for demonstration only."}, 200

class Portfolio(Resource):
    @api.doc(description='View a student\'s current stock portfolio and points balance')
    @api.param('username', 'The username of the student')
    def get(self):
        username = request.args.get('username')
        if username not in users:
            return {"message": "User not found"}, 404
        return {"portfolio": portfolios.get(username), "points_balance": users[username]["points_balance"]}, 200

class EarnPoints(Resource):
    @api.doc(description='Update student points based on good performance')
    @api.param('username', 'The username of the student')
    @api.param('points', 'The number of points to add')
    @api.param('code', 'The secret code to verify the request')
    def post(self):
        username = request.args.get('username')
        points = request.args.get('points')
        code = request.args.get('code')
        if code != "secret":
            return {"message": "Invalid code"}, 401
        if username not in users:
            return {"message": "User not found"}, 404
        users[username]["points_balance"] += int(points)

        with open('data/users.json', 'w') as f:
            json.dump(users, f, indent=4)

        return {"message": f"{points} points added to {username}"}, 200

class Leaderboard(Resource):
    @api.doc(description='Display top students or houses based on stock performance and points')
    def get(self):
        sorted_leaderboard = sorted(users.items(), key=lambda x: x[1]["points_balance"], reverse=True)
        leaderboard_data = [{"username": user, "points_balance": data["points_balance"]} for user, data in sorted_leaderboard]
        return {"leaderboard": leaderboard_data}, 200

class PriceHistory(Resource):
    @api.doc(description='Get the price history for a house stock')
    @api.param('house_name', 'The name of the house to get the price history for')
    def get(self, house_name):
        if house_name not in houses:
            return {"message": "House not found"}, 404
        return {"price_history": houses[house_name].get("price_history", [])}, 200

class AllHouses(Resource):
    @api.doc(description='Get the entire house data')
    def get(self):
        return {"houses": houses}, 200

# API Resource Routing
api.add_resource(Register, '/register')
api.add_resource(Houses, '/houses')
api.add_resource(Buy, '/buy')
api.add_resource(Sell, '/sell')
api.add_resource(Portfolio, '/portfolio')
api.add_resource(EarnPoints, '/earn-points')
api.add_resource(Leaderboard, '/leaderboard')
api.add_resource(PriceHistory, '/price-history/<house_name>')
api.add_resource(AllHouses, '/all-houses')

if __name__ == '__main__':
    app.run(debug=False)
