## Installation Steps

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
Create a `.env` file in your project directory:
```bash
GEMINI_API_KEY=your_api_key_here
```

### 5. Run the bug hunter
```bash
python client.py buggy.py
```