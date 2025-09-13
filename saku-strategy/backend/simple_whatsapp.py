#!/usr/bin/env python
"""
Simple WhatsApp API using a free service
"""
import requests
import json

def send_whatsapp_message(phone_number, message):
    """Send WhatsApp message using a free API service"""
    
    # Using a free WhatsApp API service
    url = "https://api.whatsapp.com/send"
    
    # Format the message
    clean_phone = phone_number.replace('+', '')
    clean_message = message.replace(' ', '%20').replace('\n', '%0A')
    formatted_message = f"https://wa.me/{clean_phone}?text={clean_message}"
    
    print(f"📱 WhatsApp Message Link:")
    print(f"🔗 {formatted_message}")
    print()
    print("📋 Instructions:")
    print("1. Click the link above")
    print("2. It will open WhatsApp Web/App")
    print("3. The message will be pre-filled")
    print("4. Click send")
    print()
    print("💡 This is a quick solution while we set up the API!")
    
    return formatted_message

def test_simple_whatsapp():
    """Test the simple WhatsApp method"""
    print("🧪 Simple WhatsApp Test")
    print("=" * 50)
    
    phone_number = "+254769582779"
    message = '"KCU/2023/TEST001" has registered for "Chair" in the SAKU council. Kindly verify them.\n\nhttp://localhost:5173/admin-dashboard-enhanced.html'
    
    send_whatsapp_message(phone_number, message)

if __name__ == '__main__':
    test_simple_whatsapp()
