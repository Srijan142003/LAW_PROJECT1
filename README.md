# Justice For All - AI Legal Assistant & Verdict Simulator

![Project Banner](https://placehold.co/1200x400/0d1117/7f8c8d?text=Justice%20For%20All&font=montserrat)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An innovative web application powered by Python, Flask, and Generative AI to provide simulated legal assistance. This project offers two primary features: a court trial simulation that generates AI-based verdicts and a conversational AI chatbot for legal consultation.

## ✨ Features

-   **User Authentication:** Secure registration and login system for users.
-   **AI Court Trial Simulation:** Users can input arguments from both the accuser and defender, upload supporting documents, and receive a detailed, AI-generated verdict structured like a real legal judgment.
-   **AI Legal Consultation:** A real-time chat interface where users can ask legal questions and receive guidance from a powerful language model.
-   **Dynamic Knowledge Base:** The application can fetch data from the Indian Kanoon API to build a relevant knowledge base for its AI.
-   **Admin Dashboard:** A dedicated panel for administrators to monitor user activity, view case statistics, and review user feedback on generated verdicts.
-   **Feedback System:** Users can rate and provide feedback on the AI-generated verdicts to help improve the system.

## 🛠️ Tech Stack

-   **Backend:** Python, Flask
-   **Frontend:** HTML, JavaScript, Bootstrap 5
-   **Generative AI:** Google Gemini / OpenAI (via API)
-   **External APIs:** Indian Kanoon API for legal document retrieval
-   **Database:** Flat-file JSON for storing user data, logs, and application info.

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

Make sure you have the following installed:
-   [Python 3.8+](https://www.python.org/downloads/)
-   [Git](https://git-scm.com/)

### 1. Clone the Repository

First, clone the project to your local machine.

```
git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git)
cd YourRepoName
```
2. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

```
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install Dependencies
Install all the required Python packages using the ```requirements.txt``` file.

```pip install -r requirements.txt```

4. Set Up Environment Variables (Crucial Step!)
This project requires API keys and a secret key to function correctly. You must create a .env file in the root directory of the project.

Step 1: Create a file named ```.env``` in the project's root folder.

Step 2: Copy the content from the example below into your new ```.env``` file.

Code snippet
```
# example.env - Copy this into a new .env file

# --- Flask Configuration ---
# Generate your own secret key. A long, random string is best.
FLASK_SECRET_KEY='your_super_secret_key_for_sessions_and_flash_messages'

# --- API Keys ---
# Add your API key for the Indian Kanoon service
INDIAN_KANOON_API_KEY='your_indian_kanoon_api_key_here'

# Add your API key for the Generative AI Model (e.g., Google Gemini)
GOOGLE_API_KEY='your_google_ai_api_key_here'
Step 3: Replace the placeholder values (your_..._key_here) with your actual keys.
```
5. Running the Application
Once the setup is complete, you can run the Flask application.

The application will be available at ```http://127.0.0.1:5000``` in your web browser.

📂 Project Structure
Here is a brief overview of the key files in the project:
```
.
├── app.py                  # Main Flask application, routes, and logic
├── main.py                 # Script for interacting with APIs and building knowledge base
├── requirements.txt        # List of Python dependencies
├── .gitignore              # Files and folders to be ignored by Git
├── .env                    # (You create this) Stores secret keys and environment variables
├── static/
│   └── css/
│       └── style.css       # Custom stylesheets
└── templates/              # HTML files for the user interface
    ├── layout.html         # Main layout template for all pages
    ├── login.html          # User login page
    ├── register.html       # User registration page
    ├── home.html           # Welcome/dashboard page after login
    ├── trial.html          # Page for submitting a case for verdict simulation
    ├── result.html         # Page to display the AI-generated verdict and get feedback
    ├── consult.html        # AI legal consultation chat page
    └── admin.html          # Administrator dashboard page
```

📄 Data Files and Runtime Generation
Several JSON files are used to store data. Some are part of the repository, while others are generated automatically by app.py when you run the application.

```knowledge_base.json```: Stores legal data fetched from APIs. This should be included in the repository.

The following files will be created automatically in your project folder if they don't exist. They are intentionally excluded from the repository via .gitignore because they contain user-specific or session-specific data.

```users.json```: Stores user registration details, including usernames and hashed passwords.

```admin_data.json```: Tracks admin-level statistics like user visits, feedback, and case types.

```chat_logs.json```: Saves the conversation history for each user from the "Consult a Lawyer" feature.

```user_memory_store.json```: Caches user-specific data, such as past court trial summaries.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, please feel free to fork the repository and create a pull request.

Fork the project.

Create your feature branch (```git checkout -b feature/AmazingFeature```).

Commit your changes (```git commit -m 'feat: Add some AmazingFeature'```).

Push to the branch (```git push origin feature/AmazingFeature```).

Open a Pull Request.

📄 License
This project is distributed under the MIT License. See LICENSE for more information.
