"""
WhatsApp notification service for SAKU election platform
"""
import requests
import json
from django.conf import settings
from typing import Optional


class WhatsAppService:
    """Service for sending WhatsApp notifications"""
    
    def __init__(self):
        # Meta Business API configuration
        self.api_url = getattr(settings, 'WHATSAPP_API_URL', '')
        self.api_token = getattr(settings, 'WHATSAPP_API_TOKEN', '')
        self.phone_number_id = getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', '')
        
        # Twilio configuration
        self.twilio_account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
        self.twilio_auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
        self.twilio_whatsapp_number = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', '+14155238886')
    
    def send_qualification_notification(self, phone_number: str, full_name: str, position: str = None) -> bool:
        """
        Send WhatsApp notification to qualified candidate
        
        Args:
            phone_number: Recipient's phone number (with country code)
            full_name: Candidate's full name
            position: Council position they're running for (if aspirant)
        
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.api_url or not self.api_token:
            print("WhatsApp API not configured. Skipping notification.")
            return False
        
        # Format phone number (remove any non-digit characters except +)
        formatted_number = ''.join(filter(lambda x: x.isdigit() or x == '+', phone_number))
        if not formatted_number.startswith('+'):
            formatted_number = '+254' + formatted_number.lstrip('0')  # Default to Kenya
        
        # Create message content
        if position:
            message = f"""🎉 Congratulations {full_name}!

You have been QUALIFIED to run for the position of {position} in the SAKU Council Elections!

Your application has been reviewed and approved. You can now proceed with your campaign.

Good luck! 🏆

- SAKU Electoral Commission"""
        else:
            message = f"""🎉 Congratulations {full_name}!

You have been QUALIFIED for the SAKU Elections!

Your application has been reviewed and approved. You can now proceed with your participation.

Good luck! 🏆

- SAKU Electoral Commission"""
        
        # Send message via WhatsApp API
        return self._send_message(formatted_number, message)
    
    def _send_twilio_message(self, phone_number: str, message: str) -> bool:
        """Send WhatsApp message via Twilio"""
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Messages.json"
            
            data = {
                'From': f'whatsapp:{self.twilio_whatsapp_number}',
                'To': f'whatsapp:{phone_number}',
                'Body': message
            }
            
            response = requests.post(url, data=data, auth=(self.twilio_account_sid, self.twilio_auth_token))
            
            if response.status_code == 201:
                print("✅ WhatsApp message sent via Twilio!")
                return True
            else:
                print(f"❌ Twilio API error: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Twilio error: {e}")
            return False
    
    def _send_whatsapp_link(self, phone_number: str, message: str) -> bool:
        """Send WhatsApp message using free WhatsApp link method"""
        try:
            # Format the phone number (remove + and any spaces)
            clean_phone = phone_number.replace('+', '').replace(' ', '')
            
            # Format the message for URL
            clean_message = message.replace(' ', '%20').replace('\n', '%0A').replace('"', '%22')
            
            # Create WhatsApp link
            whatsapp_link = f"https://wa.me/{clean_phone}?text={clean_message}"
            
            print("📱 WhatsApp Message Link Generated:")
            print(f"🔗 {whatsapp_link}")
            print()
            print("📋 Instructions:")
            print("1. Click the link above to open WhatsApp")
            print("2. The message will be pre-filled")
            print("3. Click send to deliver the message")
            print("4. This is a free method that works immediately!")
            print()
            
            # In a real implementation, you could:
            # 1. Open the link automatically
            # 2. Send it via email to admin
            # 3. Log it for manual sending
            
            return True
            
        except Exception as e:
            print(f"❌ WhatsApp link error: {e}")
            return False
    
    def send_admin_registration_alert(self, admin_phone: str, student_name: str, reg_number: str, user_type: str, position: str = None) -> bool:
        """
        Send WhatsApp notification to admin when a new student registers
        
        Args:
            admin_phone: Admin's phone number (with country code)
            student_name: Student's full name
            reg_number: Student's registration number
            user_type: Type of registration (ASPIRANT, DELEGATE, IECK)
            position: Council position (if aspirant)
        
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        # For development/testing, always show the notification message
        print("=" * 60)
        print("🚨 NEW SAKU REGISTRATION ALERT!")
        print("=" * 60)
        
        # Create message content in your exact format
        position_display = {
            'CHAIR': 'Chair',
            'VICE_CHAIR': 'Vice Chair', 
            'SECRETARY_GENERAL': 'Secretary General',
            'FINANCE_SECRETARY': 'Finance Secretary',
            'ACADEMIC_SECRETARY': 'Academic Secretary',
            'SPORTS_SECRETARY': 'Sports Secretary',
            'SPECIAL_INTERESTS_SECRETARY': 'Special Interests Secretary'
        }.get(position, position) if position else user_type
        
        # Admin dashboard URL (configurable)
        admin_url = getattr(settings, 'ADMIN_DASHBOARD_URL', 'http://localhost:5173/admin-dashboard-enhanced.html')
        
        # Your exact message format
        message = f'"{reg_number}" has registered for "{position_display}" in the SAKU council. Kindly verify them.\n\n{admin_url}'
        
        print("=" * 60)
        print("📱 WhatsApp Message:")
        print(message)
        print("=" * 60)
        
        # Format admin phone number
        formatted_number = ''.join(filter(lambda x: x.isdigit() or x == '+', admin_phone))
        if not formatted_number.startswith('+'):
            formatted_number = '+254' + formatted_number.lstrip('0')
        
        # Use free WhatsApp link method
        return self._send_whatsapp_link(formatted_number, message)
    
    def send_rejection_notification(self, phone_number: str, full_name: str, reason: str = None) -> bool:
        """
        Send WhatsApp notification to rejected candidate
        
        Args:
            phone_number: Recipient's phone number (with country code)
            full_name: Candidate's full name
            reason: Reason for rejection (optional)
        
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.api_url or not self.api_token:
            print("WhatsApp API not configured. Skipping notification.")
            return False
        
        # Format phone number
        formatted_number = ''.join(filter(lambda x: x.isdigit() or x == '+', phone_number))
        if not formatted_number.startswith('+'):
            formatted_number = '+254' + formatted_number.lstrip('0')
        
        # Create message content
        message = f"""Dear {full_name},

Thank you for your interest in participating in the SAKU Council Elections.

Unfortunately, your application has not been approved at this time."""
        
        if reason:
            message += f"\n\nReason: {reason}"
        
        message += """

You may reapply in future elections if you meet the requirements.

Best regards,
SAKU Electoral Commission"""
        
        return self._send_message(formatted_number, message)
    
    def _send_message(self, phone_number: str, message: str) -> bool:
        """
        Send message via WhatsApp Business API
        
        Args:
            phone_number: Recipient's phone number
            message: Message content
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'messaging_product': 'whatsapp',
                'to': phone_number,
                'type': 'text',
                'text': {
                    'body': message
                }
            }
            
            url = f"{self.api_url}/{self.phone_number_id}/messages"
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"WhatsApp message sent successfully to {phone_number}")
                return True
            else:
                print(f"Failed to send WhatsApp message: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            return False


# Global instance
whatsapp_service = WhatsAppService()
