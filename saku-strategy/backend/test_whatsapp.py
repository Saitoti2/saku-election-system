#!/usr/bin/env python
"""
Test script for WhatsApp integration
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from elections.whatsapp_service import WhatsAppService

def test_whatsapp_integration():
    """Test WhatsApp notification system"""
    
    print("🧪 Testing WhatsApp Integration")
    print("=" * 50)
    
    # Initialize WhatsApp service
    whatsapp_service = WhatsAppService()
    
    # Test data
    admin_phone = '+254769582779'  # Your WhatsApp number
    student_name = 'John Test Student'
    reg_number = 'KCU/2023/TEST001'
    user_type = 'ASPIRANT'
    position = 'CHAIR'
    
    print(f"📱 Admin Phone: {admin_phone}")
    print(f"👤 Student: {student_name}")
    print(f"📋 Registration: {reg_number}")
    print(f"🎯 Type: {user_type}")
    print(f"🏆 Position: {position}")
    print()
    
    # Test the notification
    print("🚀 Sending test notification...")
    try:
        result = whatsapp_service.send_admin_registration_alert(
            admin_phone=admin_phone,
            student_name=student_name,
            reg_number=reg_number,
            user_type=user_type,
            position=position
        )
        
        if result:
            print("✅ Notification sent successfully!")
            print("📱 Check your WhatsApp for the message")
        else:
            print("❌ Notification failed to send")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("=" * 50)
    print("📋 Next Steps:")
    print("1. Check your WhatsApp for the test message")
    print("2. If no message received, check API credentials")
    print("3. Verify your phone number format (+254769582779)")
    print("4. Check the setup guide: WHATSAPP_SETUP_GUIDE.md")

if __name__ == '__main__':
    test_whatsapp_integration()
