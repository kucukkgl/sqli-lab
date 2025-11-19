

1. **Clone the lab repository**  
   ```bash
   git clone https://github.com/kucukkgl/sqli-lab.git
   cd sqli-lab
   ```

2. **Create and activate a virtual environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**  
   ```bash
   python3 initialize_db.py
   ```

5. **Run the app**  
   ```bash
   python3 app.py
   ```

6. **Visit the login page**  
   - Open a browser inside the same VM.  
   - Navigate to: [http://localhost:5000/login](http://localhost:5000/login)
