import spacy
from transformers import pipeline
import torch

class NLPProcessor:
    def __init__(self):
        # Load spaCy model for NER
        self.nlp = spacy.load('en_core_web_sm')

        # Load pre-trained BERT model for intent classification
        self.intent_classifier = pipeline(
            'zero-shot-classification',
            model='facebook/bart-large-mnli',
            device=0 if torch.cuda.is_available() else -1
        )

        # Define intents
        self.intents = {
            'faq': ['question', 'help', 'information', 'how', 'what', 'when', 'where', 'why'],
            'order_tracking': ['track', 'order', 'status', 'delivery', 'shipped', 'arrived'],
            'return_request': ['return', 'refund', 'exchange', 'cancel', 'problem', 'defective'],
            'human_support': ['speak', 'agent', 'representative', 'manager', 'supervisor', 'complex']
        }

        # Sentiment analysis pipeline
        self.sentiment_analyzer = pipeline(
            'sentiment-analysis',
            model='cardiffnlp/twitter-roberta-base-sentiment-latest',
            device=0 if torch.cuda.is_available() else -1
        )

    def classify_intent(self, text):
        """Classify the intent of the user's message."""
        # Use zero-shot classification with our defined intents
        candidate_labels = list(self.intents.keys())
        result = self.intent_classifier(text, candidate_labels=candidate_labels)
        return result['labels'][0], result['scores'][0]

    def extract_entities(self, text):
        """Extract named entities from the text."""
        doc = self.nlp(text)
        entities = {}
        for ent in doc.ents:
            entities[ent.label_] = ent.text
        return entities

    def analyze_sentiment(self, text):
        """Analyze the sentiment of the text."""
        result = self.sentiment_analyzer(text)[0]
        # Convert to numerical score: negative=-1, neutral=0, positive=1
        if result['label'] == 'LABEL_0':
            return -1  # negative
        elif result['label'] == 'LABEL_1':
            return 0   # neutral
        else:
            return 1   # positive

    def preprocess_text(self, text):
        """Preprocess text for better NLP processing."""
        # Lowercase
        text = text.lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
