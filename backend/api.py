from flask import Flask, request, jsonify
from storage.database import Database

app = Flask(__name__)
db = Database()

@app.route('/api/events', methods=['POST'])
def receive_event():
    """Receive and store detection events"""
    try:
        event = request.get_json()
        
        # Validate event structure
        required_fields = ['timestamp', 'event_type', 'value']
        if not all(field in event for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Store event in database
        db.insert_event(event)
        
        return jsonify({'status': 'success', 'message': 'Event received'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Retrieve recent events"""
    try:
        limit = request.args.get('limit', 10, type=int)
        events = db.get_recent_events(limit)
        
        events_list = [
            {
                'id': e[0],
                'timestamp': e[1],
                'event_type': e[2],
                'value': e[3]
            }
            for e in events
        ]
        
        return jsonify({'events': events_list}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_api():
    """Start Flask API server"""
    print("Starting Flask API on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)