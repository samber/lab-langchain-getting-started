import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.command("/clippy")
def handle_clippy_command(ack, say, command):
    ack()

    user_question = command['text']

    # Add functionality here, with the Langchain stuff

    say(f"Hi there, <@{command['user_name']}>!")

if __name__ == "__main__":
    # This is the App-level token starting with `xapp-`
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
