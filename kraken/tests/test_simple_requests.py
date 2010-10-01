
import os
from unittest import TestCase

from . import KrakenSiteMixin

class TestSimpleRequests(KrakenSiteMixin, TestCase):
    def test_notfound(self):
        r = self.client.get('/nonexistent')
        self.assertEqual(r.status_code, 404)

    def test_hidden_notfound(self):
        r2 = self.client.get('/.hidden_but_nonexistent')
        self.assertEqual(r2.status_code, 404)

    def test_hidden_static(self):
        r = self.client.get('/__logo/.hidden_file')
        self.assertEqual(r.status_code, 403)

    # with the new import, . in the URL is replace by a _, so python files
    # with a . (other than .py) can never be accessed
#    def test_hidden_python(self):
#        r = self.client.get('/.hidden_python')
#        self.assertEqual(r.status_code, 403)

#    def test_hidden_dir_python(self):
#        r = self.client.get('/.hidden_dir/blah')
#        self.assertEqual(r.status_code, 403)

    def test_hidden_template(self):
        r = self.client.get('/.hidden_template')
        self.assertEqual(r.status_code, 403)

    def test_static_notfound(self):
        r = self.client.get('/__logo/inexistent.png')
        self.assertEqual(r.status_code, 404)

    def test_lipsum_notfound(self):
        r = self.client.get('/lorem/ipsum/dolor')
        self.assertEqual(r.status_code, 404)

    def test_index(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(r.data, '<html><body>Dyko root</body></html>\n')

    def test_hello(self):
        r = self.client.get('/hello/?name=World')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(r.data, '<html><body>Hello, World!</body></html>\n')

    def test_hello_redirect(self):
        r = self.client.get('/hello?world')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r.headers['Location'], 'http://localhost/hello/?world')
        self.assert_('redirect' in r.data.lower())
        self.assert_('hello/?world' in r.data)

    def test_lipsum(self):
        r = self.client.get('/lorem/ipsum/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Content-Type'], 'text/plain; charset=utf-8')
        self.assert_('Lorem ipsum dolor sit amet' in r.data)
    

    def test_logo(self):
        r = self.client.get('/__logo/dyko.png')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Content-Type'], 'image/png')
        # Maybe check the actual content here instead of just the length ?
        self.assertEqual(len(r.data), 12677)

    def test_logo_etag(self):
        # assume that self.test_logo() passed
        initial_response = self.client.get('/__logo/dyko.png')
        
        response = self.client.get('/__logo/dyko.png', headers=[
            ('If-None-Match', initial_response.headers['ETag']),
        ])
        self.assertEqual(response.status_code, 304)
        self.assertEqual(response.data, '')

    def test_logo_last_modified(self):
        # assume that self.test_logo() passed
        initial_response = self.client.get('/__logo/dyko.png')
        
        response = self.client.get('/__logo/dyko.png', headers=[
            ('If-Modified-Since', initial_response.headers['Last-Modified']),
        ])
        self.assertEqual(response.status_code, 304)
        self.assertEqual(response.data, '')

    def test_logo_etag_and_last_modified(self):
        # assume that self.test_logo() passed
        initial_response = self.client.get('/__logo/dyko.png')
        
        response = self.client.get('/__logo/dyko.png', headers=[
            ('If-None-Match', initial_response.headers['ETag']),
            ('If-Modified-Since', initial_response.headers['Last-Modified']),
        ])
        self.assertEqual(response.status_code, 304)
        self.assertEqual(response.data, '')

class TestSession(KrakenSiteMixin, TestCase):
    def setUp(self):
        self.site_secret_key = os.urandom(20)
        super(TestSession, self).setUp()

    def test_session(self):
        # get the default value
        r1 = self.client.get('/session/')
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r1.data, '(no value)')

        # set the value
        r2 = self.client.get('/session/?blah')
        self.assertEqual(r2.status_code, 200)

        # get again and check
        r3 = self.client.get('/session/')
        self.assertEqual(r3.status_code, 200)
        self.assertEqual(r3.data, 'blah')
        
