import random
import tkinter as tk
import asyncio
import websockets
import json
import threading

class WebSocketClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WebSocket Client")

        # Name input
        self.user_label = tk.Label(self.root, text="Enter your name:")
        self.user_label.pack()

        self.user_entry = tk.Entry(self.root)
        self.user_entry.pack()

        # Listbox to select chat room
        self.chat_room_label = tk.Label(self.root, text="Select Chat Room:")
        self.chat_room_label.pack()

        self.chat_room_listbox = tk.Listbox(self.root)
        self.chat_room_listbox.pack()

        # Add options to the Listbox
        self.chat_room_listbox.insert(tk.END, "politic")
        self.chat_room_listbox.insert(tk.END, "economy")
        self.chat_room_listbox.insert(tk.END, "offtopic")

        # Buttons
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_server)
        self.connect_button.pack()

        self.disconnect_button = tk.Button(self.root, text="Disconnect", command=self.disconnect_from_server, state=tk.DISABLED)
        self.disconnect_button.pack()

        self.websocket = None
        self.create_widgets()


    ## Create Tkinter widgets
    def create_widgets(self):
        self.send_text = tk.Text(self.root, width=50, height=10, wrap=tk.WORD)
        self.send_text.pack(side=tk.LEFT, padx=10, pady=10)

        self.receive_text = tk.Text(self.root, width=50, height=10, wrap=tk.WORD)
        self.receive_text.pack(side=tk.RIGHT, padx=10, pady=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=10, pady=5)


    ## Start connection button
    def connect_to_server(self):
        user = self.user_entry.get().strip()
        chat_room_index = self.chat_room_listbox.curselection()
        if chat_room_index:
            selected_chat_room = self.chat_room_listbox.get(chat_room_index)
            uri = f"ws://localhost:8000/chat/{selected_chat_room}"
            self.user_entry.config(state="disabled")
            self.chat_room_listbox.config(state="disabled")
            self.connect_button.config(state="disabled")
            self.disconnect_button.config(state="normal")
            
            self.websocket_thread = threading.Thread(target=self.websocket_loop, args=(user, uri, selected_chat_room))
            self.websocket_thread.daemon = True
            self.websocket_thread.start()
        else:
            print("Please select a chat room.")


    ## Disconnect
    def disconnect_from_server(self):
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.close(), self.root.loop)
            self.user_entry.config(state="normal")
            self.chat_room_listbox.config(state="normal")
            self.connect_button.config(state="normal")
            self.disconnect_button.config(state="disabled")
            user = self.user_entry.get().strip() or 'Anonymous user'
            self.receive_text.insert(tk.END, f"## {user} leave the chat room ##\n")
        else:
            print("Not connected to any server.")


    ## Dispatch chat message from Tkinter to send_message_async function
    def send_message(self):
        message = self.send_text.get("1.0", tk.END).strip()
        asyncio.run_coroutine_threadsafe(self.send_message_async(message), self.root.loop) if message else None


    ## Dispatch chat message to server
    async def send_message_async(self, message):
        try:
            data = {'message': message, 'user': self.user_entry.get().strip()}
            await self.websocket.send(json.dumps(data))
            self.send_text.delete("1.0", tk.END)
        except websockets.ConnectionClosedError:
            print("Connection closed.")


    ## Dispatch simulated messages to server
    async def send_simulated_data(self):
        while True:

            message = f"Simulated message {random.randint(1, 100)}"
            user = self.user_entry.get().strip()
            data = {'message': message, 'user': user}

            try:
                await self.websocket.send(json.dumps(data))
            except websockets.ConnectionClosedError:
                print("Connection closed.")
                break

            await asyncio.sleep(random.uniform(1, 2))


    ## Receive messages from server
    async def receive_messages(self, selected_chat_room):
        
        # First connection message
        self.receive_text.insert(tk.END, f"WELCOME to the {selected_chat_room} chat room!\n")

        while True:
            try:
                data = await self.websocket.recv()
                data_json = json.loads(data)
                self.receive_text.insert(tk.END, f"{data_json['message']}\n")
                self.receive_text.yview_moveto(1.0)

            except websockets.exceptions.ConnectionClosedOK:
                print("Connection closed succefully.")
                break

            except websockets.ConnectionClosedError:
                print("Connection closed.")


    ## Websocket loop definition
    def websocket_loop(self, user, uri, selected_chat_room):

        async def connect_to_server():
            self.websocket = await websockets.connect(uri, extra_headers={'user': user})

        loop = asyncio.new_event_loop()
        self.root.loop = loop
        asyncio.set_event_loop(loop)
        loop.run_until_complete(connect_to_server())
        asyncio.run_coroutine_threadsafe(self.send_simulated_data(), loop)
        loop.run_until_complete(self.receive_messages(selected_chat_room))


def main():
    root = tk.Tk()
    app = WebSocketClientApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()