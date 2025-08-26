#!/usr/bin/env python3
"""
Zeldar Oracle Website API
Simple Flask API for fortune lookup by serial number

This API serves the Burning Man interactive oracle website,
allowing participants to look up their fortunes using serial numbers.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from pathlib import Path
from datetime import datetime
import sqlite3
import hashlib

app = Flask(__name__)
CORS(app)  # Enable CORS for web frontend

class OracleAPI:
    def __init__(self, session_log_file="burning_man_oracle_sessions.jsonl"):
        self.session_log_file = session_log_file
        self.db_file = "oracle_database.db"
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for fortune storage"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fortunes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_number TEXT UNIQUE NOT NULL,
                fortune_text TEXT NOT NULL,
                information-dynamics_phi REAL NOT NULL,
                element TEXT NOT NULL,
                fortune_type TEXT NOT NULL,
                session_id TEXT NOT NULL,
                timestamp REAL NOT NULL,
                datetime_str TEXT NOT NULL,
                photo_path TEXT,
                photo_url TEXT,
                voice_file TEXT,
                metadata TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def load_fortunes_from_log(self):
        """Load fortunes from JSONL log file into database"""
        if not Path(self.session_log_file).exists():
            return 0
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        loaded_count = 0
        
        try:
            with open(self.session_log_file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    
                    try:
                        session_data = json.loads(line)
                        
                        # Extract fortune data
                        serial_number = session_data.get('serial_number')
                        if not serial_number:
                            continue
                            
                        # Check if already exists
                        cursor.execute('SELECT id FROM fortunes WHERE serial_number = ?', (serial_number,))
                        if cursor.fetchone():
                            continue  # Skip duplicates
                        
                        # Determine fortune type from information-dynamics level
                        phi = session_data.get('information-dynamics_phi', 3.0)
                        if phi < 2.5:
                            fortune_type = 'seed'
                        elif phi < 3.5:
                            fortune_type = 'field'
                        else:
                            fortune_type = 'quantum'
                        
                        # Insert fortune
                        cursor.execute('''
                            INSERT INTO fortunes (
                                serial_number, fortune_text, information-dynamics_phi, element,
                                fortune_type, session_id, timestamp, datetime_str,
                                photo_path, photo_url, voice_file, metadata
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            serial_number,
                            session_data.get('fortune', ''),
                            phi,
                            session_data.get('element', 'UNKNOWN'),
                            fortune_type,
                            session_data.get('session_id', ''),
                            session_data.get('timestamp', 0),
                            session_data.get('datetime', ''),
                            session_data.get('photo_path'),
                            session_data.get('photo_url'),
                            session_data.get('voice_file'),
                            json.dumps(session_data.get('metadata', {}))
                        ))
                        
                        loaded_count += 1
                        
                    except json.JSONDecodeError as e:
                        print(f"Warning: Could not parse log line: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error loading fortunes: {e}")
        
        conn.commit()
        conn.close()
        
        return loaded_count
    
    def get_fortune_by_serial(self, serial_number):
        """Retrieve fortune by serial number"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT serial_number, fortune_text, information-dynamics_phi, element,
                   fortune_type, session_id, timestamp, datetime_str,
                   photo_url, voice_file, metadata
            FROM fortunes
            WHERE serial_number = ?
        ''', (serial_number.upper(),))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
        
        # Convert to dictionary
        fortune_data = {
            'serial_number': result[0],
            'fortune': result[1],
            'information-dynamics_phi': result[2],
            'element': result[3],
            'fortune_type': result[4],
            'session_id': result[5],
            'timestamp': result[6],
            'datetime': result[7],
            'photo_url': result[8],
            'voice_file': result[9],
            'metadata': json.loads(result[10]) if result[10] else {}
        }
        
        return fortune_data
    
    def get_all_fortunes(self, limit=100):
        """Get all fortunes (for admin/analytics)"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT serial_number, fortune_text, information-dynamics_phi, element,
                   fortune_type, session_id, datetime_str
            FROM fortunes
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        fortunes = []
        for row in results:
            fortunes.append({
                'serial_number': row[0],
                'fortune': row[1],
                'information-dynamics_phi': row[2],
                'element': row[3],
                'fortune_type': row[4],
                'session_id': row[5],
                'datetime': row[6]
            })
        
        return fortunes
    
    def get_statistics(self):
        """Get oracle statistics"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Total count
        cursor.execute('SELECT COUNT(*) FROM fortunes')
        total_count = cursor.fetchone()[0]
        
        # InformationForce stats
        cursor.execute('SELECT MIN(information-dynamics_phi), MAX(information-dynamics_phi), AVG(information-dynamics_phi) FROM fortunes')
        phi_stats = cursor.fetchone()
        
        # Fortune type distribution
        cursor.execute('SELECT fortune_type, COUNT(*) FROM fortunes GROUP BY fortune_type')
        type_dist = dict(cursor.fetchall())
        
        # Element distribution
        cursor.execute('SELECT element, COUNT(*) FROM fortunes GROUP BY element')
        element_dist = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_fortunes': total_count,
            'information-dynamics_range': {
                'min': phi_stats[0] or 0,
                'max': phi_stats[1] or 0,
                'average': phi_stats[2] or 0
            },
            'fortune_type_distribution': type_dist,
            'element_distribution': element_dist,
            'last_updated': datetime.now().isoformat()
        }

# Initialize API
oracle_api = OracleAPI()

# Routes
@app.route('/')
def serve_website():
    """Serve the main website"""
    return send_from_directory('.', 'index.html')

@app.route('/api/fortune/<serial_number>')
def get_fortune(serial_number):
    """API endpoint to get fortune by serial number"""
    
    # Reload fortunes from log file (in case new ones were added)
    oracle_api.load_fortunes_from_log()
    
    fortune = oracle_api.get_fortune_by_serial(serial_number)
    
    if not fortune:
        return jsonify({
            'error': 'Fortune not found',
            'message': f'No fortune found with serial number {serial_number.upper()}'
        }), 404
    
    return jsonify({
        'success': True,
        'fortune': fortune
    })

@app.route('/api/fortunes')
def get_all_fortunes():
    """API endpoint to get all fortunes (for admin)"""
    limit = request.args.get('limit', 100, type=int)
    fortunes = oracle_api.get_all_fortunes(limit)
    
    return jsonify({
        'success': True,
        'fortunes': fortunes,
        'count': len(fortunes)
    })

@app.route('/api/stats')
def get_statistics():
    """API endpoint to get oracle statistics"""
    stats = oracle_api.get_statistics()
    
    return jsonify({
        'success': True,
        'statistics': stats
    })

@app.route('/api/sync')
def sync_fortunes():
    """API endpoint to sync fortunes from log file"""
    loaded_count = oracle_api.load_fortunes_from_log()
    
    return jsonify({
        'success': True,
        'message': f'Loaded {loaded_count} new fortunes from log file',
        'loaded_count': loaded_count
    })

@app.route('/fortune/<serial_number>')
def fortune_lookup_page(serial_number):
    """Direct fortune lookup URL"""
    # This could serve a customized page with the fortune pre-loaded
    return serve_website()

if __name__ == '__main__':
    # Load existing fortunes on startup
    print("🔮 Starting Zeldar Oracle API...")
    loaded = oracle_api.load_fortunes_from_log()
    print(f"📚 Loaded {loaded} fortunes from session log")
    
    # Get current stats
    stats = oracle_api.get_statistics()
    print(f"📊 Total fortunes in database: {stats['total_fortunes']}")
    
    # Start server
    print("🌐 Starting web server on http://localhost:5000")
    print("🔗 API endpoints:")
    print("   GET /api/fortune/<serial>     - Get fortune by serial number")
    print("   GET /api/fortunes             - Get all fortunes (admin)")
    print("   GET /api/stats                - Get statistics")
    print("   GET /api/sync                 - Sync from log file")
    
    app.run(debug=True, host='0.0.0.0', port=5000)