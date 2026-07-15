from database.db import get_chat_history

history = get_chat_history()

print("\n========== CHAT HISTORY ==========\n")

for chat in history:
    print("Username :", chat[0])
    print("User     :", chat[1])
    print("Bot      :", chat[2][:80], "...")
    print("Time     :", chat[3])
    print("-" * 60)