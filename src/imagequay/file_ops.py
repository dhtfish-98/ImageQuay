"""User-requested local I/O with snapshots and atomic, private output files.

The CLI may replace an existing regular output only with --overwrite. Names
from binary metadata must pass `metadata_leaf`; they cannot select directories.
"""
import contextvars
import io
import os
from pathlib import Path
import stat
import tempfile

from imagequay.container_io import MAX_INPUT_BYTES
from imagequay.failure_types import quay_MalformedMachOException

_allow_overwrite = contextvars.ContextVar('imagequay_allow_overwrite', default=False)


def set_overwrite(allowed):
    return _allow_overwrite.set(bool(allowed))


def metadata_leaf(name):
    if not isinstance(name, str) or not name or name in ('.', '..'):
        raise ValueError('metadata output name must be a nonempty file name')
    if any(character in name for character in ('/', '\\', '\x00')) or any(ord(character) < 32 or ord(character) == 127 for character in name):
        raise ValueError('metadata output name contains a path separator or control character')
    if len(name.encode('utf-8')) > 240:
        raise ValueError('metadata output name is too long')
    return name


class _OutputFile:
    def __init__(self, path, mode):
        self.path = Path(path)
        self.overwrite = _allow_overwrite.get()
        self.stage = None
        self.stream = None
        self._descriptor = None
        self.closed = False
        self._published = False
        self._check_existing()
        try:
            descriptor, stage = tempfile.mkstemp(prefix='.imagequay-', dir=self.path.parent)
            self.stage = Path(stage)
            self._descriptor = descriptor
            os.fchmod(descriptor, 0o600)
            # Ownership transfers only after fdopen returns successfully.
            self.stream = os.fdopen(descriptor, 'w+b')
            self._descriptor = None
            if mode == 'w':
                self.stream = io.TextIOWrapper(self.stream, encoding='utf-8', newline='\n')
        except BaseException:
            self._discard()
            raise

    def _check_existing(self):
        try:
            mode = self.path.lstat().st_mode
        except FileNotFoundError:
            return
        if not self.overwrite:
            raise FileExistsError(f'output already exists: {self.path}; choose a new name or use --overwrite')
        if not stat.S_ISREG(mode):
            raise OSError('output replacement requires an existing regular file, never a symlink or device')

    def __getattr__(self, name):
        stream = self.__dict__.get('stream')
        if stream is None:
            raise AttributeError(name)
        return getattr(stream, name)

    def write(self, data):
        expected = len(data.encode('utf-8')) if isinstance(data, str) else len(data)
        if self.stream.tell() + expected > MAX_INPUT_BYTES:
            raise quay_MalformedMachOException('output exceeds the 1 GiB budget')
        return self.stream.write(data)

    def seek(self, offset, whence=os.SEEK_SET):
        # Binary combine writes use absolute offsets from its verified output plan.
        if whence != os.SEEK_SET or type(offset) is not int or not 0 <= offset <= MAX_INPUT_BYTES:
            raise ValueError('output seek requires an absolute position within the 1 GiB budget')
        return self.stream.seek(offset, whence)

    def __enter__(self):
        return self

    def _discard(self):
        stream = self.__dict__.get('stream')
        descriptor = self.__dict__.get('_descriptor')
        self.stream, self._descriptor = None, None
        try:
            if stream is not None:
                stream.close()
        finally:
            try:
                if descriptor is not None:
                    try:
                        os.close(descriptor)
                    except OSError:
                        pass
            finally:
                if self.stage is not None:
                    self.stage.unlink(missing_ok=True)
                    self.stage = None
                self.closed = True

    def close(self):
        if self.closed:
            return
        try:
            self.stream.flush()
            if os.fstat(self.stream.fileno()).st_size > MAX_INPUT_BYTES:
                raise quay_MalformedMachOException('output exceeds the 1 GiB budget')
            os.fsync(self.stream.fileno())
            self.stream.close()
            self._check_existing()
            if self.overwrite:
                os.replace(self.stage, self.path)
            else:
                # Atomic no-clobber publication, including concurrent creators.
                os.link(self.stage, self.path)
                self.stage.unlink()
            self.stage = None
            self._published = True
            self.closed = True
        except BaseException:
            self._discard()
            raise

    def __exit__(self, error_type, error, traceback):
        if error_type is None:
            self.close()
        else:
            self._discard()
        return False

    def __del__(self):
        if getattr(self, 'stage', None) is not None:
            self._discard()


def safe_open(path, mode='rb'):
    if mode in ('wb', 'w'):
        return _OutputFile(path, mode)
    if mode != 'rb':
        raise ValueError('ImageQuay local I/O supports rb, wb and UTF-8 w only')
    descriptor = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0))
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise OSError('input must be a regular file')
        if info.st_size > MAX_INPUT_BYTES:
            raise quay_MalformedMachOException('input exceeds the 1 GiB budget')
        return os.fdopen(descriptor, 'rb')
    except BaseException:
        os.close(descriptor)
        raise
