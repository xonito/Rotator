"""
Proxy data class for Rota
"""

import time
from typing import Optional
from dataclasses import dataclass


@dataclass
class Proxy:
    """Proxy representation"""
    address: str
    protocol: str  # http, socks4, socks5
    username: Optional[str] = None
    password: Optional[str] = None
    last_checked: Optional[float] = None
    is_healthy: bool = False
    response_time: Optional[float] = None
    connection_count: int = 0
    added_at: float = None
    
    def __post_init__(self):
        if self.added_at is None:
            self.added_at = time.time()
    
    def to_url(self) -> str:
        """Convert proxy to URL format"""
        if self.username and self.password:
            auth = f"{self.username}:{self.password}@"
        else:
            auth = ""
        
        return f"{self.protocol}://{auth}{self.address}"
    
    def __str__(self) -> str:
        return self.to_url()
    
    def __hash__(self):
        return hash((self.address, self.protocol, self.username, self.password))
    
    def __eq__(self, other):
        if not isinstance(other, Proxy):
            return False
        return (self.address == other.address and 
                self.protocol == other.protocol and 
                self.username == other.username and 
                self.password == other.password)