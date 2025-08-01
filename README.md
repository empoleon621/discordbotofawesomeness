# 🤖 Aiden's Discord Bot

A modular, high-performance Discord bot built with Python and `discord.py`. Designed for both fun and functionality, it includes dynamic slash commands, intelligent autocomplete, and clean API integration — with more features on the way.

## ✨ Features

### 🔎 Smart Anime Search
- Uses AniList's GraphQL API to retrieve anime metadata.
- Implements **Discord-native autocomplete** to search from the **top 500 most popular anime**.
- Returns a rich embed with:
  - Title, Score, Status, Episodes
  - Large thumbnail
  - Direct AniList link

### 🧮 Secure Math Evaluator
- Accepts real-time user input via the `/math` command.
- Parses and evaluates mathematical expressions using `SimpleEval`.
- Supports functions like `sqrt()`, `sin()`, and more — all sandboxed for safety.

### 📸 Random Daniel Photo Command
- `/daniel` sends a randomly chosen image from a local directory.
- Designed for fun, personality, and meme use.
- Uses `random.choice()` to ensure variety.

### 💬 Message & Reaction Event Hooks
- Reacts to specific phrases in chat (e.g., `"poop"`) with playful responses.
- Detects when users react to messages and replies with the emoji used.

## 🔐 Security & Best Practices
- **Environment variables** handled securely via `.env`, excluded from version control.
- **Local image and log files** excluded via `.gitignore`.
- Modular architecture (`anime_cache.py`) makes it easy to expand features.
- Uses `httpx` for efficient asynchronous API requests.

## 🚀 Tech Stack
- [`discord.py`](https://github.com/Rapptz/discord.py) (v2.x)
- [`httpx`](https://www.python-httpx.org/)
- [`SimpleEval`](https://pypi.org/project/simpleeval/)
- AniList GraphQL API

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/aidens-discord-bot.git
cd aidens-discord-bot
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Set up your `.env`

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

### 4. Run the bot

```bash
python main.py
```

---

## 🛠️ Planned Features

- 🎮 Game stats integration
- 📊 Polls and voting
- 🎧 Music or soundboard support
- 📂 Modular plugin loading system
- 🧠 GPT-style conversation command

---

## 🧑‍💻 Author

**Aiden Solomon**  
Building tools at the intersection of fun and function.  
Contributions and ideas welcome!

---

## 📜 License

MIT License — feel free to use, modify, and share!
