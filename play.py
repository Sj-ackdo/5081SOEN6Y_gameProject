from sys import argv

for i in range(len(argv)-1):
    if argv[i] == "--name":
        client_name = argv[i+1]
    if argv[i] == "--password":
        server_password = argv[i+1] # password implementation



if __name__ == "__main__":
    print("Game")
