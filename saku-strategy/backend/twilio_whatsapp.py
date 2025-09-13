#!/usr/bin/env python
"""
Simple Twilio WhatsApp integration for SAKU
"""
import os
import requests
from django.conf import settings

class TwilioWhatsApp:
    """Simple Twilio WhatsApp service"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', '+14155238886')
        self.admin_phone = getattr(settings, 'ADMIN_PHONE_NUMBER', '+254769582779')
    
    def send_message(self, to_number: str, message: str) -> bool:
        """Send WhatsApp message via Twilio"""
        
        if not self.account_sid or not self.auth_token:
            print("❌ Twilio credentials not configured")
            print("📱 Message would be sent to:", to_number)
            print("💬 Message:", message)
            return False
        
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
        
        data = {
            'From': f'whatsapp:{self.whatsapp_number}',
            'To': f'whatsapp:{to_number}',
            'Body': message
        }
        
        try:
            response = requests.post(url, data=data, auth=(self.account_sid, self.auth_token))
            
            if response.status_code == 201:
                print("✅ WhatsApp message sent successfully!")
                return True
            else:
                print(f"❌ Failed to send message: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def send_admin_registration_alert(self, student_name: str, reg_number: str, user_type: str, position: str = None) -> bool:
        """Send admin notification about new registration"""
        
        user_type_display = {
            'ASPIRANT': 'SAKU Council Aspirant',
            'DELEGATE': 'Delegate',
            'IECK': 'IECK Member',
            'STUDENT': 'Student'
        }.get(user_type, user_type)
        
        message = f"""🚨 NEW SAKU REGISTRATION ALERT!

📝 Student Details:
• Name: {student_name}
• Registration Number: {reg_number}
• Registration Type: {user_type_display}"""
        
        if position:
            position_display = {
                'CHAIR': 'Chair (President)',
                'VICE_CHAIR': 'Vice Chair',
                'SECRETARY_GENERAL': 'Secretary General',
                'FINANCE_SECRETARY': 'Finance Secretary',
                'ACADEMIC_SECRETARY': 'Academic Secretary',
                'SPORTS_SECRETARY': 'Sports Secretary',
                'SPECIAL_INTERESTS_SECRETARY': 'Special Interests Secretary'
            }.get(position, position)
            message += f"\n• Position: {position_display}"
        
        message += f"""

🔗 Admin Dashboard: http://localhost:5173/admin-dashboard-enhanced.html

⏰ Please review and verify the student's documents as soon as possible.

- SAKU Election System"""
        
        return self.send_message(self.admin_phone, message)

# Test function
def test_twilio_whatsapp():
    """Test Twilio WhatsApp integration"""
    print("🧪 Testing Twilio WhatsApp Integration")
    print("=" * 50)
    
    twilio = TwilioWhatsApp()
    
    print(f"📱 Admin Phone: {twilio.admin_phone}")
    print(f"🔧 Account SID: {'✅ Set' if twilio.account_sid else '❌ Not Set'}")
    print(f"🔑 Auth Token: {'✅ Set' if twilio.auth_token else '❌ Not Set'}")
    print(f"📞 WhatsApp Number: {twilio.whatsapp_number}")
    print()
    
    # Test sending a message
    result = twilio.send_admin_registration_alert(
        student_name="John Test Student",
        reg_number="KCU/2023/TEST001",
        user_type="ASPIRANT",
        position="CHAIR"
    )
    
    if result:
        print("✅ Test message sent successfully!")
    else:
        print("❌ Test message failed")
        print("\n📋 To fix this:")
        print("1. Sign up for Twilio: https://console.twilio.com/")
        print("2. Get your Account SID and Auth Token")
        print("3. Create a .env file with:")
        print("   TWILIO_ACCOUNT_SID=your_account_sid")
        print("   TWILIO_AUTH_TOKEN=your_auth_token")

if __name__ == '__main__':
    test_twilio_whatsapp()
