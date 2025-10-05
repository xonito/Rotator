#!/usr/bin/env python3
"""
Rota - Lightning-fast proxy rotation powerhouse

A self-hosted proxy rotation tool with advanced IP management,
multiple rotation strategies, and enterprise-grade features.
"""

import logging
import signal
import sys
import time
import threading
from typing import Dict, List, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import urllib.request
import urllib.parse

from rota.config import Config
from rota.proxy_manager import ProxyManager


class Rota:
    """Main Rota application class"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = Config.from_file(config_path)
        self.proxy_manager = ProxyManager(self.config)
        self.server: Optional[HTTPServer] = None
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging based on config"""
        log_level = getattr(logging, self.config.log_level.upper())
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(self.config.log_file)
            ]
        )
    
    def start(self):
        """Start the Rota proxy server"""
        logger = logging.getLogger(__name__)
        
        try:
            # Load initial proxies
            self.proxy_manager.load_proxies()
            
            # Start proxy health checking
            self.proxy_manager.start_health_check()
            
            # File monitoring is handled by the health check loop
            
            # Create and start server
            from rota.server import ProxyServer
            self.server = ProxyServer(self.config, self.proxy_manager)
            self.server.start()
            
            logger.info(f"Rota server started on {self.config.host}:{self.config.port}")
            logger.info(f"Rotation strategy: {self.config.rotation_strategy}")
            stats = self.proxy_manager.get_stats()
            logger.info(f"Active proxies: {stats['healthy_proxies']}/{stats['total_proxies']}")
            
            # Keep the server running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            
        except Exception as e:
            logger.error(f"Failed to start Rota: {e}")
            raise
    
    def stop(self):
        """Gracefully stop the Rota server"""
        logger = logging.getLogger(__name__)
        logger.info("Shutting down Rota...")
        
        if self.server:
            self.server.shutdown()
        
        if self.proxy_manager:
            self.proxy_manager.stop()
        
        logger.info("Rota stopped gracefully")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Rota - Proxy Rotation Server")
    parser.add_argument("-c", "--config", help="Path to config file")
    parser.add_argument("--host", help="Server host address")
    parser.add_argument("--port", type=int, help="Server port")
    parser.add_argument("--proxy-file", help="Path to proxy list file")
    parser.add_argument("--menu", action="store_true", help="Launch menu system")
    
    args = parser.parse_args()
    
    if args.menu:
        # Launch menu system
        try:
            from menu_system import main_menu
            main_menu()
        except ImportError:
            print("Menu system not available. Running in command line mode.")
            run_command_line(args)
    else:
        run_command_line(args)

def run_command_line(args):
    """Run in traditional command line mode"""
    # Create Rota instance
    rota = Rota(args.config)
    
    # Override config from command line if provided
    if args.host:
        rota.config.host = args.host
    if args.port:
        rota.config.port = args.port
    if args.proxy_file:
        rota.config.proxy_files = [args.proxy_file]
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logging.info(f"Received signal {sig}, shutting down...")
        rota.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        rota.start()
    except KeyboardInterrupt:
        rota.stop()


if __name__ == "__main__":
    main()