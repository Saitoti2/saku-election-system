#!/usr/bin/env python
"""
WhatsApp API Setup Helper Script
"""
import os
import sys

def setup_whatsapp_api():
    """Interactive setup for WhatsApp API"""
    
    print("📱 WhatsApp Business API Setup")
    print("=" * 50)
    print("Your WhatsApp Number: +254769582779")
    print()
    
    print("Choose your WhatsApp API provider:")
    print("1. Twilio (Recommended - Easy setup)")
    print("2. Meta Business (Free but complex)")
    print("3. MessageBird (Alternative)")
    print("4. Skip setup (Use console notifications only)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        setup_twilio()
    elif choice == "2":
        setup_meta_business()
    elif choice == "3":
        setup_messagebird()
    elif choice == "4":
        print("✅ Skipping setup. You'll see notifications in console only.")
    else:
        print("❌ Invalid choice. Please run the script again.")
    
    print("\n" + "=" * 50)
    print("📋 Next Steps:")
    print("1. Get your API credentials from your chosen provider")
    print("2. Create a .env file in the backend directory")
    print("3. Add your credentials to the .env file")
    print("4. Test with: python test_whatsapp.py")
    print("5. Check the setup guide: WHATSAPP_SETUP_GUIDE.md")

def setup_twilio():
    """Setup instructions for Twilio"""
    print("\n🔧 Twilio Setup Instructions:")
    print("1. Go to: https://console.twilio.com/")
    print("2. Sign up for a free account")
    print("3. Go to 'Develop' > 'Messaging' > 'Try it out' > 'Send a WhatsApp message'")
    print("4. Follow the sandbox setup instructions")
    print("5. Get your credentials:")
    print("   - Account SID")
    print("   - Auth Token")
    print("   - WhatsApp Sandbox Number (usually +14155238886)")
    print("\n📝 Add to your .env file:")
    print("TWILIO_ACCOUNT_SID=your_account_sid_here")
    print("TWILIO_AUTH_TOKEN=your_auth_token_here")
    print("TWILIO_WHATSAPP_NUMBER=+14155238886")

def setup_meta_business():
    """Setup instructions for Meta Business"""
    print("\n🔧 Meta Business Setup Instructions:")
    print("1. Go to: https://developers.facebook.com/")
    print("2. Create a Meta Business account")
    print("3. Create a new app and add WhatsApp Business API")
    print("4. Get your credentials:")
    print("   - Access Token")
    print("   - Phone Number ID")
    print("   - Business Account ID")
    print("\n📝 Add to your .env file:")
    print("WHATSAPP_API_URL=https://graph.facebook.com/v18.0")
    print("WHATSAPP_API_TOKEN=your_access_token_here")
    print("WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here")

def setup_messagebird():
    """Setup instructions for MessageBird"""
    print("\n🔧 MessageBird Setup Instructions:")
    print("1. Go to: https://www.messagebird.com/")
    print("2. Sign up for a free account")
    print("3. Enable WhatsApp API in your dashboard")
    print("4. Get your API key")
    print("\n📝 Add to your .env file:")
    print("MESSAGEBIRD_API_KEY=your_api_key_here")

if __name__ == '__main__':
    setup_whatsapp_api()
