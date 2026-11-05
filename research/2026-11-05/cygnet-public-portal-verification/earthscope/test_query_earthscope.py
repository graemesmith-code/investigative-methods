import hashlib,json,pathlib,tempfile,unittest
from unittest.mock import patch
import query_earthscope as q
class FakeResponse:
    status=200
    headers={'Content-Type':'text/plain'}
    url='https://example.invalid/response'
    def __enter__(self):return self
    def __exit__(self,*a):return False
    def read(self):return b'synthetic public response'
class QueryTests(unittest.TestCase):
    def test_names_with_dots_do_not_collide(self):
        with tempfile.TemporaryDirectory() as d:
            q.ROOT=pathlib.Path(d); records=[]
            with patch('urllib.request.urlopen',return_value=FakeResponse()):
                for host in ('service.iris.edu','service.earthscope.org'):
                    for flag in ('true','false'):
                        r,b=q.fetch((f'station_{host}_{flag}','https://example.invalid',{'includerestricted':flag}));records.append(r)
            self.assertEqual(len({r['body_file'] for r in records}),4)
            for r in records:
                body=(q.ROOT/r['body_file']).read_bytes()
                self.assertEqual(r['sha256'],hashlib.sha256(body).hexdigest())
    def test_zero_distance(self):self.assertAlmostEqual(q.dist(q.LAT,q.LON),0)
if __name__=='__main__':unittest.main()
