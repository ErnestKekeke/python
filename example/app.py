import random

responses = {
    'hello': ["Hi there!", "Hello!", "Greatings!"],
    'how are you?': ["I'm doing well, thank you.", "I'm fine and you?"],
    'goodbye': ["Goodbye!", "See you later!", "Bye!"]
}

while True:
    user_input = input("You: ")
    if user_input.lower() in responses:
        bot_reply = random.choice(responses[user_input.lower()])
        print("Bot:", bot_reply, "\n")
    else:
        print("Bot: I am sorry, I didn't understand what you said.\n")



# if(__name__)=="__main__":
#     print("hello world")