"""Local checks only. No credentials or NASA network calls."""
import copy, importlib.util, json, pathlib, tempfile, unittest, zipfile
PATH=pathlib.Path(__file__).with_name('download.py')
spec=importlib.util.spec_from_file_location('downloader',PATH)
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)

class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.items=json.loads(PATH.with_name('download_manifest.json').read_text())
    def test_fixed_manifest(self):
        d.validate_manifest(self.items)
        self.assertEqual({x['event'] for x in self.items},d.EVENTS)
        self.assertTrue(all(sum(y['event']==x for y in self.items)==6 for x in d.EVENTS))
        bad=copy.deepcopy(self.items);bad[0]['download_url']='https://example.com/file'
        with self.assertRaises(ValueError):d.validate_manifest(bad)
        bad=copy.deepcopy(self.items);bad[0]['filename']='../file.h5'
        with self.assertRaises(ValueError):d.validate_manifest(bad)
    def test_signature_and_size(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'sample.h5';data=d.HDF5+b'x'*2048
            p.write_bytes(data);m={**self.items[0],'size_mib':len(data)/1024**2}
            self.assertEqual(d.inspect_file(p,m)['bytes'],len(data))
            p.write_bytes(b'<html>login</html>')
            with self.assertRaises(ValueError):d.inspect_file(p,m)
            p.write_bytes(d.HDF5+b'x'*4096)
            with self.assertRaises(ValueError):d.inspect_file(p,m)
    def test_secure_curl_arguments(self):
        args=d.curl_arguments('curl',self.items[0],pathlib.Path('out.h5.part'))
        self.assertEqual(args[args.index('--proto')+1],'=https')
        self.assertEqual(args[args.index('--proto-redir')+1],'=https')
        self.assertEqual(args[args.index('--config')+1],'-')
        self.assertEqual(args[args.index('--cookie')+1],'')
        self.assertNotIn('--location-trusted',args)
        self.assertNotIn('--insecure',args)
        self.assertFalse(any('Bearer' in x for x in args))
    def test_three_complete_archives(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td);raw=root/'raw';raw.mkdir()
            for m in self.items:(raw/m['filename']).write_bytes(d.HDF5)
            receipts=[{'filename':m['filename'],'event':m['event'],'sha256':'fixture'} for m in self.items]
            paths=d.make_archives(self.items,receipts,raw,root/'out')
            self.assertEqual(len(paths),3)
            for p in paths:
                with zipfile.ZipFile(p) as z:
                    self.assertIsNone(z.testzip())
                    manifest=json.loads(z.read('manifest.json'))
                    self.assertEqual(len(manifest),6)
                    self.assertEqual({m['filename'] for m in manifest},{n for n in z.namelist() if n.endswith('.h5')})
                    self.assertFalse(any('token' in n.lower() for n in z.namelist()))
if __name__=='__main__':unittest.main()
