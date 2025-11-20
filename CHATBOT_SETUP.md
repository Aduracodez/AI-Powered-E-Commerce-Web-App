# 🤖 AI Chatbot Setup Guide

## ✅ What's Been Added

Your e-commerce store now has an AI-powered chatbot that can:
- ✅ Answer product questions
- ✅ Check order status (for logged-in users)
- ✅ Provide shipping information
- ✅ Help with returns and refunds
- ✅ Answer general store questions
- ✅ Use Groq AI (LLaMA 3.3 70B - Fast and powerful, optional, falls back to rule-based if not configured)

## 🚀 Quick Start

### Step 1: Install Backend Dependencies

```bash
cd backend_django
source venv/bin/activate
pip install groq==0.9.0
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 2: Configure Groq (Optional but Recommended)

#### Option A: Using Groq API (Fast AI responses with LLaMA 3.3)

1. **Get a Groq API Key:**
   - Go to https://console.groq.com/keys
   - Sign up or log in (free tier available!)
   - Create a new API key
   - Copy the key (starts with `gsk_`)

2. **Set the API Key:**
   
   **On Mac/Linux:**
   ```bash
   export GROQ_API_KEY="your-api-key-here"
   ```
   
   **On Windows:**
   ```cmd
   set GROQ_API_KEY=your-api-key-here
   ```
   
   **Or create a `.env` file** in `backend_django/`:
   ```
   GROQ_API_KEY=your-api-key-here
   ```

3. **Install python-dotenv** (for .env file support):
   ```bash
   pip install python-dotenv
   ```
   
   Then add to `backend_django/ecommerce_project/settings.py`:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

#### Option B: Use Rule-Based System (Free, No API Key)

The chatbot will work **without** an API key using a smart rule-based system. It can:
- Answer common questions
- Provide product information
- Help with orders and shipping
- Handle greetings and general inquiries

**Note:** The rule-based system is less sophisticated but works perfectly fine for most queries!

### Step 3: Restart Backend Server

```bash
cd backend_django
source venv/bin/activate
python manage.py runserver 8000
```

### Step 4: Test the Chatbot

1. Open your frontend: http://localhost:3001
2. Look for the **💬** button in the bottom-right corner
3. Click it to open the chatbot
4. Try asking:
   - "What products do you have?"
   - "Tell me about shipping"
   - "How can I return an item?"

## 📋 Features

### For Users
- **24/7 Support:** Always available to help
- **Instant Responses:** Quick answers to common questions
- **Order Tracking:** Check order status (if logged in)
- **Product Help:** Get information about products

### For You
- **No Code Changes Needed:** Works out of the box
- **Flexible:** Works with or without OpenAI API
- **Cost-Effective:** Free rule-based system, or pay-per-use OpenAI
- **Context-Aware:** Knows about your products, categories, and orders

## 🔧 Configuration

### Change Chatbot Welcome Message

Edit `frontend/src/components/Chatbot.js`:
```javascript
const [messages, setMessages] = useState([
  {
    role: 'assistant',
    message: "Your custom welcome message here!"
  }
]);
```

### Customize System Prompt (Groq)

Edit `backend_django/api/views.py` in the `get_groq_response` function:
```python
system_prompt = f"""Your custom instructions here...
"""
```

### Adjust Rule-Based Responses

Edit `backend_django/api/views.py` in the `get_rule_based_response` function to customize responses.

## 💰 Cost Information

### Rule-Based System
- **Cost:** Free forever
- **Limitations:** Pre-programmed responses
- **Best for:** Most common questions

### Groq AI (LLaMA 3.3 70B)
- **Cost:** FREE tier available! 30 requests/minute
- **Speed:** Ultra-fast responses (~100-200ms)
- **Models:** LLaMA 3.3 70B, Mixtral 8x7B, and more
- **Free Tier:** Generous free tier, perfect for most stores
- **Best for:** Fast, natural conversations with powerful models

**Free Tier Limits:**
- 30 requests per minute
- Unlimited requests per day (within rate limit)
- Perfect for small to medium stores

**Paid Plans:** Available for higher rate limits if needed

## 🎨 Customization

### Change Chatbot Appearance

Edit `frontend/src/components/Chatbot.css`:
- Colors: Search for `#00d4ff` and `#0099cc` to change theme
- Position: Modify `.chatbot-toggle` and `.chatbot-container`
- Size: Adjust width/height in `.chatbot-container`

### Add More Features

You can extend the chatbot to:
- Search products in real-time
- Add items to cart
- Process orders
- Send email notifications
- Integrate with other services

## 🐛 Troubleshooting

### Chatbot Not Appearing
- Check browser console (F12) for errors
- Ensure frontend is running on port 3001
- Verify backend is running on port 8000

### "Trouble connecting" Error
- Check backend server is running
- Verify API endpoint: `http://localhost:8000/api/chatbot/`
- Check browser console for detailed errors

### Groq API Not Working
- Verify API key is set correctly (starts with `gsk_`)
- Check API key is valid (Groq console: https://console.groq.com)
- Verify you have API quota (free tier: 30 requests/minute)
- Test API key: Check Groq dashboard for usage
- The chatbot will fall back to rule-based system if Groq fails

### Responses Not Contextual
- If using rule-based: Responses are pre-programmed
- If using Groq: Check system prompt in `views.py`
- Verify store context is being passed correctly

## 📝 API Endpoint

**POST** `/api/chatbot/`

**Request Body:**
```json
{
  "message": "What products do you have?",
  "history": [
    {"role": "user", "message": "Hello"},
    {"role": "assistant", "message": "Hi there!"}
  ]
}
```

**Response:**
```json
{
  "response": "We have a great selection of products..."
}
```

## 🔒 Security Notes

- Chatbot is accessible to all users (no authentication required)
- API key should be kept secret (use environment variables)
- Don't commit API keys to git
- Consider rate limiting for production

## 📚 Next Steps

1. ✅ Test the chatbot with common questions
2. ✅ Customize responses for your store
3. ✅ (Optional) Set up Groq API for faster, better AI (free tier available!)
4. ✅ Train team on how to use chatbot insights
5. ✅ Monitor chatbot usage and improve responses

## 🎯 What the Chatbot Can Do

### Without Login (All Users):
- Product information
- Category browsing
- Shipping information
- Return policies
- General store questions

### With Login (Authenticated Users):
- Order status
- Order history
- Personalized recommendations
- Account-specific information

---

**Need help?** Check the console logs or ask me to customize the chatbot further!

