from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from elasticsearch import Elasticsearch
from rest_framework.views import APIView
from elasticsearch.exceptions import ConnectionError

from .models import Category, SubCategory, Product, BannerPromotion


class MainView(TemplateView):

    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = BannerPromotion.objects.all()
        context['products'] = Product.objects.exclude(status_product='not_actual')[:6]
        return context


class CategoryListView(ListView):
    paginate_by = 12
    model = Product
    queryset = Product.objects.all()
    template_name = 'category_detail.html'

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return redirect('main')
        else:
            self.category = category

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category=self.category,)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class SubCategoryListView(ListView):
    paginate_by = 12
    model = SubCategory
    queryset = Product.objects.all()
    template_name = 'subcategory_detail.html'

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            subcategory = SubCategory.objects.get(slug=slug)
        except SubCategory.DoesNotExist:
            return redirect('main')
        else:
            self.subcategory = subcategory

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(subcategory=self.subcategory)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategory'] = self.subcategory
        return context


class ProductDetailView(DetailView):
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


class SearchListView(ListView):
    paginate_by = 12
    model = Product
    queryset = Product.objects.all()
    template_name = 'search_results.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        object_list = ''
        if q:
            object_list = ProductSearchView.get(request=self.request)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class ProductSearchView(APIView):

    @staticmethod
    def get(request):
        query = request.GET.get('q').lower()
        client = Elasticsearch()
        try:
            response_dict = client.search(
                index='product',
                body={
                    'query': {
                        'bool': {
                            'should': [
                                {
                                    'match': {
                                        'name': {
                                            'query': query,
                                            'operator': 'or',
                                            'fuzziness': 'auto'
                                        }
                                    }
                                },
                                {
                                    'wildcard': {
                                        'name': {
                                            'value': f'*{query}*',
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    'sort': [
                        '_score',
                        {'status_product': 'asc'},
                        {'name': 'asc'}
                    ]
                }
            )
            hits = response_dict['hits']['hits']
            ids = [hit['_source']['id'] for hit in hits]
            queryset = Product.objects.filter(id__in=ids)
            product_list = list(queryset)
            product_list.sort(key=lambda product: ids.index(product.id))
            # serializer = ProductSerializer(product_list, many=True)
        except ConnectionError:
            product_list = Product.objects.filter(name__icontains=query)
            # serializer = ProductSerializer(product_list, many=True)
        # return Response(serializer.data)
        return product_list
