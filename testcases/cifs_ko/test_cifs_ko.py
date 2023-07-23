#!/usr/bin/env python3

# Test various file-system operations via kernel's cifs.ko

import random
import datetime
import pathlib
import typing


class PathData:
    """A pair of path-name to file and its associated random data"""

    def __init__(self, path: pathlib.Path, size: int) -> None:
        self.path = path
        self.size = size
        self.renew_data()

    def renew_data(self) -> None:
        self.data = random.randbytes(self.size)

    def write(self) -> None:
        self.path.write_bytes(self.data)

    def read(self) -> bytes:
        return self.path.read_bytes()

    def mkdirs(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def unlink(self) -> None:
        self.path.unlink()

    def stat_size(self) -> int:
        return self.path.stat().st_size

    def verify_size(self) -> bool:
        return self.size == self.stat_size()

    def verify_data(self) -> bool:
        data = self.read()
        return len(data) == self.size and  data == self.data



def _make_pathname(base: pathlib.Path, idx: int) -> pathlib.Path:
    return base / str(idx)


def _make_datasets(
    base: pathlib.Path, size: int, count: int
) -> typing.List[PathData]:
    return [
        PathData(_make_pathname(base, idx), size) for idx in range(0, count)
    ]


def _run_test(base: pathlib.Path) -> None:
    dsets = _make_datasets(base, 1024 * 1024, 4)
    for dset in dsets:
        dset.mkdirs()
    for dset in dsets:
        dset.write()
    for dset in dsets:
        dset.read()

    for dset in dsets:
        if not dset.verify_data():
            print("data not eq")
    for dset in dsets:
        dset.do_unlink()


def _seed_random() -> None:
    now = datetime.datetime.now()
    seed = int(now.year * now.day * now.hour * now.minute / (now.second + 1))
    random.seed(seed)


def main() -> None:
    base = pathlib.Path("/mnt/cifs/A/B")
    _seed_random()
    _run_test(base)


if __name__ == "__main__":
    main()
