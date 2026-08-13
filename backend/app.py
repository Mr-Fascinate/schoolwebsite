# pyrefly: ignore [missing-import]
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from models import db, User, Page, Alert, News, Event, Setting
import json
import time
import base64
import hmac
import hashlib
import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for frontend requests
CORS(app, resources={r"/api/*": {"origins": "*"}})

db.init_app(app)

# Helper functions for Custom JWT implementation (zero dependencies)
def generate_token(username, secret_key):
    payload = {
        'sub': username,
        'exp': int(time.time()) + 86400  # Valid for 24 hours
    }
    payload_json = json.dumps(payload)
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode().rstrip('=')
    signature = hmac.new(secret_key.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{signature}"

def verify_token(token, secret_key):
    try:
        parts = token.split('.')
        if len(parts) != 2:
            return None
        payload_b64, signature = parts
        expected_sig = hmac.new(secret_key.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return None
        
        # Add back padding if needed
        padding_needed = len(payload_b64) % 4
        if padding_needed:
            payload_b64 += '=' * (4 - padding_needed)
        payload_str = base64.urlsafe_b64decode(payload_b64.encode()).decode()
        payload = json.loads(payload_str)
        
        if payload.get('exp', 0) < time.time():
            return None
        return payload.get('sub')
    except Exception:
        return None

# JWT authentication decorator
def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Authorization token is missing!'}), 401
        
        username = verify_token(token, app.config['JWT_SECRET_KEY'])
        if not username:
            return jsonify({'message': 'Token is invalid or expired!'}), 401
            
        return f(*args, **kwargs)
    return decorated


# ==========================================
# AUTH ENDPOINTS
# ==========================================
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = generate_token(username, app.config['JWT_SECRET_KEY'])
        return jsonify({'token': token, 'username': username}), 200

    return jsonify({'message': 'Invalid username or password'}), 401


# ==========================================
# PAGE CRUD ENDPOINTS (ADMIN)
# ==========================================
@app.route('/api/pages', methods=['GET'])
@token_required
def get_pages():
    pages = Page.query.order_by(Page.created_at.desc()).all()
    return jsonify([p.to_dict() for p in pages]), 200

@app.route('/api/pages', methods=['POST'])
@token_required
def create_page():
    data = request.get_json() or {}
    title = data.get('title')
    slug = data.get('slug')
    parent_id = data.get('parent_id')
    schema = data.get('schema', [])

    if not title or not slug:
        return jsonify({'message': 'Title and Slug are required'}), 400

    # Sanitize slug
    slug = slug.strip().lower().replace(' ', '-')
    
    # Check if slug exists
    if Page.query.filter_by(slug=slug).first():
        return jsonify({'message': 'Slug already exists'}), 400

    page = Page(
        title=title,
        slug=slug,
        parent_id=parent_id,
        schema_json=json.dumps(schema)
    )
    db.session.add(page)
    db.session.commit()
    return jsonify(page.to_dict()), 201

@app.route('/api/pages/<int:page_id>', methods=['PUT'])
@token_required
def update_page(page_id):
    page = Page.query.get_or_404(page_id)
    data = request.get_json() or {}
    
    title = data.get('title')
    slug = data.get('slug')
    schema = data.get('schema')

    if title:
        page.title = title
    if slug:
        slug = slug.strip().lower().replace(' ', '-')
        existing = Page.query.filter_by(slug=slug).first()
        if existing and existing.id != page.id:
            return jsonify({'message': 'Slug already exists'}), 400
        page.slug = slug
    if 'parent_id' in data:
        page.parent_id = data.get('parent_id')
    if schema is not None:
        page.schema_json = json.dumps(schema)

    db.session.commit()
    return jsonify(page.to_dict()), 200

@app.route('/api/pages/<int:page_id>', methods=['DELETE'])
@token_required
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    return jsonify({'message': 'Page deleted successfully'}), 200


# ==========================================
# PUBLIC RENDER & PAGES METADATA ENDPOINTS
# ==========================================
@app.route('/api/public/pages', methods=['GET'])
def get_public_pages_list():
    pages = Page.query.order_by(Page.title.asc()).all()
    # Only return necessary metadata for menu navigation/drawer index
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'slug': p.slug,
        'parent_id': p.parent_id
    } for p in pages]), 200

@app.route('/api/public/pages/<slug>', methods=['GET'])
def get_public_page(slug):
    page = Page.query.filter_by(slug=slug).first()
    if not page:
        return jsonify({'message': 'Page not found'}), 404
    return jsonify(page.to_dict()), 200


# ==========================================
# SETTINGS/CONFIGURATION ENDPOINTS
# ==========================================
@app.route('/api/public/settings/<key>', methods=['GET'])
def get_public_setting(key):
    setting = Setting.query.get(key)
    if not setting:
        return jsonify({'message': 'Setting not found'}), 404
    return jsonify(setting.to_dict()), 200

@app.route('/api/settings/<key>', methods=['PUT'])
@token_required
def update_setting(key):
    data = request.get_json() or {}
    value_raw = data.get('value')
    if value_raw is None:
        return jsonify({'message': 'Value is required'}), 400

    setting = Setting.query.get(key)
    if not setting:
        setting = Setting(key=key)
        db.session.add(setting)

    setting.value = json.dumps(value_raw)
    db.session.commit()
    return jsonify(setting.to_dict()), 200


