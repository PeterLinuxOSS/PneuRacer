import paramiko
import os
import time
 
def sftp_upload(host,port,username,password,local,remote):
    transport = paramiko.Transport((host,port))
    
    transport.connect(username = username,password = password)
    transport.banner_timeout =200
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    ignorelist = ["desktop.ini", "__init__.py","__pycache__","nextcord.log", "upload.py","run.bat",".pyc","desktop.ini",".code-workspace",".vscode","logs","backups","legacy.mp4","video","desktop.ini",".git"]
    if os.path.isdir(local):
        print(os.listdir(local))
        for f in os.listdir(local):
            if not f in ignorelist:
            
                if not os.path.isdir((os.path.join(local+f))):
                    print("uploading:",os.path.join(local+f),os.path.join(remote+f))
                    sftp.put(os.path.join(local+f),os.path.join(remote+f))
                    continue
                try:
                    print('mkdir: ',os.path.join(remote+f),"returning: ", sftp.mkdir(os.path.join(remote+f)))
                except:
                    print("dir existing")
                for d in os.listdir(os.path.join(local+f)):
                    if(os.path.isdir(os.path.join(local+f+"\\"+d))):
                        sftp_upload(host,port,username,password,local+f+"\\",remote+f+'/')
                        continue
                    print("uploading:",os.path.join(local+f+"\\"+d),os.path.join(remote+f+'/'+d))
                    sftp.put(os.path.join(local+f+"\\"+d),os.path.join(remote+f+'/'+d))
    else:
        sftp.put(local,remote)
    
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


