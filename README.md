# lolbot

lolbot is a Discord bot built with Python, designed to enhance your Discord server's interactivity and fun. It responds to specific commands in chat, supports private messaging for specific features, integrates with YouTube to announce streams, and uses MQTT to publish overall probabilities.

## Features

- Replies to a test command in any channel.
- Processes a "prob" command via private message, accepting a number between 0 and 100. It calculates and announces the overall probability of an event happening based on user inputs.
- Handles "setstream" and "stream" commands to manage and announce YouTube stream URLs in a designated channel.
- Utilizes an SQLite database for persistent storage of stream URLs and user probabilities.
- Integrates with MQTT to publish the overall probability of an event to a specified topic, allowing integration with various IOT devices.

## Usage

- `!test`: The bot will reply to confirm it's active.
- `!prob <number>`: Send a private message with a number between 0 and 100 to set your probability for an event. The overall probability is then calculated and published via MQTT. Must be used in a DM.
- `!setstream <YouTube URL>`: Set a YouTube stream URL via DM. The bot will store the stream in the database and announce the stream in a designated channel.
- `!stream`: Fetches and prints the most recent stream URL if available and not older than 4 hours.

## Docker Support

lolbot supports deployment using Docker, making it easy to set up and run in any environment that supports Docker.

### Docker Compose

To deploy lolbot using Docker Compose, ensure you have Docker and Docker Compose installed on your system. Then follow these steps:

1. Create a `.env` file in the root directory with the necessary environment variables, such as `DISCORD_TOKEN`, `MQTT_BROKER`, `MQTT_TOPIC`, etc.
2. Use the provided `docker-compose.yml` file to define your services, including lolbot and any other dependent services like MQTT broker if needed.
3. Run `docker-compose up` to start the bot. Ensure your Docker Compose configuration maps the `./database` directory to a volume for persistent storage.

```yaml
version: '3'
services:
  lolbot:
    build: .
    volumes:
      - ./database:/app/database
    env_file:
      - .env
```
## Environment Variables

The bot relies on several environment variables for its configuration. These should be defined in a `.env` file in the root directory of the project. Here is a table of the required environment variables and a short description for each:

| Environment Variable     | Description                                               |
|--------------------------|-----------------------------------------------------------|
| `DISCORD_APP_ID`         | Discord Application ID.                                   |
| `DISCORD_PUBKEY`         | Discord Public Key.                                       |
| `DISCORD_TOKEN`          | Discord Bot Token.                                        |
| `DISCORD_PERMISSION_INT` | Integer representing the permissions the bot requires.    |
| `GENERAL_CHANNEL_ID`     | Discord channel ID where the bot will announce streams.   |
| `OPENAI_API_KEY`         | API Key for OpenAI services.                              |
| `DATABASE_PATH`          | Path to the SQLite database (e.g., `./database/bot.db`).  |
| `MQTT_BROKER_URL`        | URL of the MQTT broker.                                   |
| `MQTT_BROKER_PORT`       | Port of the MQTT broker (default is 1883 for MQTT).       |
| `MQTT_TOPIC`             | MQTT topic where the bot will publish probabilities.      |
| `MQTT_USERNAME`          | Username for MQTT broker authentication (if required).    |
| `MQTT_PASSWORD`          | Password for MQTT broker authentication (if required).    |

The `DATABASE_PATH` is set to use a relative path by default, but you can adjust this according to your deployment environment.
