from smb.SMBConnection import SMBConnection  # type: ignore
from smb import smb_structs, base  # type: ignore
import typing
import io


class SMBClient:
    """Use pysmb to access the SMB server"""

    def __init__(self, hostname: str, share: str, username: str, passwd: str):
        self.server = hostname
        self.share = share
        self.username = username
        self.password = passwd
        self.connected = False
        self.connect()

    def connect(self) -> None:
        if self.connected:
            return
        try:
            self.ctx = SMBConnection(
                self.username,
                self.password,
                "smbclient",
                self.server,
                use_ntlm_v2=True,
            )
            self.ctx.connect(self.server)
            self.connected = True
        except base.SMBTimeout as error:
            raise IOError(f"failed to connect: {error}")

    def disconnect(self) -> None:
        self.connected = False
        self.ctx.close()

    def listdir(self, path: str = "/") -> typing.List[str]:
        try:
            dentries = self.ctx.listPath(self.share, path)
        except smb_structs.OperationFailure as error:
            raise IOError(f"failed to readdir: {error}")
        return [dent.filename for dent in dentries]

    def mkdir(self, dpath: str) -> None:
        try:
            self.ctx.createDirectory(self.share, dpath)
        except smb_structs.OperationFailure as error:
            raise IOError(f"failed to mkdir: {error}")

    def rmdir(self, dpath: str) -> None:
        try:
            self.ctx.deleteDirectory(self.share, dpath)
        except smb_structs.OperationFailure as error:
            raise IOError(f"failed to rmdir: {error}")

    def unlink(self, fpath: str) -> None:
        try:
            self.ctx.deleteFiles(self.share, fpath)
        except smb_structs.OperationFailure as error:
            raise IOError(f"failed to unlink: {error}")

    def write_text(self, fpath: str, teststr: str) -> None:
        try:
            with io.BytesIO(teststr.encode()) as writeobj:
                self.ctx.storeFile(self.share, fpath, writeobj)
        except smb_structs.OperationFailure as error:
            raise IOError(f"failed in write_text: {error}")

    def read_text(self, fpath: str) -> str:
        try:
            with io.BytesIO() as readobj:
                self.ctx.retrieveFile(self.share, fpath, readobj)
                ret = readobj.getvalue().decode("utf8")
        except smb_structs.OperationFailure as error:
            raise IOError(f"failed in read_text: {error}")
        return ret
