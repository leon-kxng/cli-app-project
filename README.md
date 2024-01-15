# cli-app-project

Welcome to the Chatroom, a powerful Command Line Interface Python Chat Application that not only facilitates real-time communication between users but also stores your precious messages in an SQL database for future reference. This application is built using the SocketServer framework and SQLite for efficient data management.

## Features

- Real-Time Chat: Engage in seamless, real-time communication with other users through a command-line interface.

- SQL Database Storage: Your messages, along with the user who sent them and the timestamp, are securely stored in an SQL database for future     retrieval and analysis.

- User Authentication: The application includes a database for managing usernames and passwords, ensuring a secure and personalized chat experience.

### **Usage** 

## Clone the Repository

    
     git clone git@github.com:leon-kxng/cli-app-project.git
     cd cli-app-project

## Run the Server

Start the server by running server.py with the desired port and host parameters.

    python3 server.py [PORT] [HOST]

If no parameters are provided, it defaults to 10000 localhost.

## Connect Clients

Clients can connect to the server using client.py. Provide the appropriate port and host parameters.

    python3 client.py [PORT] [HOST]

If no parameters are provided, it defaults to 10000 localhost.

Enjoy Chatting!

Once connected, you can send and receive messages in real-time. All messages will be stored securely in the SQL database.

## Dependencies

    Python 3.x
    SQLite


## Author

This application was crafted by [Leon](https://github.com/Leon-kxng). You can find more of [my work](https://github.com/Leon-kxng) on GitHub

## License

This project is licensed under the [MIT License](./LICENSE). Feel free to use and modify the code as per your requirements.
