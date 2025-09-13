# 📱 WhatsApp Business API Integration Guide

## 🎯 **Your WhatsApp Number: +254769582779**

## **Step 1: Choose Your WhatsApp API Provider**

### **Option A: Meta Business (Free but Complex)**
1. **Go to:** [Meta for Developers](https://developers.facebook.com/)
2. **Create account** and verify your business
3. **Set up WhatsApp Business API**
4. **Get credentials:**
   - Access Token
   - Phone Number ID
   - Business Account ID

### **Option B: Twilio (Recommended - Easy Setup)**
1. **Go to:** [Twilio Console](https://console.twilio.com/)
2. **Sign up** for Twilio account
3. **Enable WhatsApp Sandbox** (free for testing)
4. **Get credentials:**
   - Account SID
   - Auth Token
   - WhatsApp Sandbox Number

### **Option C: MessageBird (Alternative)**
1. **Go to:** [MessageBird](https://www.messagebird.com/)
2. **Sign up** and verify your account
3. **Enable WhatsApp API**
4. **Get API key**

## **Step 2: Environment Variables Setup**

Create a `.env` file in your backend directory:

```bash
# For Meta Business API
WHATSAPP_API_URL=https://graph.facebook.com/v18.0
WHATSAPP_API_TOKEN=your_access_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here

# For Twilio
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886

# Admin Configuration
ADMIN_PHONE_NUMBER=+254769582779
```

## **Step 3: Test Your Setup**

### **Test Registration:**
1. **Register a new student** through your app
2. **Check your WhatsApp** for the notification
3. **Verify the message** contains all student details

### **Test Message Format:**
```
🚨 NEW SAKU REGISTRATION ALERT!

📝 Student Details:
• Name: John Doe
• Registration Number: KCU/2023/12345
• Registration Type: Council Aspirant
• Position: Chair (President)

🔗 Admin Dashboard: http://your-domain.com/admin-dashboard-enhanced.html

⏰ Please review and verify the student's documents as soon as possible.

- SAKU Election System
```

## **Step 4: Production Deployment**

### **For Production:**
1. **Get production WhatsApp API credentials**
2. **Update environment variables**
3. **Test with real phone numbers**
4. **Monitor message delivery**

## **Troubleshooting**

### **Common Issues:**
1. **Invalid phone number format** - Use international format (+254769582779)
2. **API rate limits** - Check your provider's limits
3. **Message not delivered** - Verify phone number is on WhatsApp
4. **Authentication errors** - Check API credentials

### **Testing Commands:**
```bash
# Test WhatsApp service
python manage.py shell
>>> from elections.whatsapp_service import WhatsAppService
>>> service = WhatsAppService()
>>> service.send_admin_registration_alert('+254769582779', 'Test Student', 'KCU/2023/TEST', 'ASPIRANT', 'CHAIR')
```

## **Costs & Limits**

### **Meta Business:**
- **Free tier:** 1,000 messages/month
- **Paid:** $0.005 per message after free tier

### **Twilio:**
- **Sandbox:** Free for testing
- **Production:** $0.005 per message

### **MessageBird:**
- **Free tier:** 1,000 messages/month
- **Paid:** $0.005 per message after free tier

## **Security Notes**

1. **Never commit API keys** to version control
2. **Use environment variables** for all credentials
3. **Rotate API keys** regularly
4. **Monitor usage** to prevent abuse

## **Next Steps**

1. **Choose your provider** (recommend Twilio for ease)
2. **Set up your account** and get credentials
3. **Update environment variables**
4. **Test the integration**
5. **Deploy to production**

---

**Need Help?** Contact your provider's support team or check their documentation.