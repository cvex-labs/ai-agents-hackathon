# 🏆 CVEXTopia AI Grinder 🏆  
Grind Your Way to the Top with Custom AI Trading Features  

## **Project Summary**  
The **CVEXTopia AI Grinder** is an AI-powered trading application designed to enhance trading on the **CVEX platform**. Built as a **Streamlit web app**, it provides a visually intuitive and feature-rich interface, diverging from the common Telegram bot approach adopted by many other participants.  

### **Why Streamlit Instead of a TG Bot?**  
When the hackathon was announced, I aimed to build something distinct that offers a professional trading experience while keeping the process enjoyable and straightforward. Streamlit enabled me to create a **dedicated web app** that blends usability with advanced trading strategies.  

---

## **Features**  
- **Manual Trade Execution:**  
  - Place orders (Buy Long, Open Short) with customizable parameters (Order Type, Quantity, Limit Price, Time In Force, Reduce Only).  
  - Cancel all active orders at once.  
  - Real-time equity display for tracking your grinding progress.  

- **Position Management:**  
  - View open positions with detailed metrics (Entry Price, Leverage, Unrealized P/L, etc.).  
  - Planned: Add a **Close Position** feature with a safety mechanism (e.g., price divergence smaller than X%) to minimize risks.  

- **AI Strategy Integration:**  
  - Market analysis using GPT-based predictions with confidence scores.  
  - Planned: Add more trading strategies and an **Auto Mode**, where trades are executed automatically if confidence exceeds 80% (with a sleep timer for hourly checks).  

- **User-Friendly UI:**  
  - Fun, gamified design to make trading enjoyable.  
  - Tooltips for each input field for better usability.  
  - Interactive tabs for Manual Trades, Position Info, and AI Strategies.  

---

## **Challenge Track**  
We are aiming for the following tracks:  
1. **Advanced Trading Agents:** Sophisticated trading strategies and automated decision-making.  
2. **Creative User Interfaces:** Unique and interactive Streamlit-based UI.  
3. **Specialized Analysis Tools:** Integrates AI-based market predictions.  
4. **Integration Solutions:** Seamless integration with the CVEX API.  

---

## **💻 Demo Instructions**  

### **Prerequisites:**  
- Python 3.9+  
- Streamlit  
- CVEX API Key (Trusted Mode)  
- OpenAI API Key  

---

### Installation  
1. **Clone the repository:**  
   ```bash
   git clone https://github.com/yourusername/cvextopia-ai-grinder.git
   cd cvextopia-ai-grinder
   ```

2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API keys:**  
   - Generate your CVEX API Key from the CVEX platform.  
   - Store your OpenAI API Key in the environment variable:  
     ```bash
     export OPENAI_API_KEY="your_openai_key"
     ```

### Configuration  
1. **Creating the Configuration File:**  
    - Before running the app, you need to set up your configuration file.
    - Create a file named config.json inside the src folder:
     ```bash
     touch src/config.json
     ```

2. **Add the following configuration template:**  
    ```json
    {
      "CVEX_API_URL": "https://api.cvex.trade",
      "API_KEY": "your_cvex_api_key",
      "PRIVATE_KEY_PATH": "./cvexapi.pem",
      "OPENAI_API_KEY": "your_openai_api_key"
    }
     ```
    **Update the Configuration:**

     - Replace "your_cvex_api_key" and "your_openai_api_key" with your actual API keys.
     - Set the correct path to your Ed25519 private key file.
     - Save the file.
---

### Running the App 

1. **Run the app:**  
   ```bash
   streamlit run src/app.py
   ```

5. **Access the app:**  
   Open your browser and visit:  
   ```
   http://localhost:8501
   ```

### Using the App  
- **Manual Trades:** Execute your orders with full control.  
- **Positions Info:** Keep track of your current open positions.  
- **AI Strategies:** Analyze potential trades and see GPT-based predictions.  

## ⚠️ Important Notes  
Due to the current CVEX API limitation (no available credits), some manual order functions and additional features couldn't be fully tested. Despite this, the app structure and core functionalities are ready for integration once the API issue is resolved.

### Current Limitations:  
- **Manual Trading:** Can view positions but lacks some order management due to API credit exhaustion.  
- **Position Closing:** Planned to add but needed a reliable liquidity check before implementation.  
- **AI Automation:** The foundation is ready, but I wanted to ensure high confidence (80%+) for auto-trades, hence the planned hourly check loop.  

## 🌟 Future Plans  
### Mass Adoption & Error Prevention:  
- Make the bot more robust by preventing error-prone situations and ensuring users understand each trading step.  
- Implement real-time market checks to avoid trading during low liquidity or high volatility periods.  

### Safety First Approach:  
- Develop automated position closing with a price divergence safety check to minimize losses during volatile markets.  

### Enhanced AI Integration:  
- Add more AI trading strategies with tailored risk management.  
- Implement an Auto Grind Mode that continuously monitors the market and executes trades when conditions are favorable.  

### User Feedback:  
- After the Hackathon, I plan to collect feedback from users to improve UI and functionality.  
- Regular updates to adapt to changing market conditions and user preferences.  

## 💬 Why Vote for CVEXTopia AI Grinder?  
This project was built with the community in mind. I believe CVEX can thrive if users feel in control of their trades rather than overwhelmed by data or uncertain execution. By making a fun, intuitive, and strategic tool, I aim to empower traders to make better decisions while enjoying the grind. Let’s make CVEX not just functional but fun!


### 💡 Usage:
- **Manual Trades:**
     - Select your contract from the dropdown.
     - Input quantity, order type, limit price (if applicable), time in force, and whether to reduce the position.
     - Click Open Long or Open Short to place the order.
     - Check Positions Info for the updated position list.

- **Position Management:**
     - View your active positions and open orders.
     - Click Cancel All Orders to clear your active trades.

- **AI Strategies:**
     - Choose a contract and click Analyze Potential to get AI-driven insights.
     - The AI provides a trading decision (LONG, SHORT, STAY OUT) and a confidence score.
     - Use these insights to make informed trading decisions.

### ⚠️ Important Notes:
Due to the current CVEX API limitation (no available credits), some manual order functions and additional features couldn't be fully tested.
Despite this, the app structure and core functionalities are prepared for further integration once the API issue is resolved.

- **Known Issues:**
     - Manual Trading: Order management may have limited testing due to API credit exhaustion.
     - Position Closing: Planned to add a safe closing mechanism.
     - AI Automation: The foundation is ready, but automatic trading needs more testing.

### 🌟 Future Plans:
- **Mass Adoption & Error Prevention:**
     - Implement real-time market checks to avoid trading during low liquidity or high volatility periods.

- **Enhanced AI Integration:**
     - Add more AI trading strategies with tailored risk management.

     - Implement an Auto Grind Mode for continuous monitoring and execution.

- **Safety-First Approach:**
     - Automated position closing with a price divergence safety check to minimize losses during volatile markets.

- **User Feedback:**
     - Gather feedback to improve UI/UX and add more requested features.

### Why Vote for CVEXTopia AI Grinder?
This project was built with the community in mind.
I believe CVEX can thrive if users feel empowered and confident while trading.
By combining intuitive design, advanced AI insights, and a fun approach, CVEXTopia AI Grinder makes trading more accessible and enjoyable.
Let’s make trading not just profitable but also fun!