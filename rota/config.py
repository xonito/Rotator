"""
Configuration management for Rota proxy rotation server
"""

import os
import yaml
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class RotationStrategy(Enum):
    """Available proxy rotation strategies"""
    RANDOM = "random"
    ROUND_ROBIN = "roundrobin"
    LEAST_CONNECTIONS = "least_conn"
    TIME_BASED = "time_based"


@dataclass
class Config:
    """Rota configuration class"""
    
    # Server configuration
    host: str = "127.0.0.1"
    port: int = 8080
    max_connections: int = 1000
    connection_timeout: int = 30
    
    # Proxy configuration
    proxy_files: List[str] = None
    rotation_strategy: RotationStrategy = RotationStrategy.RANDOM
    max_proxy_age: int = 3600  # 1 hour in seconds
    proxy_check_interval: int = 300  # 5 minutes
    
    # Health checking
    health_check_enabled: bool = True
    health_check_url: str = "http://httpbin.org/ip"
    health_check_timeout: int = 10
    health_check_interval: int = 60  # 1 minute
    max_proxies_per_check: int = 100  # Max proxies to check per health check cycle
    
    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100  # requests per minute
    rate_limit_burst: int = 50  # burst capacity
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "rota.log"
    
    # File monitoring
    file_monitor_interval: int = 30  # seconds
    
    def __post_init__(self):
        if self.proxy_files is None:
            self.proxy_files = ["proxies.txt"]
    
    @classmethod
    def from_file(cls, config_path: Optional[str] = None) -> 'Config':
        """Load configuration from YAML file"""
        config = cls()
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f) or {}
                
                # Server settings
                if 'server' in config_data:
                    server = config_data['server']
                    config.host = server.get('host', config.host)
                    config.port = server.get('port', config.port)
                    config.max_connections = server.get('max_connections', config.max_connections)
                    config.connection_timeout = server.get('connection_timeout', config.connection_timeout)
                
                # Proxy settings
                if 'proxy' in config_data:
                    proxy = config_data['proxy']
                    config.proxy_files = proxy.get('files', config.proxy_files)
                    strategy = proxy.get('rotation_strategy')
                    if strategy:
                        config.rotation_strategy = RotationStrategy(strategy)
                    config.max_proxy_age = proxy.get('max_proxy_age', config.max_proxy_age)
                    config.proxy_check_interval = proxy.get('check_interval', config.proxy_check_interval)
                
                # Health check settings
                if 'health_check' in config_data:
                    health = config_data['health_check']
                    config.health_check_enabled = health.get('enabled', config.health_check_enabled)
                    config.health_check_url = health.get('url', config.health_check_url)
                    config.health_check_timeout = health.get('timeout', config.health_check_timeout)
                    config.health_check_interval = health.get('interval', config.health_check_interval)
                    config.max_proxies_per_check = health.get('max_proxies_per_check', config.max_proxies_per_check)
                
                # Rate limiting settings
                if 'rate_limit' in config_data:
                    rate = config_data['rate_limit']
                    config.rate_limit_enabled = rate.get('enabled', config.rate_limit_enabled)
                    config.rate_limit_requests = rate.get('requests_per_minute', config.rate_limit_requests)
                    config.rate_limit_burst = rate.get('burst_capacity', config.rate_limit_burst)
                
                # Logging settings
                if 'logging' in config_data:
                    logging = config_data['logging']
                    config.log_level = logging.get('level', config.log_level)
                    config.log_file = logging.get('file', config.log_file)
                
                # File monitoring
                if 'file_monitor' in config_data:
                    monitor = config_data['file_monitor']
                    config.file_monitor_interval = monitor.get('interval', config.file_monitor_interval)
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for serialization"""
        return {
            'server': {
                'host': self.host,
                'port': self.port,
                'max_connections': self.max_connections,
                'connection_timeout': self.connection_timeout
            },
            'proxy': {
                'files': self.proxy_files,
                'rotation_strategy': self.rotation_strategy.value,
                'max_proxy_age': self.max_proxy_age,
                'check_interval': self.proxy_check_interval
            },
            'health_check': {
                'enabled': self.health_check_enabled,
                'url': self.health_check_url,
                'timeout': self.health_check_timeout,
                'interval': self.health_check_interval,
                'max_proxies_per_check': self.max_proxies_per_check
            },
            'rate_limit': {
                'enabled': self.rate_limit_enabled,
                'requests_per_minute': self.rate_limit_requests,
                'burst_capacity': self.rate_limit_burst
            },
            'logging': {
                'level': self.log_level,
                'file': self.log_file
            },
            'file_monitor': {
                'interval': self.file_monitor_interval
            }
        }
    
    def save(self, config_path: str):
        """Save configuration to YAML file"""
        config_dict = self.to_dict()
        with open(config_path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False)