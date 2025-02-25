import requests
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)

# 🔑 API Keys
ETHERSCAN_API_KEY = "Your Etherscan API Key"
DEX_SCREENER_API = "https://api.dexscreener.com/token/{}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_token():
    data = request.get_json()
    address = data.get("address")

    if not address:
        return jsonify({"error": "Token address is required"}), 400

    try:
        # 1️⃣ **Fetch Token Price & Liquidity**
        token_price, liquidity = get_token_price_liquidity(address)

        # 2️⃣ **Get Total Supply**
        total_supply = get_total_supply(address)

        # 3️⃣ **Calculate Market Cap**
        market_cap = (total_supply * token_price) if token_price else "N/A"

        # 4️⃣ **Risk Factor Analysis**
        risk_factor = calculate_risk_factor(address)

        # 5️⃣ **Fetch Solidity Source Code (Last)**
        contract_info = get_contract_details(address)
        if "error" in contract_info:
            return jsonify(contract_info), 404

        # 6️⃣ **Count Number of Lines in Solidity Code**
        num_lines = contract_info["source_code"].count("\n") if contract_info["source_code"] else 0

        return jsonify({
            "Market Cap (USD)": market_cap,
            "Token Price (USD)": token_price,
            "Liquidity (USD)": liquidity,
            "Total Supply": total_supply,
            "No. of Lines in Code": num_lines,
            "Risk Factor": risk_factor,
            "Solidity Source Code": contract_info["source_code"]  # Placed at the end
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Something went wrong."}), 500

# 📌 **Helper Functions**
def get_contract_details(address):
    """
    Fetches contract source code from Etherscan.
    """
    url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url).json()
    
    if response["status"] == "1":
        contract_data = response["result"][0]
        source_code = contract_data["SourceCode"]
        return {"source_code": source_code}
    
    return {"error": "Contract not found"}

def get_token_price_liquidity(address):
    """
    Fetches token price and liquidity from Dex Screener API.
    """
    try:
        response = requests.get(DEX_SCREENER_API.format(address)).json()
        if "pairs" in response:
            price = float(response["pairs"][0]["priceUsd"])
            liquidity = float(response["pairs"][0]["liquidity"]["usd"])
            return price, liquidity
    except:
        return None, None
    return None, None

def get_total_supply(address):
    """
    Fetches total supply from the contract.
    """
    url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={address}&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url).json()
    
    if response["status"] == "1":
        return int(response["result"]) / 1e18  # Convert Wei to ETH units
    return "N/A"

def calculate_risk_factor(address):
    """
    Analyzes the contract for potential risks.
    """
    holders_url = f"https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress={address}&apikey={ETHERSCAN_API_KEY}"
    holders_response = requests.get(holders_url).json()

    if holders_response["status"] == "1":
        holders = holders_response["result"]
        if len(holders) < 10:
            return "High (Few Holders - Possible Scam)"
        top_holder_balance = int(holders[0]["TokenHolderBalance"]) / 1e18
        if top_holder_balance > 0.5:  # If a single holder has > 50% of supply
            return "High (Centralized Ownership)"
    
    return "Low (More Decentralized)"

if __name__ == "__main__":
    app.run(debug=True)
