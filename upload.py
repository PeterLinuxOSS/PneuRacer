import paramiko
import os
import time
 
def sftp_upload(host, port, username, password, local, remote, sftp=None, transport=None):
    close_transport = False
    if sftp is None or transport is None:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        transport.banner_timeout = 200
        sftp = paramiko.SFTPClient.from_transport(transport)
        close_transport = True

    ignorelist = ["desktop.ini", "__init__.py", "__pycache__", "nextcord.log", "upload.py", "run.bat", ".pyc", "desktop.ini", ".code-workspace", ".vscode", "logs", "backups", "legacy.mp4", "video", "desktop.ini", ".git"]
    if os.path.isdir(local):
        print(os.listdir(local))
        for f in os.listdir(local):
            if f not in ignorelist:
                local_path = os.path.join(local, f)
                remote_path = os.path.join(remote, f).replace("\\", "/")
                if not os.path.isdir(local_path):
                    print("uploading:", local_path, remote_path)
                    sftp.put(local_path, remote_path)
                    continue
                try:
                    sftp.mkdir(remote_path)
                    print('mkdir:', remote_path)
                except Exception:
                    print("dir existing")
                for d in os.listdir(local_path):
                    sub_local_path = os.path.join(local_path, d)
                    sub_remote_path = os.path.join(remote_path, d).replace("\\", "/")
                    if os.path.isdir(sub_local_path):
                        sftp_upload(host, port, username, password, sub_local_path + os.sep, sub_remote_path + '/', sftp, transport)
                    else:
                        print("uploading:", sub_local_path, sub_remote_path)
                        sftp.put(sub_local_path, sub_remote_path)
    else:
        sftp.put(local, remote)

    if close_transport:
        channel = transport.open_channel(kind="session")
        while not channel.exit_status_ready():
            channel.exec_command("systemctl restart pneuracer")
            channel.close()

        # Corrected log streaming logic
        log_channel = transport.open_session()
        log_channel.exec_command("journalctl -u pneuracer -f --no-pager")
        print("Streaming Service Logs:")
        try:
            for line in iter(log_channel.makefile('r').readline, ""):
                print(line.strip())
        except KeyboardInterrupt:
            print("Log streaming interrupted by user.")
        finally:
            log_channel.close()

        transport.close()
 


if __name__ == '__main__': 
    local = os.getcwd() 
    local += "\\"
    sftp_upload('racer',22,'root','1199',local,'/home/pneu/src/')


