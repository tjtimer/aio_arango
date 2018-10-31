"""
conftest
author: Tim "tjtimer" Jedro
created: 24.10.18
"""
from string import ascii_letters

alphabet = [*ascii_letters.upper(), *ascii_letters.lower(), *[str(i) for i in range(10)], '-', '_']
