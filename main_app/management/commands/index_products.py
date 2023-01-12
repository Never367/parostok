from django.conf import settings
from django.core.management.base import BaseCommand
from elasticsearch_dsl import Index
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from main_app.models import Product
from main_app.documents import ProductDoc


class Command(BaseCommand):
    help = 'Indexes Products in Elastic Search'

    def handle(self, *args, **options):
        es = Elasticsearch(
            [{'host': settings.ES_HOST, 'port': settings.ES_PORT}],
            index="product"
        )
        product_index = Index('product')
        product_index.document(ProductDoc)
        if product_index.exists():
            product_index.delete()
            print('Deleted product index.')
        ProductDoc.init()
        result = bulk(
            client=es,
            actions=(product.indexing() for product in Product.objects.all().iterator())
        )
        print('Indexed products.')
        print(result)
