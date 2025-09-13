#!/usr/bin/env python
"""
Simple script to help you add your Twilio credentials
"""
import os

def setup_twilio_credentials():
    """Interactive setup for Twilio credentials"""
    
    print("🔧 Twilio WhatsApp Setup")
    print("=" * 50)
    print("📱 Your WhatsApp Number: +254769582779")
    print()
    
    print("📋 Step 1: Get your Twilio credentials")
    print("1. Go to: https://console.twilio.com/")
    print("2. Sign up and verify your phone number")
    print("3. Go to: Develop → Messaging → Try it out → Send a WhatsApp message")
    print("4. Follow the sandbox setup")
    print("5. Get your Account SID and Auth Token")
    print()
    
    # Get credentials from user
    account_sid = input("Enter your Twilio Account SID (starts with AC...): ").strip()
    auth_token = input("Enter your Twilio Auth Token: ").strip()
    
    if not account_sid or not auth_token:
        print("❌ Credentials cannot be empty!")
        return
    
    # Create .env file
    env_content = f"""# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID={account_sid}
TWILIO_AUTH_TOKEN={auth_token}
TWILIO_WHATSAPP_NUMBER=+14155238886
ADMIN_PHONE_NUMBER=+254769582779
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Credentials saved to .env file!")
        print()
        print("🧪 Testing your setup...")
        
        # Test the setup
        os.environ['TWILIO_ACCOUNT_SID'] = account_sid
        os.environ['TWILIO_AUTH_TOKEN'] = auth_token
        
        # Import and test
        import sys
        sys.path.append('.')
        
        from twilio_whatsapp import test_twilio_whatsapp
        test_twilio_whatsapp()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please create the .env file manually with your credentials")

if __name__ == '__main__':
    setup_twilio_credentials()
