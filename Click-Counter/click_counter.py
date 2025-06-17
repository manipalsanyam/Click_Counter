from flask import Flask, jsonify, render_template_string, request
import os
import json

app = Flask(__name__)


COUNT_FILE = 'click_count.json'

def load_count():
    """Load the current count from file"""
    if os.path.exists(COUNT_FILE):
        try:
            with open(COUNT_FILE, 'r') as f:
                data = json.load(f)
                return data.get('count', 0)
        except (json.JSONDecodeError, FileNotFoundError):
            return 0
    return 0

def save_count(count):
    """Save the current count to file"""
    with open(COUNT_FILE, 'w') as f:
        json.dump({'count': count}, f)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Click Counter</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            text-align: center;
            min-width: 300px;
        }
        
        h1 {
            color: white;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .count-display {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .count-number {
            font-size: 3em;
            font-weight: bold;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin: 0;
        }
        
        .count-label {
            color: rgba(255, 255, 255, 0.8);
            font-size: 1.1em;
            margin-top: 10px;
        }
        
        .click-button {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            border: none;
            color: white;
            font-size: 1.5em;
            font-weight: bold;
            padding: 15px 30px;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
            margin: 20px 10px;
        }
        
        .click-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
        }
        
        .click-button:active {
            transform: translateY(0);
            box-shadow: 0 2px 10px rgba(255, 107, 107, 0.4);
        }
        
        .reset-button {
            background: linear-gradient(45deg, #74b9ff, #0984e3);
            border: none;
            color: white;
            font-size: 1em;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(116, 185, 255, 0.4);
            margin: 10px;
        }
        
        .reset-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(116, 185, 255, 0.6);
        }
        
        .loading {
            opacity: 0.6;
            pointer-events: none;
        }
        
        .error {
            color: #ff6b6b;
            background: rgba(255, 107, 107, 0.1);
            border: 1px solid rgba(255, 107, 107, 0.3);
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1> Click Counter</h1>
        
        <div class="count-display">
            <div class="count-number" id="countDisplay">{{ count }}</div>
            <div class="count-label">Total Clicks</div>
        </div>
        
        <button class="click-button" id="clickButton" onclick="incrementCount()">
            Click Me! 
        </button>
        
        <br>
        
        <button class="reset-button" id="resetButton" onclick="resetCount()">
            Reset Counter 
        </button>
        
        <div id="errorMessage" class="error" style="display: none;"></div>
    </div>

    <script>
        let currentCount = {{ count }};
        
        async function incrementCount() {
            const button = document.getElementById('clickButton');
            const display = document.getElementById('countDisplay');
            const container = document.querySelector('.container');
            
            // Add loading state
            container.classList.add('loading');
            
            try {
                const response = await fetch('/increment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                
                const data = await response.json();
                currentCount = data.count;
                display.textContent = currentCount;
                
                // Add a little animation
                display.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    display.style.transform = 'scale(1)';
                }, 150);
                
                hideError();
                
            } catch (error) {
                console.error('Error:', error);
                showError('Failed to update count. Please try again.');
            } finally {
                container.classList.remove('loading');
            }
        }
        
        async function resetCount() {
            const display = document.getElementById('countDisplay');
            const container = document.querySelector('.container');
            
            if (!confirm('Are you sure you want to reset the counter to 0?')) {
                return;
            }
            
            container.classList.add('loading');
            
            try {
                const response = await fetch('/reset', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                
                const data = await response.json();
                currentCount = data.count;
                display.textContent = currentCount;
                
                hideError();
                
            } catch (error) {
                console.error('Error:', error);
                showError('Failed to reset count. Please try again.');
            } finally {
                container.classList.remove('loading');
            }
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
        
        function hideError() {
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.style.display = 'none';
        }
        
        // Add CSS transition for smooth scaling
        document.getElementById('countDisplay').style.transition = 'transform 0.15s ease';
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main page"""
    count = load_count()
    return render_template_string(HTML_TEMPLATE, count=count)

@app.route('/increment', methods=['POST'])
def increment():
    """Increment the click counter"""
    try:
        current_count = load_count()
        new_count = current_count + 1
        save_count(new_count)
        return jsonify({'count': new_count, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the click counter to 0"""
    try:
        save_count(0)
        return jsonify({'count': 0, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/count', methods=['GET'])
def get_count():
    """Get the current count (API endpoint)"""
    try:
        count = load_count()
        return jsonify({'count': count, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
   
    if not os.path.exists(COUNT_FILE):
        save_count(0)
    
    print("🚀 Starting Click Counter Server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)