from google.cloud import bigquery

class Bigquery():

    def __init__(self):
        self.client = bigquery.Client()