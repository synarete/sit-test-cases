#!/usr/bin/env python3

# Test mounts a cifs share, creates a new file on it, writes to it,
# deletes the file and unmounts

import testhelper
import os
import sys
import pytest
import typing
import shutil

from .mount_io import check_io_consistency
from .mount_dbm import check_dbm_consistency

# Use a global test_info to get a better output when running pytest
test_info: typing.Dict[str, typing.Any] = {}


def _get_test_dirs(
    mount_params: typing.Dict[str, str]
) -> typing.Tuple[str, str, str, bool]:
    test_dir = mount_params.get("test_dir", "")
    if not test_dir:
        tmp_root = testhelper.get_tmp_root()
        mount_point = testhelper.get_tmp_mount_point(tmp_root)
        test_dir = mount_point + "/mount_test"
        do_mnt = True
    else:
        tmp_root = ""
        mount_point = ""
        do_mnt = False
    return (tmp_root, mount_point, test_dir, do_mnt)


def _check_mounted_smbshare(test_dir: str) -> None:
    check_io_consistency(test_dir)
    check_dbm_consistency(test_dir)


def _mount_and_check(
    mount_params: typing.Dict[str, str],
    tmp_root: str,
    mount_point: str,
    test_dir: str,
) -> None:
    flag_mounted = False
    try:
        testhelper.cifs_mount(mount_params, mount_point)
        flag_mounted = True
        os.mkdir(test_dir)
        _check_mounted_smbshare(test_dir)
    finally:
        if flag_mounted:
            shutil.rmtree(test_dir, ignore_errors=True)
            testhelper.cifs_umount(mount_point)
        os.rmdir(mount_point)
        os.rmdir(tmp_root)


def mount_check(ipaddr: str, share_name: str) -> None:
    mount_params = testhelper.get_mount_parameters(test_info, share_name)
    mount_params["host"] = ipaddr
    (tmp_root, mount_point, test_dir, do_mnt) = _get_test_dirs(mount_params)
    if do_mnt:
        _mount_and_check(mount_params, tmp_root, mount_point, test_dir)
    else:
        _check_mounted_smbshare(test_dir)


def generate_mount_check(
    test_info_file: typing.Optional[str],
) -> typing.List[typing.Tuple[str, str]]:
    global test_info
    if not test_info_file:
        return []
    test_info = testhelper.read_yaml(test_info_file)
    arr = []
    for ipaddr in test_info["public_interfaces"]:
        for share_name in test_info["exported_sharenames"]:
            arr.append((ipaddr, share_name))
    return arr


@pytest.mark.parametrize(
    "ipaddr,share_name", generate_mount_check(os.getenv("TEST_INFO_FILE"))
)
def test_mount(ipaddr: str, share_name: str) -> None:
    mount_check(ipaddr, share_name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s <test-info.yml>" % (sys.argv[0]))
        exit(1)
    test_info_file = sys.argv[1]
    print("Running mount check:")
    for ipaddr, share_name in generate_mount_check(test_info_file):
        print("%s - %s" % (ipaddr, share_name))
        mount_check(ipaddr, share_name)
