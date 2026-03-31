# 🤖 AI Chat App (Streamlit + OpenRouter)

A AI Chat application built using **Streamlit** and **OpenRouter (LLM APIs)**.  
This app allows users to interact with LLM models like LLaMA in a ChatGPT-like interface.

---

## Features

- ChatGPT-style UI using Streamlit
- Multi-message conversation memory
- Supports OpenRouter models (LLaMA, Mistral, etc.)
- Secure API key handling via environment variables
- Auto-scroll chat window
following production-grade features has been added:
1. Login with DB
2. Password hashing (bcrypt)
3. User isolation (user_id)
4. Separate chats per user
5. Archive / restore
6. File + text input handling

---

## Tech Stack

- Python 3.x
- Streamlit
- OpenAI SDK (used with OpenRouter)
- OpenRouter API

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/amiit-singh5/ChatRepo.git
cd ChatRepo
