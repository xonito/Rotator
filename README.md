# Rota 🚀

**Lightning-fast, self-hosted proxy rotation powerhouse**

Rota is a high-performance proxy rotation server that revolutionizes how you manage and rotate proxies. Built with performance at its core, this robust tool handles thousands of requests per second while seamlessly rotating IPs to maintain your anonymity.

## ✨ Features

- 🚀 **Self-hosted solution** with complete control over your proxy infrastructure
- ⚡ **Blazing-fast performance** optimized for high-throughput operations
- 🔄 **Advanced proxy rotation** with intelligent IP management
  - Random rotation
  - Round-robin rotation
  - Least connections rotation
  - Time-based rotation
- 🤖 **Automatic proxy pool management** with real-time file monitoring
- 🌍 **Multi-protocol support**: HTTP, SOCKS v4(A) & v5
- ✅ **Built-in proxy checker** to maintain a healthy proxy pool
- 🔒 **Rate limiting** to prevent abuse
- 🌐 **Perfect companion** for web scraping and data collection projects
- 🔍 **Cross-platform compatibility** (Windows, Linux, Mac, Raspberry Pi)
- 🔗 **Easy integration** with upstream proxies and proxy chains

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd rota
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your proxies**:
   Edit `proxies.txt` with your proxy list:
   ```
   http://user:pass@proxy1.example.com:8080
   socks5://proxy2.example.com:1080
   socks4://user:pass@proxy3.example.com:1080
   ```

4. **Start the server**:
   ```bash
   python main.py
   ```

### Basic Usage

```bash
# Start with default configuration
python main.py

# Start with custom config file
python main.py -c config.yaml

# Start on specific host and port
python main.py --host 0.0.0.0 --port 9090

# Use specific proxy file
python main.py --proxy-file my_proxies.txt
```

## 📋 Configuration

Rota uses YAML configuration. See `config.yaml` for all options:

```yaml
server:
  host: "127.0.0.1"
  port: 8080
  max_connections: 1000
  connection_timeout: 30

proxy:
  files:
    - "proxies.txt"
  rotation_strategy: "random"  # random, roundrobin, least_conn, time_based
  max_proxy_age: 3600
  check_interval: 300

health_check:
  enabled: true
  url: "http://httpbin.org/ip"
  timeout: 10
  interval: 60

rate_limit:
  enabled: true
  requests_per_minute: 100
  burst_capacity: 50

logging:
  level: "INFO"
  file: "rota.log"

file_monitor:
  interval: 30
```

## 🔄 Rotation Strategies

Rota supports multiple rotation strategies:

1. **`random`** - Selects a random proxy from the healthy pool
2. **`roundrobin`** - Cycles through proxies in sequence
3. **`least_conn`** - Selects the proxy with the fewest active connections
4. **`time_based`** - Rotates proxies based on current time

## 🌐 Protocol Support

Rota supports all major proxy protocols:

- **HTTP/HTTPS proxies**
- **SOCKS v4** and **SOCKS v4A**
- **SOCKS v5**

### Proxy Format Examples

```
# HTTP with authentication
http://username:password@proxy.example.com:8080

# HTTP without authentication
http://proxy.example.com:8080

# SOCKS5 with authentication
socks5://username:password@proxy.example.com:1080

# SOCKS4
socks4://proxy.example.com:1080

# Simple format (defaults to HTTP)
proxy.example.com:8080
username:password@proxy.example.com:8080
```

## 🔧 Integration Examples

### Python Requests

```python
import requests

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

response = requests.get('https://example.com', proxies=proxies)
print(response.text)
```

### cURL

```bash
curl -x http://127.0.0.1:8080 https://example.com
```

### Web Scraping with Scrapy

```python
# settings.py
ROTATING_PROXY_LIST = ['http://127.0.0.1:8080']
DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}
```

### Burp Suite Integration

1. Configure Burp Suite to use Rota as an upstream proxy
2. Set Rota's address as the proxy server
3. All Burp traffic will be rotated through Rota's proxy pool

## 📊 Monitoring and Logging

Rota provides comprehensive logging:

- **Real-time health checks** of all proxies
- **Connection statistics** and performance metrics
- **File change monitoring** for automatic proxy list updates
- **Rate limit enforcement** and tracking

Logs are written to `rota.log` by default.

## 🚀 Performance Features

- **Asynchronous I/O** for high concurrency
- **Connection pooling** for reduced latency
- **Memory-efficient** proxy management
- **Zero-downtime** proxy rotation
- **Automatic failover** to healthy proxies

## 🔒 Security Features

- **Rate limiting** to prevent abuse
- **Proxy authentication** support
- **SSL/TLS** support for secure connections
- **No data logging** for privacy protection

## 🐳 Docker Support

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["python", "main.py", "--host", "0.0.0.0"]
```

```bash
docker build -t rota .
docker run -p 8080:8080 -v $(pwd)/proxies.txt:/app/proxies.txt rota
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: This README
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

## 🚀 Enterprise Features

Rota is designed for enterprise use with:

- **High availability** configurations
- **Load balancing** across multiple instances
- **API endpoints** for monitoring and management
- **Integration hooks** for existing infrastructure

---

**Rota** - Because your proxies deserve better rotation. 🚀