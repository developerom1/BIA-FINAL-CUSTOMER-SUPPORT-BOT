import time
from src.chatbot import CustomerSupportBot

def test_chatbot():
    bot = CustomerSupportBot()

    # Test cases
    test_messages = [
        "How do I track my order?",
        "I want to return my laptop order number 1",
        "What is your return policy?",
        "I need to speak to a human agent",
        "My order 2 is delayed",
        "How do I reset my password?"
    ]

    print("Testing Customer Support Chatbot")
    print("=" * 50)

    total_response_time = 0
    correct_intents = 0
    total_tests = len(test_messages)

    expected_intents = [
        'faq',
        'return_request',
        'faq',
        'human_support',
        'order_tracking',
        'faq'
    ]

    for i, message in enumerate(test_messages):
        print(f"\nTest {i+1}: '{message}'")
        start_time = time.time()
        result = bot.process_message(message)
        response_time = time.time() - start_time

        total_response_time += response_time

        print(f"Response: {result['response']}")
        print(f"Intent: {result['intent']} (Confidence: {result['confidence']:.2f})")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Entities: {result['entities']}")
        print(f"Response Time: {response_time:.2f} seconds")

        # Check intent accuracy
        if result['intent'] == expected_intents[i]:
            correct_intents += 1
            print("✓ Intent classification correct")
        else:
            print("✗ Intent classification incorrect")

    # Calculate metrics
    avg_response_time = total_response_time / total_tests
    intent_accuracy = correct_intents / total_tests * 100

    print("\n" + "=" * 50)
    print("EVALUATION METRICS")
    print("=" * 50)
    print(f"Intent Classification Accuracy: {intent_accuracy:.1f}%")
    print(f"Average Response Time: {avg_response_time:.2f} seconds")
    print(f"Total Tests: {total_tests}")

    # Manual evaluation note
    print("\nNote: Response Appropriateness requires manual evaluation.")
    print("Please review the responses above for appropriateness.")

if __name__ == "__main__":
    test_chatbot()
