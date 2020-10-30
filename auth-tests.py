import unittest, sys, requests, json,io
import warnings

warnings.simplefilter("ignore", ResourceWarning)
USER_TOKEN =
ADMIN_TOKEN = 
BASE_URL = 'https://clarklab.uvarc.io/'
ARK = 'ark:99999/23ca2cf4-8521-424d-99be-9072ea29aaa6'
GROUP = 'test-group'

class test_user(unittest.TestCase):

    def test_user_mds_get(self):
        r = requests.get(BASE_URL + 'mds/' + ARK,
                            headers = {"Authorization": USER_TOKEN})

        status_code = r.status_code
        self.assertEqual(status_code,200)

    def test_user_mds_post(self):

        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})

        status_code = r.status_code
        self.assertEqual(status_code,201)
        minted_id = r.json()['created']
        r3 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": ADMIN_TOKEN})
    def test_user_mds_put(self):
        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": ADMIN_TOKEN})
        minted_id = r.json()['created']
        new_meta = {'name':'New Test'}
        r2 = requests.put(BASE_URL + 'mds/' + minted_id,
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})

        self.assertEqual(r2.status_code,401)
        r3 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": ADMIN_TOKEN})

    def test_user_mds_delete(self):
        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": ADMIN_TOKEN})
        minted_id = r.json()['created']
        r2 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": USER_TOKEN})

        self.assertEqual(r2.status_code,401)
        r3 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": ADMIN_TOKEN})

    def test_user_transfer_get(self):
        r = requests.get(BASE_URL + 'transfer/data/' + ARK,
                                        headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,401)

    def test_user_transfer_post(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        "author":'Michael Notter'
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": USER_TOKEN})
        files['files'].close()
        self.assertTrue(r.status_code not in [401,403])


    def test_user_transfer_put(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        "author":'Michael Notter'
                        }
        files = {
            'files':open('auth-tests.py','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data/' + ARK
        r = requests.put(url,files=files,headers = {"Authorization": USER_TOKEN})
        files['files'].close()
        self.assertTrue(r.status_code in [401,403])

    def test_user_transfer_delete(self):

        r = requests.delete(BASE_URL + 'transfer/data/' + ARK,
                                headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,401)

    def test_user_compute_get(self):

        r = requests.get(BASE_URL + 'compute/job',
                                headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

    def test_user_compute_post(self):
        job_data =  {
                    "datasetID":ARK,
                    "scriptID":ARK
                    }
        r = requests.post(BASE_URL + 'compute/nipype',data = json.dumps(job_data),
                                headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,401)

    def test_user_eg_get(self):
        r = requests.get(BASE_URL + 'evidencegraph/' + ARK, headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

    def test_user_viz_get(self):
        r = requests.get(BASE_URL + 'viz/' + ARK, headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

    def test_user_search_get(self):
        r = requests.get(BASE_URL + 'search/test', headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

class test_admin(unittest.TestCase):

    def test_admin_mds_get(self):


        r = requests.get(BASE_URL + 'mds/' + ARK,
                            headers = {"Authorization": ADMIN_TOKEN})

        status_code = r.status_code
        self.assertEqual(status_code,200)

    def test_admin_mds_post(self):

        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": ADMIN_TOKEN})

        status_code = r.status_code
        self.assertEqual(status_code,201)
        minted_id = r.json()['created']
        r3 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": ADMIN_TOKEN})
    def test_admin_mds_put(self):
        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})
        minted_id = r.json()['created']
        new_meta = {'name':'New Test'}
        r2 = requests.put(BASE_URL + 'mds/' + minted_id,
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": ADMIN_TOKEN})

        self.assertEqual(r2.status_code,200)
        r3 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": ADMIN_TOKEN})

    def test_admin_mds_delete(self):
        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})
        minted_id = r.json()['created']
        r2 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": ADMIN_TOKEN})

        self.assertEqual(r2.status_code,200)

    def test_admin_transfer_get(self):
        r = requests.get(BASE_URL + 'transfer/data/' + ARK,
                                        headers = {"Authorization": ADMIN_TOKEN})
        self.assertEqual(r.status_code,200)

    def test_admin_transfer_post(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        "author":'Michael Notter'
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": ADMIN_TOKEN})
        files['files'].close()
        self.assertTrue(r.status_code not in [401,403])

    def test_admin_transfer_put(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        "author":'Michael Notter'
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data/' + ARK
        r = requests.put(url,files=files,headers = {"Authorization": ADMIN_TOKEN})
        files['files'].close()
        self.assertTrue(r.status_code not in [401,403])

    def test_admin_transfer_delete(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        "author":'Michael Notter'
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": USER_TOKEN})
        ark = r.json()['Minted Identifiers'][0]
        r = requests.delete(BASE_URL + 'transfer/data/' + ark,
                                headers = {"Authorization": ADMIN_TOKEN})
        self.assertEqual(r.status_code,200)

    def test_admin_compute_get(self):

        r = requests.get(BASE_URL + 'compute/job',
                                headers = {"Authorization": ADMIN_TOKEN})
        self.assertEqual(r.status_code,200)

    def test_admin_compute_post(self):
        job_data =  {
                    "datasetID":ARK,
                    "scriptID":ARK
                    }
        r = requests.post(BASE_URL + 'compute/nipype',data = json.dumps(job_data),
                                headers = {"Authorization": ADMIN_TOKEN})

        self.assertEqual(r.status_code,200)

class test_owner(unittest.TestCase):
    def test_user_mds_post(self):

        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})

        status_code = r.status_code
        self.assertEqual(status_code,201)
        minted_id = r.json()['created']
        r3 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": ADMIN_TOKEN})
    def test_owner_mds_get(self):
        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})
        ark = r.json()['created']
        r = requests.get(BASE_URL + 'mds/' + ark,
                            headers = {"Authorization": USER_TOKEN})

        status_code = r.status_code
        self.assertEqual(status_code,200)

    def test_owner_mds_put(self):
        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})
        minted_id = r.json()['created']
        new_meta = {'name':'New Test'}
        r2 = requests.put(BASE_URL + 'mds/' + minted_id,
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})

        self.assertEqual(r2.status_code,200)
        r3 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": ADMIN_TOKEN})

    def test_owner_mds_delete(self):
        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})
        minted_id = r.json()['created']
        r2 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": USER_TOKEN})

        self.assertEqual(r2.status_code,200)

    def test_owner_transfer_get(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst"
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": USER_TOKEN})
        files['files'].close()
        ark = r.json()['Minted Identifiers'][0]
        r = requests.get(BASE_URL + 'transfer/data/' + ark,
                                        headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

    def test_owner_transfer_post(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        "author":'Michael Notter'
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": USER_TOKEN})
        files['files'].close()
        self.assertTrue(r.status_code not in [401,403])

    def test_owner_transfer_put(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        "author":'Michael Notter'
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": USER_TOKEN})
        files['files'].close()
        ark = r.json()['Minted Identifiers'][0]
        files = {
            'files':open('auth-tests.py','rb'),
            'metadata':json.dumps(dataset_meta)
        }
        url = BASE_URL + '/transfer/data/' + ark
        r = requests.put(url,files=files,headers = {"Authorization": USER_TOKEN})
        files['files'].close()
        self.assertTrue(r.status_code not in [401,403])


    def test_owner_transfer_delete(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        "author":'Michael Notter'
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": USER_TOKEN})
        files['files'].close()
        ark = r.json()['Minted Identifiers'][0]
        r = requests.delete(BASE_URL + 'transfer/data/' + ark,
                                        headers = {"Authorization": USER_TOKEN})
        self.assertTrue(r.status_code not in [401,403])

    def test_owner_compute_get(self):

        r = requests.get(BASE_URL + 'compute/job',
                                headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

    def test_owner_compute_post(self):

        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        "author":'Michael Notter'
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": USER_TOKEN})
        files['files'].close()
        ark = r.json()['Minted Identifiers'][0]
        job_data =  {
                    "datasetID":ark,
                    "scriptID":ark
                    }
        r = requests.post(BASE_URL + 'compute/nipype',data = json.dumps(job_data),
                                headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

class test_group(unittest.TestCase):

    def test_group_mds_get(self):
        sample_meta = {'@type':'Dataset','name':'Test','group':GROUP}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": ADMIN_TOKEN})
        ark = r.json()['created']
        r = requests.get(BASE_URL + 'mds/' + ark,
                            headers = {"Authorization": USER_TOKEN})

        status_code = r.status_code
        self.assertEqual(status_code,200)

    def test_group_mds_post(self):

        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})

        status_code = r.status_code
        self.assertEqual(status_code,201)
        minted_id = r.json()['created']
        r3 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": ADMIN_TOKEN})
    def test_group_mds_put(self):
        sample_meta = {'@type':'Dataset','name':'Test','group':GROUP}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": ADMIN_TOKEN})
        minted_id = r.json()['created']
        new_meta = {'name':'New Test'}
        r2 = requests.put(BASE_URL + 'mds/' + minted_id,
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})

        self.assertEqual(r2.status_code,401)
        r3 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": ADMIN_TOKEN})

    def test_group_mds_delete(self):
                sample_meta = {'@type':'Dataset','name':'Test','group':GROUP}
                r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                                data = json.dumps(sample_meta),
                                                headers = {"Authorization": ADMIN_TOKEN})
                minted_id = r.json()['created']
                r2 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                                headers = {"Authorization": USER_TOKEN})

                self.assertEqual(r2.status_code,401)

    def test_group_transfer_get(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        'group':GROUP
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": ADMIN_TOKEN})
        files['files'].close()
        ark = r.json()['Minted Identifiers'][0]
        r = requests.get(BASE_URL + 'transfer/data/' + ark,
                                        headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

    def test_group_transfer_post(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst"
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": USER_TOKEN})
        files['files'].close()
        self.assertTrue(r.status_code not in [401,403])

    def test_group_transfer_put(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        'group':GROUP
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": ADMIN_TOKEN})
        files['files'].close()
        ark = r.json()['Minted Identifiers'][0]
        files = {
            'files':open('auth-tests.py','rb'),
            'metadata':json.dumps(dataset_meta)
        }
        url = BASE_URL + '/transfer/data/' + ark
        r = requests.put(url,files=files,headers = {"Authorization": USER_TOKEN})
        files['files'].close()
        self.assertTrue(r.status_code in [401,403])


    def test_group_transfer_delete(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        'group':GROUP
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": ADMIN_TOKEN})
        files['files'].close()
        ark = r.json()['Minted Identifiers'][0]
        r = requests.delete(BASE_URL + 'transfer/data/' + ark,
                                        headers = {"Authorization": USER_TOKEN})
        self.assertTrue(r.status_code in [401,403])

    def test_owner_compute_get(self):

        r = requests.get(BASE_URL + 'compute/job',
                                headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

    def test_group_compute_post(self):

        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        'group':GROUP
                        }
        files = {
            'files':open('README.md','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": ADMIN_TOKEN})
        ark = r.json()['Minted Identifiers'][0]
        job_data =  {
                    "datasetID":ark,
                    "scriptID":ark
                    }
        r = requests.post(BASE_URL + 'compute/nipype',data = json.dumps(job_data),
                                headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
