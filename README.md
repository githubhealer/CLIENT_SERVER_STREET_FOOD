# Group-Buying Web Application

A web application that empowers street food vendors to create and join bulk purchasing deals.

## Features Implemented ✅

### Supplier Features
- ✅ Create new deals with full validation
- ✅ Set item details, pricing, and target quantities
- ✅ Automatic deal ID generation and expiry tracking

### Vendor Features  
- ✅ View all active deals with beautiful card layout
- ✅ Filter deals by location
- ✅ See real-time progress and remaining quantities
- ✅ Visual progress bars and expiry warnings

### Backend API
- ✅ POST `/api/deals` - Create new deals
- ✅ GET `/api/deals` - Fetch deals with filtering
- ✅ Complete validation and error handling
- ✅ Database abstraction layer

### Frontend UI
- ✅ Responsive design for mobile and desktop
- ✅ Interactive forms with real-time validation
- ✅ Beautiful card-based deal display
- ✅ Location filtering and refresh functionality

## Setup Instructions

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open browser and go to: `http://127.0.0.1:5001`

## Testing

- **Database**: `python test_database.py`
- **Create Deal API**: `python test_create_deal.py`
- **Get Deals API**: `python test_get_deals.py`
- **Frontend**: Open browser and test UI interactions

## Tech Stack
- **Backend**: Python Flask with JSON database
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: JSON file (easy to migrate to real DB later)
- **Testing**: Comprehensive test scripts

## Project Structure
```
├── app.py                 # Main Flask application
├── database.py           # Database abstraction layer
├── database.json         # JSON database with sample data
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/style.css     # Responsive styling
│   └── js/app.js         # Frontend JavaScript
└── test_*.py             # Test scripts
```

## Next Steps (Planned)
- Vendor join deal functionality
- Real-time updates with WebSockets
- User authentication
- Database migration to PostgreSQL/MongoDB

---
🎯 **Hackathon Project**: Street Food Vendor Group-Buying Platform
