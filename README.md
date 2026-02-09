# CalmPal – Your Mental Health Chatbot 🧠🧘🏼‍♀️

### CalmPal is a web-based mental health support chatbot built to provide users with a safe and empathetic space to express their feelings. It listens without judgment, offers friendly responses, and helps users navigate through emotions, all through an engaging chat UI.
---

## 🚀 Live Demo
#### [CalmPal Live](https://calmpal.streamlit.app/)
---

## 🛠️ Tech Stack

| Layer        | Tech Used                     |
|--------------|-------------------------------|
| 👩‍🎨 Frontend   | HTML5, Tailwind CSS, JavaScript |
| 🔧 Backend    | Streamlit (Python)               |
| 🧠 AI Model   | Gemini / GPT-style responses via Google Generative AI API |

---

## ✨ Features

- 🤖 Friendly chatbot UI with real-time responses
- 🕐 Message timestamps like a real chat app
- 🔒 No data stored - user privacy by design
---

## 📁 Project Structure

```bash
CalmPal/
├── static/
│   ├── style.css             # Tailwind CSS styles
│   ├── script.js             # Frontend JS logic
├── templates/
│   ├── index.html            # Chat UI
├── app.py                    # Flask backend logic
├── .env                      # API Key config
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```
---
## ⚙️ Setup Instructions

### 1️⃣ Clone the repo

```bash
git clone https://github.com/yourusername/CalmPal.git
cd CalmPal
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Google API Key in '.env' file

```bash
=GOOGLE_API_KEY=your_api_key_here
```

### 5️⃣ Run the application

```bash
streamlit run app.py
```
---

## 🤖 AI Integration
### Google Generative AI (Gemini API) is used to simulate human-like, empathetic responses. You can replace this with OpenAI's GPT if needed by adjusting the backend logic in app.py.
---

## 📌 Future Enhancements
- 🗂️ Add conversation history export
- 🧠 Emotion analysis and mood tracking dashboard
- 🖼️ AI-generated motivational image suggestions
- 🧘‍♀️ Daily check-ins and meditation prompts
- 📱 PWA version for mobile use
---

## 🤝 Contributing
### Pull requests are welcome. Feel free to fork and improve this project.
---

## 🙌 Acknowledgements
Google Generative AI (Gemini)
