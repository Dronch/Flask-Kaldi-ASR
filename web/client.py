from urllib.request import Request, urlopen
from multiprocessing.dummy import Pool as ThreadPool
import json
import time
import os


class TestClient(object):

    def __init__(self, host):
        self.host = host
        self.guid = None

    def post_wav(self, filepath):
        url = 'http://{}/asr'.format(self.host)
        data = open(filepath, 'rb').read()
        try:
            response = urlopen(Request(url, data=data))
            self.guid = json.loads(response.read().decode('utf-8'))['guid']
        except:
            self.guid = None
        return self.guid

    def status(self):
        if not self.guid:
            return None
        url = 'http://{}/asr/{}'.format(self.host, self.guid)
        try:
            response = urlopen(Request(url))
            return json.loads(response.read().decode('utf-8'))
        except:
            return None

    def test(self, filepath):
        if not self.post_wav(filepath):
            print('{} - FAILED POST'.format(filepath))
            return
        else:
            print('{} - CREATED {}'.format(filepath, self.guid))
        ready = False
        while not ready:
            result = self.status()
            if result is None:
                return

            if 'error' in result:
                print('{} - FAILED with {}'.format(filepath, result['error']))

            ready = result['ready']
            if ready:
                print('{} - OK with {}'.format(filepath, result))
            else:
                time.sleep(1)


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Server host', default='localhost')
    parser.add_argument('--dir', help='Folder path to test wav files.', default='wav')
    args = parser.parse_args()

    host = args.host

    def test_wav(filepath):
        client = TestClient(host)
        client.test(filepath)

    files = [os.path.join(args.dir, f) for f in os.listdir(args.dir)
             if os.path.isfile(os.path.join(args.dir, f)) and os.path.splitext(f)[1] == '.wav']

    n = len(files)
    print('Total wav files to test: {}'.format(n))
    pool = ThreadPool(n)
    pool.map(test_wav, files)
    pool.close()
    pool.join()


