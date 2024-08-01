import paramiko
import pytest
import os
import time

def run_command_over_ssh(host, usename, password, command, text):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=usename, password=password)

        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode()
        error = stderr.read().decode()
        return_code = stdout.channel.recv_exit_status()

        ssh.close()

        if return_code == 0:
            return text in output
        
        else:
            print(f"Command error: {error}")
            return False
    except Exception as e:   
            print(f"Error executing SSH command: {e}")
            return False
    
@pytest.fixture(autouse=True)
def log_statistics():
     with open('stat.txt', 'a') as f:
          with open('/proc/loadavg', 'r') as loadavg_file:
            loadavg = loadavg_file.read().strip()
        
        
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        
            try:
                with open('config.txt', 'r') as config_file:
                    config_data = config_file.readlines()
                    number_of_files = len(config_data)  
                    file_size = os.path.getsize(config_data[0].strip()) if config_data else 0  
            except FileNotFoundError:
                number_of_files = 0
                ile_size = 0
        
      
            f.write(f"{current_time}, {number_of_files}, {file_size}, {loadavg}n")

def test_run_command_success_ssh():
    host = 'your_remote_host' 
    username = 'your_username'   
    password = 'your_password'
    result = run_command_over_ssh(host, username, password, 'echo Hello World', 'Hello')
    assert result == True

def test_run_command_failure_ssh():
    host = 'your_remote_host' 
    username = 'your_username'   
    password = 'your_password'  
    result = run_command_over_ssh(host, username, password, 'ls non_existent_file', 'Hello')
    assert result == False   

def test_run_command_failure_invalid_ssh():
    host = 'your_remote_host'
    username = 'your_username'
    password = 'your_password'
    result = run_command_over_ssh(host, username, password, 'invalid_command', 'Hello')
    assert result == False 
