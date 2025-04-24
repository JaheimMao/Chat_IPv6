# Chat_IPv6

## Features

This project implements text-based chat communication between two hosts in an IPv6 environment. It supports user registration and login, peer-to-peer chat, and group chat functionalities.

## Implementation Process

### Socket Communication Based on the UDP Protocol

UDP is a connectionless protocol. Before data transmission, no connection is established between the source and the destination. When it wants to send data, it simply takes the data from the application and throws it onto the network as quickly as possible.

The main methods used at the protocol level are:

```
socket([family[, type[, proto]]])  
bind(address: Union[_Address, bytes])  
sendto(data, address)  
recvfrom(bufsize, flags)  
```

### SQLite3 Database

During program development, a database is needed to store user information such as usernames, passwords, status, IP addresses, and ports. SQLite3, a lightweight database, is used for easy migration and maintenance.

| Function Name  | Description    |
| :------------: | :------------: |
| `init(self)` | Creates and opens the database |
| `select_all(self)` | Retrieves all user information from the relevant database table |
| `register(self, username, password, ip, port)` | Called during registration to add user information |
| `search_username(self, username)` | Searches for user information by username |
| `login_success(self, username, ip, port)` | Updates user status upon successful login |
| `login_check(self, username, password, ip, port)` | Checks username and password during login |
| `logout_success(self, username)` | Updates user status when logging out |
| `db_close(self)` | Closes the database |

## Test Procedure

On two hosts that can communicate with each other, navigate to the code directory and run `python3 Client.py` and `python3 Server.py` respectively. Multiple clients can be launched, but only one server should run. Starting the server also opens the database.

Follow the prompts to choose different functionalities. In peer-to-peer chat, either party can send `END` to close the chat; the other party can confirm closure based on the prompt. Group chat works similarly in principle and the test procedure is nearly the same.
