# Smart Contract Security Analyzer

## Overview
This project is a Flask-based web application that analyzes the security and key financial metrics of Ethereum-based smart contracts. It fetches data from external APIs like Etherscan and Dex Screener to provide insights into token price, liquidity, market capitalization, and potential risk factors.

## Features
- Fetches token price and liquidity from Dex Screener.
- Retrieves total supply and calculates market capitalization.
- Fetches Solidity source code from Etherscan.
- Counts the number of lines in the Solidity source code.
- Analyzes risk factors such as the number of holders and ownership concentration.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Flask
- Flask-CORS
- Requests module

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open a browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## API Endpoints
### `GET /`
- Renders the homepage (`index.html`).

### `POST /analyze`
- **Request Body (JSON):**
  ```json
  {
    "address": "0xTokenContractAddress"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "Market Cap (USD)": 12345678.90,
    "Token Price (USD)": 1.23,
    "Liquidity (USD)": 987654.32,
    "Total Supply": 100000000,
    "No. of Lines in Code": 250,
    "Risk Factor": "Low (More Decentralized)",
    "Solidity Source Code": "pragma solidity ^0.8.0; ..."
  }
  ```

## Helper Functions
- `get_contract_details(address)`: Fetches contract source code from Etherscan.
- `get_token_price_liquidity(address)`: Retrieves token price and liquidity from Dex Screener.
- `get_total_supply(address)`: Fetches total supply from Etherscan.
- `calculate_risk_factor(address)`: Evaluates the risk factor based on holder distribution.

## Environment Variables
This project uses API keys for external services:
- `ETHERSCAN_API_KEY`: Your Etherscan API key.
- `DEX_SCREENER_API`: Endpoint for Dex Screener API.

## License
This project is licensed under the MIT License.

## Author
Allu Mahendra

