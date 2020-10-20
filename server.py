import socket
import threading

def new_thread(new_client,ip_port):
    while True:
        recv_data = new_client.recv(1024)
        # 判断客户端状态
        if not recv_data:
            print(f'{ip_port} --> 主人~ Ta离开了我们')
            del client_dict[ip_port]
            new_client.close()
            break
        recv_content = recv_data.decode('utf-8')
        print(f'{ip_port}:{recv_content}')
        # 同步聊天记录至其它客户端
        for i in client_dict.values():
            if i != new_client:
                send_data = f'{ip_port}:{recv_content}\n'
                send_content = send_data.encode('utf-8')
                i.send(send_content)

if __name__=='__main__':
    client_dict = {}
    # 创建套接字
    tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 复用端口,使之进程关闭，立即释放端口
    tcp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    # 绑定端口
    tcp_server.bind(('',3344))
    # 监听端口
    tcp_server.listen(128)
    while True:
        # 等待接收连接请求
        new_client,ip_port = tcp_server.accept()
        # 添加客户端套接字，以便同步聊天记录
        client_dict[ip_port] = new_client
        # 每收到一条连接请求，便创建一条子线程
        loli = threading.Thread(target=new_thread,args=(new_client,ip_port),daemon=True)
        # 启动线程
        loli.start()
