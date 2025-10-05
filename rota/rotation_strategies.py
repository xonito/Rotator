"""
Proxy rotation strategies for Rota
"""

import random
import time
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

from rota.proxy import Proxy


class RotationStrategy(Enum):
    """Available proxy rotation strategies"""
    RANDOM = "random"
    ROUND_ROBIN = "roundrobin"
    LEAST_CONNECTIONS = "least_conn"
    TIME_BASED = "time_based"


# Global state for round-robin rotation
_round_robin_index = 0
_round_robin_lock = None


def get_random_proxy(proxies: List[Proxy]) -> Optional[Proxy]:
    """Select a random proxy from the list"""
    if not proxies:
        return None
    return random.choice(proxies)


def get_round_robin_proxy(proxies: List[Proxy]) -> Optional[Proxy]:
    """Select proxies in round-robin fashion"""
    global _round_robin_index
    
    if not proxies:
        return None
    
    proxy = proxies[_round_robin_index % len(proxies)]
    _round_robin_index += 1
    
    return proxy


def get_least_connections_proxy(proxies: List[Proxy]) -> Optional[Proxy]:
    """Select proxy with least number of active connections"""
    if not proxies:
        return None
    
    # Sort by connection count, then by response time
    sorted_proxies = sorted(
        proxies,
        key=lambda p: (p.connection_count, p.response_time or float('inf'))
    )
    
    return sorted_proxies[0]


def get_time_based_proxy(proxies: List[Proxy]) -> Optional[Proxy]:
    """Select proxy based on time-based rotation"""
    if not proxies:
        return None
    
    current_time = time.time()
    
    # Use current minute to determine index
    current_minute = int(current_time / 60)
    index = current_minute % len(proxies)
    
    return proxies[index]


def get_proxy_by_strategy(proxies: List[Proxy], strategy: RotationStrategy) -> Optional[Proxy]:
    """Get proxy using specified strategy"""
    if not proxies:
        return None
    
    if strategy == RotationStrategy.RANDOM:
        return get_random_proxy(proxies)
    elif strategy == RotationStrategy.ROUND_ROBIN:
        return get_round_robin_proxy(proxies)
    elif strategy == RotationStrategy.LEAST_CONNECTIONS:
        return get_least_connections_proxy(proxies)
    elif strategy == RotationStrategy.TIME_BASED:
        return get_time_based_proxy(proxies)
    else:
        return get_random_proxy(proxies)


class RotationStrategyFactory:
    """Factory for creating rotation strategy instances"""
    
    @staticmethod
    def create(strategy: RotationStrategy):
        """Create a rotation strategy instance"""
        if strategy == RotationStrategy.RANDOM:
            return RandomRotationStrategy()
        elif strategy == RotationStrategy.ROUND_ROBIN:
            return RoundRobinRotationStrategy()
        elif strategy == RotationStrategy.LEAST_CONNECTIONS:
            return LeastConnectionsRotationStrategy()
        elif strategy == RotationStrategy.TIME_BASED:
            return TimeBasedRotationStrategy()
        else:
            return RandomRotationStrategy()


class RotationStrategyBase:
    """Base class for rotation strategies"""
    
    def get_next(self, proxies: List[Proxy]) -> Optional[Proxy]:
        """Get next proxy from list"""
        raise NotImplementedError


class RandomRotationStrategy(RotationStrategyBase):
    """Random proxy selection"""
    
    def get_next(self, proxies: List[Proxy]) -> Optional[Proxy]:
        return get_random_proxy(proxies)


class RoundRobinRotationStrategy(RotationStrategyBase):
    """Round-robin proxy selection"""
    
    def __init__(self):
        self.index = 0
    
    def get_next(self, proxies: List[Proxy]) -> Optional[Proxy]:
        if not proxies:
            return None
        
        proxy = proxies[self.index % len(proxies)]
        self.index += 1
        return proxy


class LeastConnectionsRotationStrategy(RotationStrategyBase):
    """Select proxy with least connections"""
    
    def get_next(self, proxies: List[Proxy]) -> Optional[Proxy]:
        return get_least_connections_proxy(proxies)


class TimeBasedRotationStrategy(RotationStrategyBase):
    """Time-based proxy selection"""
    
    def get_next(self, proxies: List[Proxy]) -> Optional[Proxy]:
        return get_time_based_proxy(proxies)