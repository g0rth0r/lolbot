# lolbot

lolbot is a Discord bot built with Python designed to enhance your Discord server's interactivity and fun. It responds to specific commands in chat, supports private messaging for specific features, and integrates with YouTube to announce streams.

## Features

- Replies to a test command in any channel.
- Processes a "prob" command via private message, accepting a number between 0 and 100 and responding with custom logic.
- Handles "setstream" and "stream" commands to manage and announce YouTube stream URLs in a designated channel.

## Usage

- `!test`: The bot will reply to confirm it's listening.
- `!prob <number>`: Send a private message with a number between 0 and 100 to receive a custom response. Must be used in a DM.
- `!setstream <YouTube URL>`: Set a YouTube stream URL via DM. The bot will announce the stream in a designated channel.
- `!stream`: Prints the current stream URL if available.

## Docker Support

**Coming Later**

## Contributing

Contributions are welcome! Please open an issue or pull request if you'd like to contribute to the project.

