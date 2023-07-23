
def ask(prompt):
    """Run your chain here."""
    return ""

def get_prompt():
    print("Type 'exit' to quit")

    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                print(ask(prompt))
            except Exception as e:
                print(e)

if __name__ == "__main__":
    get_prompt()
