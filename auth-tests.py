import unittest, sys, requests, json,io

USER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwczovL2ZhaXJzY2FwZS5vcmciLCJleHAiOjE2MDMzODY2NTQsImdyb3VwcyI6bnVsbCwiaWF0IjoxNjAzMjEzODU0LCJuYW1lIjoiSnVzdGluIE5pZXN0cm95Iiwicm9sZSI6InVzZXIiLCJzdWIiOiJmN2E1Yjk1Ny1kOWVjLTQzNDktOWRlOS1hMGRmOWU5ZmVlYzUifQ.BCLgZu_rcyghA2O2Rh1yVbcouHGkIpnkhQH70Ku4DtE"
ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwczovL2ZhaXJzY2FwZS5vcmciLCJleHAiOjE2MDMzOTQ0NTgsImdyb3VwcyI6bnVsbCwiaWF0IjoxNjAzMjIxNjU4LCJuYW1lIjoiSnVzdGluIE5pZXN0cm95Iiwicm9sZSI6ImFkbWluIiwic3ViIjoiNTViYjYwZmMtYjczZi00M2MwLWIxMDUtNzU1MTIyMmNiNDU4In0.glv1vNbHjmVfy9FJ8HpNGIwCyH9opspIXVex7ZNlmLo"
BASE_URL = 'https://clarklab.uvarc.io/'
ARK = 'ark:99999/68c18c54-0ded-43c2-8bf5-9ad843ff1c18'
GROUP = 'test-group'
class test_user(unittest.TestCase):

    def test_mds_get(self):
        r = requests.get(BASE_URL + 'mds/' + ARK,
                            headers = {"Authorization": USER_TOKEN})

        status_code = r.status_code
        self.assertEqual(status_code,200)

    def test_mds_post(self):

        sample_meta = {'@type':'Dataset','name':'Test'}
        r = requests.post(BASE_URL + 'mds/shoulder/ark:99999',
                                        data = json.dumps(sample_meta),
                                        headers = {"Authorization": USER_TOKEN})

        status_code = r.status_code
        self.assertEqual(status_code,201)
        minted_id = r.json()['created']
        r3 = requests.delete(BASE_URL + 'mds/' + minted_id,
                                        headers = {"Authorization": ADMIN_TOKEN})
    def test_mds_put(self):
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

    def test_mds_delete(self):
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

    def test_transfer_get(self):
        r = requests.get(BASE_URL + 'transfer/data/' + ARK,
                                        headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,401)

    def test_transfer_post(self):
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

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": USER_TOKEN})
        self.assertTrue(r.status_code not in [400,401,403])

    def test_transfer_delete(self):

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

class test_admin(unittest.TestCase):

    def test_admin_mds_get(self):

        ark = 'ark:99999/02296050-26f8-441b-a765-b708224ca40a'
        r = requests.get(BASE_URL + 'mds/' + ark,
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
            'files':open('auth-tests.py','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": ADMIN_TOKEN})
        self.assertTrue(r.status_code not in [400,401,403])


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

    def test_owner_transfer_post_get_delete(self):
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

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": USER_TOKEN})
        self.assertTrue(r.status_code not in [400,401,403])
        ark = r.json()['Minted Identifiers'][0]
        r = requests.get(BASE_URL + 'transfer/data/' + ark,
                                        headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

        r = requests.delete(BASE_URL + 'transfer/data/' + ark,
                                        headers = {"Authorization": USER_TOKEN})
        self.assertTrue(r.status_code not in [400,401,403])


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
            'files':open('auth-tests.py','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": USER_TOKEN})
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

    def test_group_transfer_post_get_delete(self):
        dataset_meta = {
                        "@context":{
                            "@vocab":"http://schema.org/"
                        },
                        "@type":"SoftwareSourceCode",
                        "name":"Sample Software",
                        "description":"TEst",
                        "author":'Michael Notter',
                        'group':GROUP
                        }
        files = {
            'files':open('auth-tests.py','rb'),
            'metadata':json.dumps(dataset_meta)
        }

        url = BASE_URL + '/transfer/data'
        r = requests.post(url,files=files,headers = {"Authorization": ADMIN_TOKEN})
        ark = r.json()['Minted Identifiers'][0]
        r = requests.get(BASE_URL + 'transfer/data/' + ark,
                                        headers = {"Authorization": USER_TOKEN})
        self.assertEqual(r.status_code,200)

        r = requests.delete(BASE_URL + 'transfer/data/' + ark,
                                        headers = {"Authorization": USER_TOKEN})
        self.assertTrue(r.status_code in [400,401,403])

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
            'files':open('auth-tests.py','rb'),
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
    unittest.main()
