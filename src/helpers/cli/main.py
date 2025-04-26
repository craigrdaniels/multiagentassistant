# Handle input and output of the chatbot on the CLI


# chatbot will output to the CLI
def speak(text: str):
    """
    Function to output text to the CLI.
    """
    # print(text, end="", flush=True)


def listen(timeout=5):
    """
    Function to simulate listening for user input from the CLI.
    """
    user_input = input("\n\nYou: ")
    print("-----")
    return user_input.lower()
