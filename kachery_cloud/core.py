from typing import Any, Union

from .store_file import store_file
from .load_file import load_file
from .store_file_local import store_file_local
from .TemporaryDirectory import TemporaryDirectory
from ._safe_pickle import _safe_pickle, _safe_unpickle
    
def store_text(text: str, *, label: Union[str, None]=None, cache_locally: bool=False) -> str:
    with TemporaryDirectory() as tmpdir:
        fname = f'{tmpdir}/file.dat'
        with open(fname, 'w') as f:
            f.write(text)
        return store_file(fname, label=label, cache_locally=cache_locally)

def store_json(x: Any, *, separators=(',', ':'), indent=None, label: Union[str, None]=None, cache_locally: bool=False) -> str:
    import simplejson
    text = simplejson.dumps(x, separators=separators, indent=indent, allow_nan=False, sort_keys=True)
    return store_text(text, label=label, cache_locally=cache_locally)

def store_npy(array: Any, *, label: Union[str, None]=None, cache_locally: bool=False) -> str:
    import numpy as np
    with TemporaryDirectory() as tmpdir:
        fname = f'{tmpdir}/file.npy'
        np.save(fname, array, allow_pickle=False)
        return store_file(fname, label=label, cache_locally=cache_locally)

def store_pkl(x: Any, *, label: Union[str, None]=None, cache_locally: bool=False) -> str:
    with TemporaryDirectory() as tmpdir:
        fname = f'{tmpdir}/file.npy'
        _safe_pickle(fname, x)
        return store_file(fname, label=label, cache_locally=cache_locally)

def load_text(uri: str, *, local_only: bool=False) -> Union[str, None]:
    local_path = load_file(uri, local_only=local_only)
    if local_path is None:
        return None
    with open(local_path, 'r') as f:
        return f.read()

def load_json(uri: str, *, local_only: bool=False) -> Union[dict, None]:
    import simplejson
    local_path = load_file(uri, local_only=local_only)
    if local_path is None:
        return None
    with open(local_path, 'r') as f:
        return simplejson.load(f)

def load_npy(uri: str, *, local_only: bool=False) -> Union[Any, None]:
    import numpy as np
    local_path = load_file(uri, local_only=local_only)
    if local_path is None:
        return None
    return np.load(local_path, allow_pickle=False)

def load_pkl(uri: str, *, local_only: bool=False) -> Union[Any, None]:
    local_path = load_file(uri, local_only=local_only)
    if local_path is None:
        return None
    return _safe_unpickle(local_path)

def store_text_local(text: str, label: Union[str, None]=None) -> str:
    with TemporaryDirectory() as tmpdir:
        fname = f'{tmpdir}/file.dat'
        with open(fname, 'w') as f:
            f.write(text)
        return store_file_local(fname, label=label)

def store_json_local(x: Any, *, separators=(',', ':'), indent=None, label: Union[str, None]=None) -> str:
    import simplejson
    text = simplejson.dumps(x, separators=separators, indent=indent, allow_nan=False, sort_keys=True)
    return store_text_local(text, label=label)

def store_npy_local(array: Any, label: Union[str, None]=None) -> str:
    import numpy as np
    with TemporaryDirectory() as tmpdir:
        fname = f'{tmpdir}/file.npy'
        np.save(fname, array, allow_pickle=False)
        return store_file_local(fname, label=label)

def store_pkl_local(x: Any, label: Union[str, None]=None) -> str:
    with TemporaryDirectory() as tmpdir:
        fname = f'{tmpdir}/file.npy'
        _safe_pickle(fname, x)
        return store_file_local(fname, label=label)