# ==========================================
# NOTIFICATION ALERTS ENDPOINTS
# ==========================================
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()
    return jsonify([a.to_dict() for a in alerts]), 200

@app.route('/api/alerts/active', methods=['GET'])
def get_active_alerts():
    # Return all active alerts
    alerts = Alert.query.filter_by(active=True).order_by(Alert.created_at.desc()).all()
    now = datetime.datetime.utcnow()
    valid_alerts = []
    mutated = False
    
    for alert in alerts:
        if alert.expires_at and alert.expires_at < now:
            alert.active = False
            mutated = True
        else:
            valid_alerts.append(alert.to_dict())
            
    if mutated:
        db.session.commit()

    return jsonify(valid_alerts), 200

@app.route('/api/alerts', methods=['POST'])
@token_required
def create_alert():
    data = request.get_json() or {}
    message = data.get('message')
    active = data.get('active', True)
    link_url = data.get('link_url')
    expires_in_hours = data.get('expires_in_hours')

    if not message:
        return jsonify({'message': 'Message is required'}), 400

    expires_at = None
    if expires_in_hours:
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=float(expires_in_hours))

    alert = Alert(
        message=message,
        active=active,
        link_url=link_url,
        expires_at=expires_at
    )
    db.session.add(alert)
    db.session.commit()
    return jsonify(alert.to_dict()), 201

@app.route('/api/alerts/<int:alert_id>', methods=['PUT'])
@token_required
def update_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    data = request.get_json() or {}
    
    active = data.get('active')
    message = data.get('message')
    link_url = data.get('link_url')

    if message:
        alert.message = message
    if active is not None:
        alert.active = active
    if link_url is not None:
        alert.link_url = link_url

    db.session.commit()
    return jsonify(alert.to_dict()), 200


# ==========================================
# NEWS ENDPOINTS
# ==========================================
@app.route('/api/news', methods=['GET'])
def get_news():
    news_list = News.query.order_by(News.date.desc()).all()
    return jsonify([n.to_dict() for n in news_list]), 200

@app.route('/api/news', methods=['POST'])
@token_required
def create_news():
    data = request.get_json() or {}
    title = data.get('title')
    content = data.get('content')
    image_url = data.get('image_url')

    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400

    news = News(title=title, content=content, image_url=image_url)
    db.session.add(news)
    db.session.commit()
    return jsonify(news.to_dict()), 201

@app.route('/api/news/<int:news_id>', methods=['DELETE'])
@token_required
def delete_news(news_id):
    news = News.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    return jsonify({'message': 'News article deleted successfully'}), 200


# ==========================================
# EVENTS ENDPOINTS
# ==========================================
@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.order_by(Event.date.asc()).all()
    return jsonify([e.to_dict() for e in events]), 200

@app.route('/api/events', methods=['POST'])
@token_required
def create_event():
    data = request.get_json() or {}
    title = data.get('title')
    description = data.get('description')
    location = data.get('location')
    date_str = data.get('date') # ISO string
    image_url = data.get('image_url')

    if not title or not description or not location or not date_str:
        return jsonify({'message': 'Title, description, location, and date are required'}), 400

    try:
        # Parse ISO date string
        # Support formats like '2026-06-15T21:00:00' or '2026-06-15'
        if 'T' in date_str:
            date_val = datetime.datetime.strptime(date_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        else:
            date_val = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        date_val = datetime.datetime.utcnow()

    event = Event(
        title=title,
        description=description,
        location=location,
        date=date_val,
        image_url=image_url
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
@token_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'}), 200


# ==========================================
# SEARCH ENDPOINT
# ==========================================
@app.route('/api/public/search', methods=['GET'])
def public_search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify({'results': []}), 200

    # Query Pages
    pages = Page.query.filter(
        (Page.title.ilike(f'%{q}%')) | 
        (Page.schema_json.ilike(f'%{q}%'))
    ).all()

    # Query News
    news = News.query.filter(
        (News.title.ilike(f'%{q}%')) | 
        (News.content.ilike(f'%{q}%'))
    ).all()

    # Query Events
    events = Event.query.filter(
        (Event.title.ilike(f'%{q}%')) | 
        (Event.description.ilike(f'%{q}%')) |
        (Event.location.ilike(f'%{q}%'))
    ).all()

    results = []

    for p in pages:
        results.append({
            'type': 'Page',
            'title': p.title,
            'description': f"Portal page content: {p.title}",
            'link': f"/{p.slug}"
        })

    for n in news:
        results.append({
            'type': 'News',
            'title': n.title,
            'description': n.content[:200] + '...' if len(n.content) > 200 else n.content,
            'link': n.link_url if n.link_url else "/updates"
        })

    for e in events:
        results.append({
            'type': 'Event',
            'title': e.title,
            'description': f"Location: {e.location} | {e.description[:150]}...",
            'link': e.link_url if e.link_url else "/events"
        })

    return jsonify({'results': results}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
