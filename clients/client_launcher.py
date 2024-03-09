import subprocess

chatrooms = ['politic','economy','offtopic']
user = input("Enter your name:")
user = 'Anonymous user' if user == '' else user
chatroom_name = input(f"Enter your chatroom {chatrooms}:")

while chatroom_name not in chatrooms:
    print('Choose a valid chat room')
    chatroom_name = input(f"Enter your chatroom {chatrooms}:")

uri = f"ws://localhost:8000/chat/{chatroom_name}"

if __name__ == "__main__":

    for i in range(10):
        user_i = f"{user} - {i}"
        process = subprocess.Popen(["python", "basic_python_client.py", user_i, uri])
        
    process.wait()