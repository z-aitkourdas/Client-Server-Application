import socket
from pathlib import Path

BUFFER_SIZE = 8192


def download_file(sock: socket.socket, filename: str, filesize: int) -> None:
    target_path = Path.cwd() / f"Downloaded_{filename}"
    with target_path.open("wb") as target:
        received = 0
        while received < filesize:
            chunk = sock.recv(BUFFER_SIZE)
            if not chunk:
                break
            target.write(chunk)
            received += len(chunk)
    if received >= filesize:
        print("The file has been completely transferred.")
    else:
        print("Download interrupted before completion.")


def main() -> None:
    host = input("Enter Server name : ")
    port = 5000

    with socket.create_connection((host, port)) as sock:
        print("Connected!")
        filename = input("File to download ? => ")
        if not filename:
            return

        sock.sendall(filename.encode())
        response = sock.recv(BUFFER_SIZE).decode()
        if not response.startswith("EXIST"):
            print("File does not Exist!")
            return

        filesize = int(response[5:])
        message = input(f"File Exists, {filesize} Bytes, download? (Y/N) -> ")
        if message.lower() not in {"y", "yes"}:
            return

        sock.sendall(b"OK")
        download_file(sock, filename, filesize)


if __name__ == "__main__":
    main()
