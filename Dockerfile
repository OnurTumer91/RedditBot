FROM python:3.10-slim

# Working directory
WORKDIR /app

# Set PYTHONPATH to current directory explicitly
ENV PYTHONPATH=/app

# Copy dependency list and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly copy your code
COPY ./config ./config
COPY ./src ./src

# Run the bot
CMD ["python", "src/bot.py"]
