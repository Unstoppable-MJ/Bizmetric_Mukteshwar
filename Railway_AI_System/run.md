# Setup and Running Guide: Railway AI System

This guide provides step-by-step instructions to run the three main components of the Railway AI System: the Django REST API, the React Frontend, and the Machine Learning Prediction Service.

---

## 1. Backend REST API (Django)

The backend handles live train tracking by integrating with RapidAPI.

### Prerequisites
- Python 3.x installed.
- A valid RapidAPI Key for "Indian Railway Live Train Status".

### Steps
1. **Install Dependencies**:
   ```bash
   pip install django djangorestframework requests python-dotenv django-cors-headers
   ```
2. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   RAPIDAPI_KEY=your_actual_key_here
   RAPIDAPI_HOST=indian-railway-irctc.p.rapidapi.com
   ```
3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
4. **Start the Server**:
   ```bash
   python manage.py runserver
   ```
   *The API will be available at `http://127.0.0.1:8004/api/`*

---

## 2. Frontend (React + Vite)

The frontend provides a premium UI for interacting with the tracking system.

### Steps
1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```
2. **Install Dependencies**:
   ```bash
   npm install
   # If you encounter dependency conflicts, use:
   # npm install --legacy-peer-deps
   ```
3. **Start the Development Server**:
   ```bash
   npm run dev
   ```
   *The UI will be available at `http://localhost:5173/`*

---

## 3. Machine Learning Service (Flask)

The ML service provides delay predictions and estimated arrival times using Linear Regression and LSTM models.

### Steps
1. **Install ML Dependencies**:
   ```bash
   pip install pandas numpy scikit-learn tensorflow flask joblib
   ```
2. **(Optional) Retrain Models**:
   If you want to regenerate data and retrain:
   ```bash
   python ml_model/generate_data.py
   python ml_model/train.py
   ```
3. **Start the Flask API**:
   ```bash
   python ml_model/app.py
   ```
   *The Prediction API will be available at `http://127.0.0.1:5000/predict`*

---

## 4. Flutter Mobile Application (Android)

A Material UI mobile app for checking train status on the go.

### Prerequisites
- [Flutter SDK](https://docs.flutter.dev/get-started/install) installed.
- Android Studio / VS Code with Flutter extension.
- Android Emulator or a real device connected.

### Steps
1. **Navigate to Mobile App Directory**:
   ```bash
   cd mobile_app
   ```
2. **Fetch Dependencies**:
   ```bash
   flutter pub get
   ```
3. **Run the App**:
   ```bash
   flutter run
   ```
   *Note: Ensure the Django backend is running on port 8004. Use `10.0.2.2` for the Android emulator.*

> [!IMPORTANT]
> **Flutter Installation Required**: The `flutter` command is not available in this remote environment. You must download and install the [Flutter SDK](https://docs.flutter.dev/get-started/install) on your local computer to build and run the mobile application.

---

## Summary of Endpoints
- **Live Status (Django)**: `http://127.0.0.1:8004/api/train/<train_no>/`
- **Delay Prediction (Flask)**: `POST /predict` (JSON: `{"train_no": 12051, "current_delay": 15, "station_index": 5}`)

---
**Happy Tracking!**
