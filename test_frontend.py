"""
Test script to verify the frontend form works by checking the webpage content
"""

import requests
from bs4 import BeautifulSoup

def test_frontend_form():
    print("🎨 Testing Frontend UI...")
    print("=" * 50)
    
    try:
        # Test that the main page loads
        print("1. Testing main page loads...")
        response = requests.get("http://127.0.0.1:5001/", timeout=5)
        
        if response.status_code == 200:
            print("   ✅ Main page loads successfully")
            
            # Check if form elements exist
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for Create Deal button
            create_btn = soup.find('button', {'onclick': 'showCreateDealForm()'})
            if create_btn:
                print("   ✅ 'Create New Deal' button found")
            else:
                print("   ❌ 'Create New Deal' button not found")
            
            # Check for form elements
            deal_form = soup.find('form', {'id': 'dealForm'})
            if deal_form:
                print("   ✅ Deal creation form found")
                
                # Check for required form fields
                required_fields = ['supplierId', 'item', 'unit', 'price', 'target_quantity', 'location']
                for field in required_fields:
                    field_element = soup.find(['input', 'select'], {'name': field})
                    if field_element:
                        print(f"   ✅ Field '{field}' found")
                    else:
                        print(f"   ❌ Field '{field}' missing")
            else:
                print("   ❌ Deal creation form not found")
            
            # Check for JavaScript
            js_script = soup.find('script', {'src': lambda x: x and 'app.js' in x})
            if js_script:
                print("   ✅ JavaScript file linked")
            else:
                print("   ❌ JavaScript file not linked")
            
            # Check for CSS
            css_link = soup.find('link', {'href': lambda x: x and 'style.css' in x})
            if css_link:
                print("   ✅ CSS file linked")
            else:
                print("   ❌ CSS file not linked")
                
        else:
            print(f"   ❌ Failed to load page: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to Flask server. Make sure it's running on port 5001")
        return
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    print("2. Manual testing instructions:")
    print("   • Open http://127.0.0.1:5001 in your browser")
    print("   • Click 'Create New Deal' button")
    print("   • Fill out the form with:")
    print("     - Supplier: Reliable Veggies")
    print("     - Item: Test Carrots")
    print("     - Unit: kg")
    print("     - Price: 20")
    print("     - Target Quantity: 80")
    print("     - Location: Jayanagar, Bangalore")
    print("   • Click 'Create Deal' and check for success message")
    
    print()
    print("✅ Frontend UI test completed!")

if __name__ == "__main__":
    test_frontend_form()
