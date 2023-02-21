import importlib as _importlib
if __name__ == "__main__":
    import inspect
    import os
    import sys
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../../../'))


_cipher = "origin"
try:
    import configloader as _configloader
    _c = _configloader.config()
    _new_cipher = _c.getkey("rsa_cipher")
    if _new_cipher:
        _cipher = _new_cipher
    _cipher_class = _importlib.import_module("tools.base.rsa_utils."+_cipher)
except ImportError:
    _cipher = "origin"
    _cipher_class = _importlib.import_module("tools.base.rsa_utils.origin")

rsa_utils = _cipher_class.rsa_utils
generate_rsa_keys = _cipher_class.generate_rsa_keys
__all__ = ["rsa_utils","generate_rsa_keys"]