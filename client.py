import socket
import threading
# 接收消息
def _recv(client):
    while True:
        recv_data = client.recv(1024)
        if not recv_data:
            break
        recv_content = recv_data.decode('utf-8')
        print(f'\n{recv_content}')
if __name__=='__main__':   
    flag = True
    # 创建套接字
    tcp_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 连接服务端
    tcp_client.connect(("",3344))
    send_data = input('send:')
    while True:
        if send_data=='q':
            break
        # 创建接收消息的子线程
        if flag:
            recv_thread = threading.Thread(target=_recv,args=(tcp_client,),daemon=True)
            # 启动线程
            recv_thread.start()
            flag = False
        # 发送消息
        send_content = send_data.encode('utf-8')
        tcp_client.send(send_content)
        send_data = input('send:')
    tcp_client.close()
