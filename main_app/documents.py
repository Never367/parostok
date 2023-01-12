from elasticsearch_dsl import Document, Text, Integer, analyzer, tokenizer

my_analyzer = analyzer('my_analyzer',
                       tokenizer=tokenizer('trigram', 'edge_ngram',
                                           min_gram=1, max_gram=100),
                       filter=['lowercase']
                       )


class ProductDoc(Document):
    name = Text(analyzer=my_analyzer, norms=False, fielddata=True)
    id = Integer()
    status_product = Text(fielddata=True)

    class Meta:
        index = 'product'
