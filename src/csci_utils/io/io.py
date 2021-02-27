import os
from contextlib import contextmanager
from typing import ContextManager, Union
from datetime import datetime as dt
from builtins import FileExistsError
import warnings



@contextmanager
def atomic_write(
    file: Union[str, os.PathLike], mode: str = "w", as_file: bool = True, **kwargs
) -> ContextManager:
    """Write a file atomically

    :param file: str or :class:`os.PathLike` target to write
    :param mode: the mode in which the file is opened, defaults to "w" (writing in text mode)
    :param bool as_file:  if True, the yielded object is a :class:File.
        (eg, what you get with `open(...)`).  Otherwise, it will be the
        temporary file path string

    :param kwargs: anything else needed to open the file

    :raises: FileExistsError if target exists

    Example::

        with atomic_write("hello.txt") as f:
            f.write("world!")

    """
    dir_path = os.path.dirname(os.path.realpath(file))
    file_name = os.path.basename(file)
    temp_file_name = os.path.join(dir_path, '.temp' + str(dt.now()).encode('ascii').hex()[:6] + file_name)

    try:
        temp_file = open(temp_file_name, mode)
        if os.path.exists(file):
            print('Writing unsuccessful, file already exists!')
            yield None
        else:
            if as_file:
                yield temp_file
            else:
                yield temp_file_name
    except Exception as e:
        warnings.warn('Writing unsuccessful, aborted due to {}'.format(str(e)))
        temp_file.close()
        os.remove(temp_file_name)
    else: # instead of using finally, else is only called when no exception encountered
        temp_file.close()
        os.rename(temp_file_name, file)





if __name__ == '__main__': # pragma: no cover
    with atomic_write("hello.txt", as_file= False) as f:
        f.write("world!")
