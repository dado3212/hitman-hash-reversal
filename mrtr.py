from utils import hashcat, load_data
from typing import Dict, Optional
import string

data = load_data()

names: set[str] = set()
to_crack: Dict[str, Optional[str]] = {}

