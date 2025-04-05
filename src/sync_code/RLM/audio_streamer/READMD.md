
首先安装依赖包：
pip install -r requirements.txt

生成协议代码：
python build_protocol.py

在接收机器上启动服务器：
python audio_server.py

在发送机器上启动客户端：
python audio_client.py --server localhost:50051

netsh advfirewall firewall add rule name="Open Port 50051" dir=in action=allow protocol=TCP localport=50051

