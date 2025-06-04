# 🍽️ Effortless Dining with Food Ordering Chatbot
Ruby is a real-time food ordering chatbot designed for seamless user experience. Built with intuitive conversational AI, Ruby streamlines food orders, integrates with restaurant menus, and enhances customer satisfaction. 

Overview
This system is designed to simplify food ordering with:
- 🤖 Interactive chatbot
- 🍕 Live menu display
- 📦 Order tracking
- 📊 Database integration

Tech Stack
- 🤖 **Chatbot Development**: Google's Dialogflow
- 💾 **Backend**: MySQL Workbench + Python (PyCharm)
- 🌐 **HTTPS Tunneling**: Cloudflare Tunnel (SSL keys)
- 🖥️ **Frontend**: Static/Dynamic website (HTML/CSS or Streamlit)

🚀 How to Run This Project Locally
### Step 1: Backend Setup
- Open PyCharm
- Navigate to: `food_chatbot_backend/`
- Run `mainn.py`

### Step 2: Generate HTTPS Tunnel
- Open Windows PowerShell
- Run the following command:
```bash
cloudflared tunnel --url https://localhost:8001 --no-tls-verify
```
* Copy the HTTPS link generated
### Step 3: Google Dialogflow Setup
- Login to your Google Cloud Console
-Go to your Dialogflow agent (e.g., Ruby-Chatbot)
-Navigate to Fulfillment
-Paste the HTTPS link from Step 2 in the Webhook URL

### Step 4: Frontend Website
-Open the website folder (e.g., Ruchi_Suchi/)
-Launch the website locally or on a server




Demo 🎬
Quick walkthrough of how the system works 👇
### 🖥️ Website UI
![ruchi_suchi_website](https://github.com/user-attachments/assets/773077b8-0d27-4bc8-afe7-357f67d50cd3)
![image](https://github.com/user-attachments/assets/3ada32fd-290f-424e-8c54-0b29651d1412)

### 💬 Chatbot Conversation
![chatbot_conv](https://github.com/user-attachments/assets/154eba81-d238-4dd5-a36c-142caea4fde1)

### 🗄️ Database Storage
![chatbot_conv](https://github.com/user-attachments/assets/7797ad77-a12b-42fe-a012-f2509b4401ac)

