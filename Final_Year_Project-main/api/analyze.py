import json
import joblib
import os
from http.server import BaseHTTPRequestHandler

# Load models
models_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vectorizer = joblib.load(os.path.join(models_dir, 'vectorizer.jb'))
model = joblib.load(os.path.join(models_dir, 'lr_model.jb'))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/analyze':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            text = data.get('text', '')
            
            if not text or len(text.strip()) < 10:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Text too short'}).encode())
                return
            
            try:
                # Vectorize and predict
                vectorized = vectorizer.transform([text])
                prediction = model.predict(vectorized)[0]
                confidence = max(model.predict_proba(vectorized)[0])
                
                result = 'real' if prediction == 1 else 'fake'
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'result': result,
                    'confidence': float(confidence),
                    'prediction': int(prediction)
                }
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
