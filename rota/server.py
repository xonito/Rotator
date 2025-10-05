"""
Proxy server implementation for Rota
Simplified version using standard HTTP server
"""

import logging
import time
import threading
import http.server
import socketserver
import urllib.request
import urllib.parse
from typing import Optional
from http import HTTPStatus

from rota.config import Config
from rota.proxy_manager import ProxyManager
from rota.proxy import Proxy


class ProxyHTTPHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for proxy server"""
    
    def __init__(self, *args, proxy_manager: ProxyManager, config: Config, **kwargs):
        self.proxy_manager = proxy_manager
        self.config = config
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        self._handle_request()
    
    def do_POST(self):
        """Handle POST requests"""
        self._handle_request()
    
    def do_PUT(self):
        """Handle PUT requests"""
        self._handle_request()
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        self._handle_request()
    
    def do_HEAD(self):
        """Handle HEAD requests"""
        self._handle_request()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests"""
        self._handle_request()
    
    def _handle_request(self):
        """Handle all HTTP requests"""
        # Check rate limiting
        if not self._check_rate_limit():
            self.send_error(HTTPStatus.TOO_MANY_REQUESTS, "Rate limit exceeded")
            return
        
        # Get target URL
        target_url = self._get_target_url()
        if not target_url:
            self.send_error(HTTPStatus.BAD_REQUEST, "No target URL specified")
            return
        
        # Select proxy
        proxy = self.proxy_manager.get_proxy()
        if not proxy:
            self.send_error(HTTPStatus.SERVICE_UNAVAILABLE, "No healthy proxies available")
            return
        
        # Forward request
        try:
            proxy.connection_count += 1
            self._forward_request(target_url, proxy)
        except Exception as e:
            self.send_error(HTTPStatus.BAD_GATEWAY, f"Proxy error: {str(e)}")
        finally:
            proxy.connection_count -= 1
    
    def _check_rate_limit(self) -> bool:
        """Simple rate limiting"""
        if not self.config.rate_limit_enabled:
            return True
        
        # This is a simplified version - in production you'd want more sophisticated rate limiting
        current_time = time.time()
        elapsed = current_time - self.server.last_reset
        
        if elapsed >= 60:  # Reset every minute
            self.server.request_count = 0
            self.server.last_reset = current_time
        
        if self.server.request_count >= self.config.rate_limit_requests:
            return False
        
        self.server.request_count += 1
        return True
    
    def _get_target_url(self) -> Optional[str]:
        """Extract target URL from request"""
        # Check query parameter
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if 'target' in query_params:
            return query_params['target'][0]
        
        # Check path (for simple proxy usage)
        path = self.path
        if path.startswith('/http://') or path.startswith('/https://'):
            return path[1:]  # Remove leading slash
        
        # Check Host header for transparent proxy
        host = self.headers.get('Host')
        if host:
            scheme = 'https' if self.headers.get('X-Forwarded-Proto') == 'https' else 'http'
            return f"{scheme}://{host}{self.path}"
        
        return None
    
    def _forward_request(self, target_url: str, proxy: Proxy):
        """Forward request through proxy"""
        # Prepare headers
        headers = {}
        for key, value in self.headers.items():
            if key.lower() not in ['host', 'connection', 'proxy-connection']:
                headers[key] = value
        
        # Prepare request data
        content_length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(content_length) if content_length > 0 else None
        
        # Create proxy handler
        proxy_url = proxy.to_url()
        proxy_handler = urllib.request.ProxyHandler({
            'http': proxy_url,
            'https': proxy_url
        })
        
        opener = urllib.request.build_opener(proxy_handler)
        
        # Make the request
        req = urllib.request.Request(
            url=target_url,
            data=data,
            headers=headers,
            method=self.command
        )
        
        with opener.open(req, timeout=self.config.connection_timeout) as response:
            # Send response back to client
            self.send_response(response.status)
            
            # Copy headers
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()
            
            # Copy response body
            self.wfile.write(response.read())
    
    def log_message(self, format, *args):
        """Custom logging"""
        self.server.logger.info(format % args)


class ProxyServer:
    """HTTP proxy server with rotation capabilities"""
    
    def __init__(self, config: Config, proxy_manager: ProxyManager):
        self.config = config
        self.proxy_manager = proxy_manager
        self.server: Optional[socketserver.ThreadingTCPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.logger = logging.getLogger(__name__)
        
        # Rate limiting state
        self.request_count = 0
        self.last_reset = time.time()
    
    def start(self):
        """Start the proxy server"""
        # Create custom handler class with our dependencies
        handler_class = lambda *args: ProxyHTTPHandler(
            *args, 
            proxy_manager=self.proxy_manager, 
            config=self.config
        )
        
        self.server = socketserver.ThreadingTCPServer(
            (self.config.host, self.config.port),
            handler_class
        )
        
        # Add our attributes to the server instance
        self.server.request_count = self.request_count
        self.server.last_reset = self.last_reset
        self.server.logger = self.logger
        
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        self.logger.info(f"Proxy server started on {self.config.host}:{self.config.port}")
    
    def stop(self):
        """Stop the proxy server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.server_thread:
            self.server_thread.join(timeout=5)
    
    def get_stats(self) -> dict:
        """Get server statistics"""
        stats = self.proxy_manager.get_stats()
        stats.update({
            'request_count': self.request_count,
            'uptime': time.time() - self.last_reset
        })
        return stats