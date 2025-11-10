# Customer Support Chatbot

A comprehensive AI-powered customer support chatbot for e-commerce platforms, built with Python, Streamlit, and advanced NLP models.

## Features

### Core Functionality
- **Intelligent Intent Classification**: Automatically categorizes customer queries into intents like order tracking, returns, FAQs, etc.
- **Sentiment Analysis**: Analyzes customer sentiment to prioritize urgent issues
- **Entity Extraction**: Identifies key information like order IDs, product names, and dates
- **Voice Input Support**: Transcribes voice messages using OpenAI Whisper
- **Real-time Responses**: Provides instant responses with confidence scores
- **Database Integration**: Stores conversations and order data for analysis

### Technical Features
- **Multi-modal Input**: Supports both text and voice inputs
- **Chat History**: Maintains conversation context
- **Feedback System**: Allows users to rate interactions
- **User Authentication**: Optional email-based user tracking
- **Error Handling**: Graceful fallback to human agents for complex queries

## Technology Stack

### Core Libraries
- **Streamlit**: Web application framework
- **spaCy**: Natural Language Processing
- **Transformers**: Pre-trained NLP models from Hugging Face
- **OpenAI Whisper**: Speech-to-text transcription
- **SQLite**: Database for data persistence

### NLP Models
- **Intent Classification**: Custom-trained model for customer support intents
- **Sentiment Analysis**: RoBERTa-based sentiment classifier
- **Named Entity Recognition**: spaCy for entity extraction

## Installation

### Prerequisites
- Python 3.8+
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/developerom1/BIA-FINAL-CUSTOMER-SUPPORT-BOT.git
   cd BIA-FINAL-CUSTOMER-SUPPORT-BOT
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
customer-support-bot/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── TODO.md               # Development tasks and progress
├── test_chatbot.py       # Unit tests
├── data/
│   └── chatbot.db        # SQLite database
└── src/
    ├── chatbot.py        # Main chatbot logic
    ├── nlp.py           # NLP processing utilities
    └── database.py      # Database operations
```

## Usage

### Starting the Application
1. Run `streamlit run app.py`
2. Open the provided local URL in your browser
3. Enter your email (optional) in the sidebar
4. Choose between text or voice input

### Supported Query Types
- **Order Tracking**: "Where is my order #12345?"
- **Returns**: "I want to return this product"
- **FAQs**: "What are your shipping policies?"
- **Complaints**: "The product arrived damaged"
- **General Support**: "I need help with my account"

### Voice Input
- Click the voice input option
- Record your message
- The system will transcribe and process your speech

## NLP Pipeline

### Intent Classification
- Uses a fine-tuned transformer model
- Supports 8+ intent categories
- Provides confidence scores for each prediction

### Sentiment Analysis
- Analyzes emotional tone of customer messages
- Helps prioritize urgent negative feedback
- Uses RoBERTa-base model fine-tuned on Twitter data

### Entity Extraction
- Identifies order numbers, dates, product names
- Uses spaCy's statistical NER model
- Custom rules for domain-specific entities

## Database Schema

### Conversations Table
- Stores chat history and metadata
- Tracks user information and timestamps
- Links to intent classification results

### Orders Table
- Sample order data for demonstration
- Includes order status, dates, and customer info

## Testing

Run the test suite:
```bash
python test_chatbot.py
```

## Deployment

### Local Deployment
- Follow installation instructions above
- Ensure all dependencies are installed
- Run with `streamlit run app.py`

### Production Deployment
- Use Streamlit Cloud, Heroku, or similar platforms
- Configure environment variables for API keys
- Set up proper database (PostgreSQL recommended for production)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for Whisper speech recognition
- Hugging Face for transformer models
- spaCy for NLP processing
- Streamlit for the web framework

## Future Enhancements

- Integration with actual e-commerce APIs
- Multi-language support
- Advanced conversation flow management
- Integration with CRM systems
- Analytics dashboard for support metrics
- Machine learning model improvements
