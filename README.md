
# 🦜 Langchain: Getting Started 🚀

Meetup Generative AI Nantes 20/07/2023.

```txt
OpenAI:
* https://openai.com/
* You will get a 5€ free tier
* Create token here: https://platform.openai.com/account/api-keys
```

## For meetup organizers

1- Prepare a PostgreSQL instance with the IMDB database imported
2- Some participants might not have access to a Slack organization. Prepare a fresh new Slack team and invite participants with "owner" permissions.
3- Create an OpenAI account with 5€ free credits. It should be sufficient for 10-20 participants.

Remember the goal of this tuto is not to set up a Slack bot, but to manipulate Langchain. If participants take too much time to start, you can fall back on a simple stdin prompt.

Warning: suggest to the participants to use a different Slack app name and Slack slash command.

## Import and start IMDB database

(optional if the meetup organizer prepared a PostgreSQL server with live data)

```sh
docker-compose up -d

# Get the download link on the following page:
# https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/2QYZBT

wget -O dump_pg11 '<s3-download-url>'

apt install postgresql-client postgresql-client-common libpq-dev
pg_restore -d screeb -U screeb -h localhost -p 5432 --clean --if-exists -v dump_pg11
```

```sh
psql postgres://screeb:screeb@localhost:5432/screeb
```

## Step 1 - Request IMDB database from Slack

### Create Slack bot

1- Go to https://api.slack.com/apps a create an app using the following [manifest](./assets/slack/manifest.json).
2- Go to `Basic Information` and click on `Install to Workspace`.
3- Next, in `Basic Information` page, generate a `App Level Token` with the `connections:write` scope. Copy the `Token` (= SLACK_APP_TOKEN).
4- Go to `OAuth & Permissions`, copy the `Bot User OAuth Token` (= SLACK_BOT_TOKEN).
5- Next, navigate to the `Socket Mode` section and toggle the `Enable Socket Mode` button to start receiving events over a WebSocket connection.
6- Go to `App Home` page and check the box `Allow users to send Slash commands and messages from the messages tab`.

### Create a simple Slack command

In your Slack app configuration, go to `Slash Command`, and create a new `/clippy` command.

```sh
export SLACK_BOT_TOKEN=xoxb-xxxxxxx
export SLACK_APP_TOKEN=xapp-xxxxxxx
export OPENAI_API_KEY=xxxxxxx

pip3 install -r requirements.txt
python3 step1-bot.py
```

In Slack, a Clippy App has appeared. Send the following message in its private channel: `/clippy hello world`.

### Langchain!

In this step, you will connect your Slack command to a Langchain chain, that generates SQL queries, and send them to a database.

Use OpenAI LLM to format the result of the SQL query. The models `gpt-3.5-turbo` (4k tokens) and `gpt-3.5-turbo-16k` (16k tokens) are a good start.

Documentation:
- https://python.langchain.com/docs/modules/chains/popular/sqlite
- https://python.langchain.com/docs/modules/agents/toolkits/sql_database

Advanced:
* Limit the table visible by your AI
* Create a custom SQL view to select the data you wish to expose
* Feel free to customize your prompt: https://github.com/hwchase17/langchain/blob/master/langchain/chains/sql_database/prompt.py
* If you run this tutorial against your data warehouse, don't forget to create a read-only user. 😁 😘
* [Format your Slack response](https://api.slack.com/reference/surfaces/formatting#inline-code) and write the SQL query in a note.

__Example 1__:

> /clippy how many movies in 2000 ?

Final answer here: There are 53,013 movies in the year 2000.

__Example 2__:

> /clippy count movies per year between 2010 and 2015

Final answer here: The number of movies produced per year, in descending order, are as follows: 
- 2012: 164,307 movies
- 2011: 160,017 movies
- 2010: 141,703 movies
- 2013: 63,827 movies
- 2014: 3,077 movies

__Example 3__:

> /clippy Movie titles containing "star wars". 1 movie per line.

Finished chain.
Star Wars: Episode IV
Star Wars VII
Star Wars vs Star Trek
Drunk Star Wars
Star Wars Original Trilogy

## Step 2 - Question the IPCC AR6 report

Now, let's build a simple question-answering bot based on the IPCC AR6 reports. The PDFs are provided in this repository. You should start with the Summary for Policymakers (SPM), then when your chain is ready, generate embeddings with the full reports!

We will use IPCC reports hosted in this repository. Cloning the repository requires git LFS:

```bash
brew install git-lfs  
git lfs install
```

In this step, the Slack app you built above is optional. You can use `step2-stdin.py` instead.

In your Langchain chain, you will need:
- a pdf loader (many loaders are available)
- a text splitter to tokenize files
- an embedding model to convert tokens into vectors (OpenAI or "sentence transformers" hosted on HuggingFace)
- an (in-memory?) vector database
- a retriever to query the vector database
- a question-answering model that will format the output

A few questions to ask:
- "What drives emissions from human activities?"
- "Comment ont évolué les émissions depuis 2010?"
- "List climate models"
- "What are the main vulnerabilities?"

Documentation:
- https://python.langchain.com/docs/use_cases/question_answering/
- https://python.langchain.com/docs/modules/chains/popular/chat_vector_db
- https://python.langchain.com/docs/modules/data_connection/document_loaders/how_to/pdf

## Step 3 - Chain of thought

Merge both steps 1 and 2 into a single prompt in your Slack bot. Your Langchain script should handle the right route, based on the user question.
