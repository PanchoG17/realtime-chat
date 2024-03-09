# Junco Films Real-Time Chat with WebSockets and Redis

Welcome to the **Real-Time Chat** project!. This project provides a real-time chat system using WebSockets technology with Django Channels and Redis for managing channels.

## The project includes three types of clients:

1. **<u>Web Browser Client:</u>** Access the chat system through a web browser interface.
2. **<u>Tkinter GUI Client:</u>** Interact with the chat system using a Tkinter-based graphical user interface.
3. **<u>Script Launcher:</u>** Launch multiple instances of a basic Python client script to connect to the chat system.

Users can connect to their preferred chat room, including politics, economy, and off-topic discussions, and engage in real-time conversations.


## Folder Structure:
*Note: The following directory structure includes only the relevant folders and files.*

- `clients`: WebSocket clients
    - `basic_python_client.py` : A basic python client for receive messages from server.
    - `client_launcher.py` : Used to launch 10 instances of basic python client.
    - `tkinter_python_client.py` : A Tkinter GUI python client for send and recive messages.

- `data_stream`: Django WebSocket server
    - `templates`: HTML templates folder
        - `base.html`: base layout.
        - `lobby.html`: template for main page.
        - `chat_room.html`: template for single chat room.
    - `routing.py` : WebSocket routing configuration.
    - `consumers.py` : WebSocket consumer logic.
    - `urls.py` : URL patterns for HTTP application.
    - `views.py` : view functions for HTTP requests.

- `realtime_data_processing`: Django settings folder
    - `settings.py`: Configuration settings for Django project.
    - `urls.py`: URL patterns mapping URLs to views.


## Prerequisites
Before running this project, ensure you have the following installed:

- Python
- Docker
- Docker Compose
- websockets python library

## Run Project
Follow these steps to run the project:

1. Clone the repository:
    ```console
    git clone https://github.com/PanchoG17/realtime-chat.git

2. Navigate to the project directory:
    ```console
    cd ./realtime_data_processing

3. Run Docker Compose:
    ```console
    docker-compose up --build

4. Access the application via client browser:
    ```
    Open a web browser and go to http://localhost:8000.

5. Navigate to the clients directory:
    ```console
    cd ./clients
    ```

6. Launch the terminal clients:
    ```console
    python client_launcher.py
    ```
    - Enter your username and select a chat room from the available options.

6. Accessing the Application via Tkinter GUI:
    ```console
    python tkinter_python_client.py
    ```
    - Enter your username and select a chat room from the available options.
    - Click the "Connect" button to establish a connection to the chat server.
    - It will automatically spawm simulated messages.
    - Type your message in the text area and click "Send" to send messages to the chat room.
    - Click the "Disconnect" button to end the chat session and disconnect from the server.