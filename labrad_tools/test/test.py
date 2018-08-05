from labrad.server import LabradServer
from labrad.server import Signal, setting

class TestServer(LabradServer):
    name = 'test'

if __name__ == "__main__":
    from labrad import util
    util.runServer(TestServer())
