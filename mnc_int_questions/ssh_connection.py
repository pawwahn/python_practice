import paramiko
from paramiko import SSHClient
def run():
    print("run method called")
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('10.197.75.232',32770,'root','cisco')
    #client = client.get_transport().open_session()

    output = client.exec_command('touch pavan.txt')
    client.exec_command('cat pavan.txt')
    print(output)

    client.close()


if __name__ == '__main__':
    print("Main")
    run()


#####-----------------------------
import paramiko
from paramiko import SSHClient

client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('host','port','username','pwd')
output = client.exec_command('touch pavan.txt')
print(output)

