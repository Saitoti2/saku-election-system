#!/usr/bin/env python
"""
Quick WhatsApp test - just enter your credentials and test
"""
import requests

def test_whatsapp():
    print("🧪 Quick WhatsApp Test")
    print("=" * 50)
    
    # Get credentials from user
    account_sid = input("Enter your Twilio Account SID (starts with AC...): ").strip()
    auth_token = input("Enter your Twilio Auth Token: ").strip()
    
    if not account_sid or not auth_token:
        print("❌ Credentials cannot be empty!")
        return
    
    # Test message
    message = '"KCU/2023/TEST001" has registered for "Chair" in the SAKU council. Kindly verify them.\n\nhttp://localhost:5173/admin-dashboard-enhanced.html'
    
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    
    data = {
        'From': 'whatsapp:+14155238886',  # Twilio sandbox number
        'To': 'whatsapp:+254769582779',   # Your WhatsApp number
        'Body': message
    }
    
    print(f"\n🚀 Sending test message...")
    print(f"📱 To: +254769582779")
    print(f"💬 Message: {message}")
    print()
    
    try:
        response = requests.post(url, data=data, auth=(account_sid, auth_token))
        
        if response.status_code == 201:
            print("✅ SUCCESS! WhatsApp message sent!")
            print("📱 Check your WhatsApp for the message")
            
            # Save credentials to .env file
            with open('.env', 'w') as f:
                f.write(f"TWILIO_ACCOUNT_SID={account_sid}\n")
                f.write(f"TWILIO_AUTH_TOKEN={auth_token}\n")
                f.write("TWILIO_WHATSAPP_NUMBER=+14155238886\n")
                f.write("ADMIN_PHONE_NUMBER=+254769582779\n")
            
            print("✅ Credentials saved to .env file!")
            print("🎉 Your WhatsApp API is now working!")
            
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_whatsapp()
