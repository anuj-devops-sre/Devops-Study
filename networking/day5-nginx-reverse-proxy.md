# 🌐 Day 5: Nginx Reverse Proxy

Nginx is a high-performance web server and reverse proxy.

## 🛠️ Key Features
- Reverse Proxying
- Load Balancing
- SSL Termination
- Caching

## ⚙️ Basic Configuration
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend_server;
    }
}
```
