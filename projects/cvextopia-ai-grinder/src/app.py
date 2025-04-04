import streamlit as st
import pandas as pd
from trade_executor import place_order, get_account_overview, get_open_orders, get_positions, cancel_all_orders
from strategies import get_all_contracts, analyze_market, parse_gpt_response
import base64
from config_loader import load_config

# Load configuration
config = load_config()


# Background Image Function
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: 80%; 
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to add the background
add_bg_from_local("../images/image.png")

st.markdown(
    """
    <style>
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center; /* Center the tabs */
        gap: 20px; /* Space between tabs */
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.2rem; /* Increase font size */
        font-weight: bold; /* Make the text bold */
        padding: 10px 20px; /* Add some padding */
        border-radius: 10px; /* Round the corners */
        color: #ffffff; /* Text color */
        background-color: #333333; /* Background color */
        margin: 5px; /* Add margin between tabs */
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF6347; /* Different color for selected tab */
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Title and Header
st.title('🏆 CVEXTopia AI Grinder 🏆')
st.header('Climb Your Way to the Top with Custom AI Trading Features')

# Display account equity with fun text
account = get_account_overview()
equity = account.get("portfolio", {}).get("equity", "N/A")
st.subheader(f'💰 (Equity): {equity} USD')

# Tabbed UI
tabs = st.tabs(["🛠️ Manual Trades", "📊 Positions Info", "🤖 AI Strategies"])

# Manual Trades Tab
with tabs[0]:
    st.subheader("🛠️ Manual Mode: Take Control of Your Grind")

    # Initialize session state for contract selection
    if 'selected_contract' not in st.session_state:
        st.session_state.selected_contract = None

    # Fetch all available contracts for the dropdown
    contracts = get_all_contracts()
    contract_symbols = [f"{contract.get('symbol', 'Unknown')} (ID: {contract.get('contract_id', 'N/A')})" for contract in contracts]

    # Contract selection with session state persistence
    def update_contract():
        st.session_state.selected_contract = st.session_state.contract_choice

    # Extract contract ID correctly from the selected dropdown option
    def extract_contract_id(selected_contract, contracts):
        for contract in contracts:
            symbol_with_id = f"{contract.get('symbol', 'Unknown')} (ID: {contract.get('contract_id', 'N/A')})"
            if symbol_with_id == selected_contract:
                return contract.get('contract_id', 'N/A')
        return 'N/A'

    # Use session state to maintain the selected contract
    selected_contract = st.selectbox(
        "Select Your Grinding Contract",
        options=contract_symbols,
        index=0 if st.session_state.selected_contract is None else contract_symbols.index(st.session_state.selected_contract),
        key='contract_choice',
        on_change=update_contract,
        help="Select the contract to start your grind."
    )

    # Get the contract ID from the selected contract
    contract_id = extract_contract_id(selected_contract, contracts)
    st.write(f"📝 DEBUG: Contract ID being used: {contract_id}")

    # Input fields for trading parameters with tooltips
    quantity = st.text_input("Quantity (Steps)", value="1", key='quantity', help="Specify the quantity of the asset to trade. Use whole numbers for contracts.")
    order_type = st.selectbox("Order Type", ["market", "limit"], key='order_type', help="Market: Instant grind. Limit: Grind when the price matches your target.")
    limit_price = st.text_input("Limit Price (if applicable)", value="0", key='limit_price', help="Set your price for limit orders. Leave as 0 for market orders.")
    time_in_force = st.selectbox("Time In Force", ["GTC", "IOC", "FOK", "PO"], key='time_in_force', help="Order duration: GTC (Good Till Canceled), IOC (Instant or Cancel), FOK (Fill or Kill), PO (Post Only).")
    reduce_only = st.checkbox("Reduce Only", value=False, key='reduce_only', help="Enable to reduce your size instead of opening new positions.")

    # Execute order function
    def execute_order(order_side):
        try:
            formatted_quantity = float(quantity.replace(",", "."))
            quantity_value = str(formatted_quantity) if order_side == "buy" else str(-formatted_quantity)
            result = place_order(contract_id, order_side, quantity_value, order_type, limit_price, time_in_force, reduce_only)
            st.write(f"🚀 Grind Result: {result}")
        except ValueError:
            st.error("Invalid quantity or limit price format. Please use numeric values.")

    # Trade buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏁 Open Long"):
            execute_order("buy")
    with col2:
        if st.button("🔄 Open Short"):
            execute_order("sell")

# Positions Info Tab
with tabs[1]:
    st.subheader("📊 Current Positions")
    if st.button("🔄 Refresh Positions"):
        positions = get_positions()
        if not positions:
            st.info("No active positions.")
        else:
            df = pd.DataFrame(positions)
            st.table(df)

    st.subheader("📑 Active Orders")
    if st.button("🔄 Refresh Orders"):
        orders = get_open_orders()
        if not orders:
            st.info("No open orders.")
        else:
            df = pd.DataFrame(orders)
            st.table(df)

    # Cancel All Orders Button
    st.subheader("🚫 Cancel All Orders")
    if st.button("💥 Cancel All Orders"):
        result = cancel_all_orders()
        if result.get("status") == "success":
            st.success("✅ All orders canceled.")
        else:
            st.error(f"❌ Failed to cancel orders: {result}")

# AI Strategies Tab
with tabs[2]:
    st.subheader("🤖 AI Strategies: Automate Your Grind")

    # Use the same contract selection as in the Manual Trades tab
    selected_contract_ai = st.selectbox(
        "Select Contract for Analysis",
        options=contract_symbols,
        index=0 if st.session_state.selected_contract is None else contract_symbols.index(st.session_state.selected_contract),
        key='ai_contract_choice',
        help="Choose a contract to analyze."
    )

    # Get the contract ID for the selected AI contract
    contract_id_ai = extract_contract_id(selected_contract_ai, contracts)
    st.write(f"📝 DEBUG: Contract ID being analyzed: {contract_id_ai}")

    if st.button("🔍 Analyze Potential"):
        selected_data = next((c for c in contracts if str(c.get('contract_id', 'N/A')) == str(contract_id_ai)), None)
        if selected_data:
            analysis = analyze_market(selected_data)
            st.write("💡 AI Insight:")
            st.text(analysis)
            decision, confidence = parse_gpt_response(analysis)
            if decision:
                st.write(f"✅ Decision: {decision}")
                st.write(f"📊 Confidence: {confidence}%")
            else:
                st.error("Failed to parse AI response.")
        else:
            st.error("Failed to retrieve contract data.")
