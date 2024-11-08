import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Simulated in-memory data
users = {}
houses = {
    "Rua_Bien": {"current_price": 100, "volume": 1000, "price_history": []},
    "Voi": {"current_price": 120, "volume": 800, "price_history": []},
    "Te_Giac": {"current_price": 90, "volume": 1200, "price_history": []},
    "Ho": {"current_price": 110, "volume": 1100, "price_history": []}
}
portfolios = {}
news_impact = {"Rua_Bien": 0, "Voi": 0, "Te_Giac": 0, "Ho": 0}

# Helper functions
def register_user():
    username = fake.user_name()
    if username not in users:
        house = random.choice(list(houses.keys()))
        users[username] = {"house": house, "points_balance": 1000}
        portfolios[username] = {house: {"shares": 0}}
    return username

def submit_news():
    house = random.choice(list(houses.keys()))
    impact_score = random.uniform(-0.05, 0.1)  # Impact between -5% and +10%
    news_impact[house] = impact_score

def adjust_stock_prices():
    for house, data in houses.items():
        price_change = data["current_price"] * (news_impact[house] + random.uniform(-0.01, 0.01))
        data["current_price"] += price_change
        data["current_price"] = round(data["current_price"], 2)
        data["price_history"].append({
            "date": current_date.strftime("%Y-%m-%d"),
            "price": data["current_price"]
        })
        news_impact[house] = 0  # Reset impact after price adjustment

def user_trade(username):
    house = random.choice(list(houses.keys()))
    shares = random.randint(1, 10)
    user_data = users[username]

    if random.choice(["buy", "sell"]) == "buy" and user_data["points_balance"] >= shares * houses[house]["current_price"]:
        total_cost = shares * houses[house]["current_price"]
        user_data["points_balance"] -= total_cost
        portfolios[username].setdefault(house, {"shares": 0})
        portfolios[username][house]["shares"] += shares
        houses[house]["volume"] -= shares

    elif house in portfolios[username] and portfolios[username][house]["shares"] >= shares:
        sale_amount = shares * houses[house]["current_price"]
        user_data["points_balance"] += sale_amount
        portfolios[username][house]["shares"] -= shares
        houses[house]["volume"] += shares

# Simulation loop
start_date = datetime.now() - timedelta(days=14)
for day in range(14):
    current_date = start_date + timedelta(days=day)

    for _ in range(5):
        register_user()

    if day % 2 == 0:
        submit_news()

    for username in users.keys():
        user_trade(username)

    adjust_stock_prices()

# Save data to JSON files
with open('users.json', 'w') as f:
    json.dump(users, f, indent=4)

with open('portfolios.json', 'w') as f:
    json.dump(portfolios, f, indent=4)

with open('houses.json', 'w') as f:
    json.dump(houses, f, indent=4)

print("Data saved to JSON files.")
