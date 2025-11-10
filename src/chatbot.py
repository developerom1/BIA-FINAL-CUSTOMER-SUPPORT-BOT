from src.database import Database
from src.nlp import NLPProcessor
import re

class CustomerSupportBot:
    def __init__(self):
        self.db = Database()
        self.nlp = NLPProcessor()

    def process_message(self, user_message, user_email=None):
        """Process user message and return appropriate response."""
        # Preprocess the message
        processed_message = self.nlp.preprocess_text(user_message)

        # Classify intent
        intent, confidence = self.nlp.classify_intent(processed_message)

        # Extract entities
        entities = self.nlp.extract_entities(user_message)

        # Analyze sentiment
        sentiment = self.nlp.analyze_sentiment(user_message)

        # Get user ID if email provided
        user_id = None
        if user_email:
            user = self.db.get_user_by_email(user_email)
            if user:
                user_id = user[0]

        # Generate response based on intent
        response = self.generate_response(intent, processed_message, entities, confidence)

        # Save conversation to database
        if user_id:
            self.db.save_conversation(user_id, user_message, response, sentiment)

        return {
            'response': response,
            'intent': intent,
            'confidence': confidence,
            'sentiment': sentiment,
            'entities': entities
        }

    def generate_response(self, intent, message, entities, confidence):
        """Generate response based on classified intent."""
        if confidence < 0.5:
            return "I'm not sure I understand your question. Could you please rephrase it or provide more details?"

        if intent == 'faq':
            return self.handle_faq(message)
        elif intent == 'order_tracking':
            return self.handle_order_tracking(message, entities)
        elif intent == 'return_request':
            return self.handle_return_request(message, entities)
        elif intent == 'human_support':
            return self.handle_human_support(message)
        else:
            return "I'm here to help with FAQs, order tracking, returns, and connecting you to human support. How can I assist you today?"

    def handle_faq(self, message):
        """Handle FAQ queries."""
        # Simple keyword matching for FAQs
        faqs = self.db.get_faqs_by_category()

        for question, answer in faqs:
            if any(keyword in message for keyword in question.lower().split()):
                return answer

        return "I couldn't find a specific answer to your question. Here are some common FAQs:\n" + \
               "\n".join([f"- {q}" for q, _ in faqs[:3]])

    def handle_order_tracking(self, message, entities):
        """Handle order tracking queries."""
        # Extract order ID from message or entities
        order_id = self.extract_order_id(message, entities)

        if order_id:
            order = self.db.get_order_by_id(order_id)
            if order:
                return f"Your order #{order_id} for {order[7]} is currently {order[5]}. It was placed on {order[4]}."
            else:
                return f"I couldn't find an order with ID {order_id}. Please check your order number and try again."
        else:
            return "To track your order, please provide your order number. You can find it in your confirmation email."

    def handle_return_request(self, message, entities):
        """Handle return requests."""
        # Extract order ID
        order_id = self.extract_order_id(message, entities)

        if order_id:
            return f"I've initiated a return request for order #{order_id}. Our team will contact you within 24 hours to process your return. Please have your order details ready."
        else:
            return "To process a return, please provide your order number. Our return policy allows returns within 30 days of purchase."

    def handle_human_support(self, message):
        """Handle requests for human support."""
        return "I understand this might be a complex issue. I'm connecting you to a human support agent. Please hold on while I transfer you. In the meantime, could you briefly describe your issue?"

    def extract_order_id(self, message, entities):
        """Extract order ID from message or entities."""
        # Look for patterns like "order 123", "#123", "123"
        order_pattern = r'(?:order\s*#?|#)?(\d+)'
        match = re.search(order_pattern, message, re.IGNORECASE)
        if match:
            return int(match.group(1))

        # Check entities for CARDINAL (numbers)
        if 'CARDINAL' in entities:
            try:
                return int(entities['CARDINAL'])
            except ValueError:
                pass

        return None
