import tkinter as tk
from tkinter import scrolledtext
import anthropic

class ClaudeChatbot:
    def __init__(self):
        self.client = client = anthropic.Anthropic()
        self.setup_ui()
        self.conversation_history = []

    def setup_ui(self):
        self.window = tk.Tk()
        self.window.title("Claude Chatbot")
        self.window.geometry("600x400")

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, height=20)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input area
        self.input_frame = tk.Frame(self.window)
        self.input_frame.pack(padx=10, pady=5, fill=tk.X)

        self.message_entry = tk.Entry(self.input_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=5)

        # Bind Enter key to send message
        self.message_entry.bind("<Return>", lambda e: self.send_message())

    def send_message(self):
        user_message = self.message_entry.get()
        if user_message.strip():
            # Display user message
            self.chat_area.insert(tk.END, "You: " + user_message + "\n")
            
            # Prepare conversation context
            messages = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])
            
            # Get Claude's response
            try:
                response = self.client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1024,
                    messages=[
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ]
                )
                
                bot_response = response.content[0].text
                
                # Update conversation history
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": bot_response})
                
                # Display Claude's response
                self.chat_area.insert(tk.END, "Claude: " + bot_response + "\n\n")
                self.chat_area.see(tk.END)
            
            except Exception as e:
                self.chat_area.insert(tk.END, "Error: Could not get response from Claude\n\n")
                print(f"Error: {e}")

            # Clear input field
            self.message_entry.delete(0, tk.END)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    chatbot = ClaudeChatbot()
    chatbot.run()