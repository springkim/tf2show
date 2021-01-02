import inspect
import os
import sys

real_path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
sys.path.append(real_path)

try:
    from tf2show.tf2show import *
except ImportError as e:
    print(e, "Import Error")
    exit(1)

__all__ = [name for name, obj in locals().items()
           if not (name.startswith('_') or inspect.ismodule(obj))]
