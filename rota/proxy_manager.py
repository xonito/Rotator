"""
Proxy management and health checking for Rota
Simplified version using only standard libraries and requests
"""

import logging
import time
import os
import threading
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import requests
from requests.exceptions import RequestException

from rota.config import Config
from rota.rotation_strategies import RotationStrategy
from rota.proxy import Proxy


class ProxyManager:
    """Manages proxy pool with health checking and rotation"""
    
    def __init__(self, config: Config):
        self.config = config
        self.proxies: List[Proxy] = []
        self.healthy_proxies: Set[Proxy] = set()
        self._lock = threading.Lock()
        self._health_check_thread: Optional[threading.Thread] = None
        self._running = False
        self.logger = logging.getLogger(__name__)
    
    def load_proxies(self) -> int:
        """Load proxies from configured files"""
        loaded_count = 0
        
        for proxy_file in self.config.proxy_files:
            try:
                count = self._load_proxies_from_file(proxy_file)
                loaded_count += count
                self.logger.info(f"Loaded {count} proxies from {proxy_file}")
            except Exception as e:
                self.logger.error(f"Failed to load proxies from {proxy_file}: {e}")
        
        if loaded_count > 0:
            self._comprehensive_health_check()
        
        return loaded_count
    
    def _load_proxies_from_file(self, file_path: str) -> int:
        """Load proxies from a single file"""
        count = 0
        
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    proxy = self._parse_proxy_line(line)
                    if proxy:
                        with self._lock:
                            # Check if proxy already exists
                            if not any(p.address == proxy.address and p.protocol == proxy.protocol 
                                     for p in self.proxies):
                                self.proxies.append(proxy)
                                count += 1
        except FileNotFoundError:
            self.logger.warning(f"Proxy file {file_path} not found")
        
        return count
    
    def _parse_proxy_line(self, line: str) -> Optional[Proxy]:
        """Parse a proxy line into a Proxy object"""
        try:
            # Handle different formats:
            # http://user:pass@host:port
            # socks5://host:port
            # host:port
            # protocol:host:port:user:pass
            
            if '://' in line:
                # URL format
                protocol, rest = line.split('://', 1)
                if '@' in rest:
                    auth, address = rest.split('@', 1)
                    if ':' in auth:
                        username, password = auth.split(':', 1)
                    else:
                        username, password = auth, None
                else:
                    address = rest
                    username, password = None, None
            else:
                # Simple format: host:port or protocol:host:port
                parts = line.split(':')
                if len(parts) >= 2:
                    if parts[0] in ['http', 'socks4', 'socks5']:
                        protocol = parts[0]
                        address = f"{parts[1]}:{parts[2]}"
                        username = parts[3] if len(parts) > 3 else None
                        password = parts[4] if len(parts) > 4 else None
                    else:
                        protocol = 'http'  # default protocol
                        address = line
                        username, password = None, None
            
            # Validate address format
            if ':' not in address:
                return None
            
            return Proxy(
                address=address,
                protocol=protocol,
                username=username,
                password=password
            )
            
        except Exception as e:
            self.logger.warning(f"Failed to parse proxy line '{line}': {e}")
            return None
    
    def _comprehensive_health_check(self):
        """Perform comprehensive health check on all proxies before startup"""
        self.logger.info("Starting comprehensive health check on all proxies...")
        
        healthy_count = 0
        total_count = len(self.proxies)
        
        with self._lock:
            for i, proxy in enumerate(self.proxies):
                if self._check_proxy_health(proxy):
                    healthy_count += 1
                
                # Log progress every 10% of proxies
                if (i + 1) % max(1, total_count // 10) == 0 or (i + 1) == total_count:
                    progress = ((i + 1) / total_count) * 100
                    self.logger.info(f"Health check progress: {progress:.1f}% ({i + 1}/{total_count})")
        
        self.logger.info(f"Comprehensive health check completed. {healthy_count}/{total_count} proxies healthy")
        
        # If no healthy proxies found, log warning
        if healthy_count == 0 and total_count > 0:
            self.logger.warning("No healthy proxies found! The server may not function properly.")
        
        return healthy_count
    
    def _check_all_proxies(self):
        """Check health of all proxies (for periodic checks)"""
        with self._lock:
            for proxy in self.proxies:
                self._check_proxy_health(proxy)
    
    def _check_proxy_health(self, proxy: Proxy) -> bool:
        """Check if a proxy is healthy with enhanced error handling"""
        try:
            start_time = time.time()
            
            # Use requests with proxy
            proxy_url = proxy.to_url()
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # Set appropriate headers to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive'
            }
            
            response = requests.get(
                self.config.health_check_url,
                proxies=proxies,
                timeout=self.config.health_check_timeout,
                headers=headers,
                verify=False  # For testing purposes
            )
            
            if response.status_code == 200:
                proxy.response_time = time.time() - start_time
                proxy.is_healthy = True
                proxy.last_checked = time.time()
                self.healthy_proxies.add(proxy)
                
                # Log successful health check for first few proxies or periodically
                if len(self.healthy_proxies) <= 5 or time.time() % 60 < 5:
                    self.logger.info(f"Proxy {proxy} is healthy (response time: {proxy.response_time:.3f}s)")
                
                return True
            else:
                self.logger.debug(f"Proxy {proxy} returned status code {response.status_code}")
            
        except requests.exceptions.ConnectTimeout:
            self.logger.debug(f"Proxy {proxy} connection timeout")
        except requests.exceptions.ReadTimeout:
            self.logger.debug(f"Proxy {proxy} read timeout")
        except requests.exceptions.ConnectionError as e:
            self.logger.debug(f"Proxy {proxy} connection error: {e}")
        except requests.exceptions.ProxyError as e:
            self.logger.debug(f"Proxy {proxy} proxy error: {e}")
        except requests.exceptions.SSLError as e:
            self.logger.debug(f"Proxy {proxy} SSL error: {e}")
        except RequestException as e:
            self.logger.debug(f"Proxy {proxy} general error: {e}")
        except Exception as e:
            self.logger.warning(f"Unexpected error checking proxy {proxy}: {e}")
        
        proxy.is_healthy = False
        proxy.last_checked = time.time()
        if proxy in self.healthy_proxies:
            self.healthy_proxies.remove(proxy)
        
        return False
    
    def start_health_check(self):
        """Start periodic health checking"""
        if self.config.health_check_enabled:
            self._running = True
            self._health_check_thread = threading.Thread(target=self._health_check_loop)
            self._health_check_thread.daemon = True
            self._health_check_thread.start()
    
    def _health_check_loop(self):
        """Continuous health checking loop with staggered checks"""
        check_cycle = 0
        
        while self._running:
            try:
                time.sleep(self.config.health_check_interval)
                check_cycle += 1
                
                # Log periodic status
                if check_cycle % 10 == 0:  # Every 10 cycles
                    stats = self.get_stats()
                    self.logger.info(
                        f"Periodic health check status - "
                        f"Total: {stats['total_proxies']}, "
                        f"Healthy: {stats['healthy_proxies']}, "
                        f"Unhealthy: {stats['unhealthy_proxies']}"
                    )
                
                # Check all proxies but in a staggered manner
                with self._lock:
                    total_proxies = len(self.proxies)
                    if total_proxies > 0:
                        # Check a subset of proxies each cycle to spread the load
                        proxies_to_check = min(self.config.max_proxies_per_check, total_proxies)
                        
                        # Get proxies that haven't been checked recently
                        current_time = time.time()
                        proxies_needing_check = [
                            p for p in self.proxies
                            if current_time - (p.last_checked or 0) > self.config.health_check_interval
                        ]
                        
                        if proxies_needing_check:
                            # Check the oldest unchecked proxies first
                            proxies_needing_check.sort(key=lambda p: p.last_checked or 0)
                            proxies_to_check_now = proxies_needing_check[:proxies_to_check]
                            
                            for proxy in proxies_to_check_now:
                                self._check_proxy_health(proxy)
                        else:
                            # If all proxies are recently checked, do a random sample
                            import random
                            sample_size = min(proxies_to_check, total_proxies)
                            proxies_to_check_now = random.sample(self.proxies, sample_size)
                            
                            for proxy in proxies_to_check_now:
                                self._check_proxy_health(proxy)
                
                # Remove old proxies periodically
                if check_cycle % 5 == 0:  # Every 5 cycles
                    current_time = time.time()
                    with self._lock:
                        old_count = len(self.proxies)
                        self.proxies = [
                            p for p in self.proxies 
                            if current_time - p.added_at < self.config.proxy_max_age
                        ]
                        removed = old_count - len(self.proxies)
                        if removed > 0:
                            self.logger.info(f"Removed {removed} old proxies")
                    
            except Exception as e:
                self.logger.error(f"Health check loop error: {e}")
                # Continue running despite errors
                time.sleep(5)
    
    def stop_health_check(self):
        """Stop health checking"""
        self._running = False
        if self._health_check_thread:
            self._health_check_thread.join(timeout=5)
    
    def get_proxy(self, strategy: RotationStrategy = RotationStrategy.RANDOM) -> Optional[Proxy]:
        """Get a proxy based on rotation strategy"""
        with self._lock:
            healthy = list(self.healthy_proxies)
            
            if not healthy:
                return None
            
            if strategy == RotationStrategy.RANDOM:
                import random
                return random.choice(healthy)
            elif strategy == RotationStrategy.ROUND_ROBIN:
                # Simple round robin - get first and move to end
                proxy = healthy[0]
                # Move to end for next time
                if proxy in self.healthy_proxies:
                    self.healthy_proxies.remove(proxy)
                    self.healthy_proxies.add(proxy)
                return proxy
            elif strategy == RotationStrategy.LEAST_CONNECTIONS:
                return min(healthy, key=lambda p: p.connection_count)
            elif strategy == RotationStrategy.TIME_BASED:
                # Get proxy with oldest last check time
                return min(healthy, key=lambda p: p.last_checked or 0)
            else:
                return healthy[0]
    
    def get_stats(self) -> Dict:
        """Get proxy statistics"""
        with self._lock:
            return {
                'total_proxies': len(self.proxies),
                'healthy_proxies': len(self.healthy_proxies),
                'unhealthy_proxies': len(self.proxies) - len(self.healthy_proxies)
            }