from . import Publisher
import paramiko
import json
import tempfile
import os

class SftpPublisher:
    def __init__(self, hostname, port, username, password):
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(transport)

    async def publish(self, data):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmpfile:
            json.dump(data, tmpfile)
            tmpfile_path = tmpfile.name
        remote_path = '/path/on/remote/server/data.json'
        self.sftp.put(tmpfile_path, remote_path)
        print("Data uploaded via SFTP to", remote_path)
        os.unlink(tmpfile_path)  # Clean up the temporary file
