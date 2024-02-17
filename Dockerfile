# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the bot directory and requirements.txt into the container at /app
COPY bot/ /app/bot/
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable to specify the directory of bot scripts
ENV BOT_DIR=/app/bot

# Run bot.py when the container launches, adjusting the path as needed
CMD ["python", "./bot/bot.py"]