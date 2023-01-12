from django.test import TestCase
from django.urls import reverse

from main_app.models import Category, SubCategory, Product


class AbstractProductsViewTest:

    @classmethod
    def setUpTestData(cls):
        number_of_products = 15
        cls.category = Category.objects.create(name=f'category_name',
                                               slug=f'category_slug',
                                               image=f'category_picture.jpg')

        cls.subcategory = SubCategory.objects.create(category=cls.category,
                                                     name='subcategory_name',
                                                     slug='subcategory_slug')

        for product_number in range(number_of_products):
            Product.objects.create(category=cls.category,
                                   subcategory=cls.subcategory,
                                   name=f'product_name_{product_number}',
                                   slug=f'product_slug_{product_number}',
                                   status_product='actual')


class MainViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')


class CategoryListViewViewTest(AbstractProductsViewTest, TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/category_slug/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('category_detail', args=['category_slug']))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('category_detail', args=['category_slug']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_detail.html')

    def test_pagination_is_twelve(self):
        response = self.client.get(reverse('category_detail', args=['category_slug']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['product_list']) == 12)

    def test_lists_all_products(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('category_detail', args=['category_slug'])
                                   + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['product_list']) == 3)


class SubCategoryListViewViewTest(AbstractProductsViewTest, TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/category_slug/subcategory_slug/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('subcategory_detail',
                                           args=['category_slug', 'subcategory_slug']))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('subcategory_detail', args=['category_slug', 'subcategory_slug']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subcategory_detail.html')

    def test_pagination_is_twelve(self):
        response = self.client.get(reverse('subcategory_detail',
                                           args=['category_slug', 'subcategory_slug']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['product_list']) == 12)

    def test_lists_all_products(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('subcategory_detail',
                                           args=['category_slug',
                                                 'subcategory_slug'])
                                   + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['product_list']) == 3)


class ProductDetailViewViewTest(AbstractProductsViewTest, TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/category_slug/subcategory_slug/product_slug_1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('product_detail', args=['category_slug',
                                                                   'subcategory_slug',
                                                                   'product_slug_1']))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('product_detail', args=['category_slug',
                                                                   'subcategory_slug',
                                                                   'product_slug_1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')


class SearchListViewViewTest(AbstractProductsViewTest, TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/search/?q=product_name/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('search_results'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('search_results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')

    def test_pagination_is_twelve(self):
        response = self.client.get(reverse('search_results') + '?q=product_name')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['product_list']) == 12)

    def test_lists_all_products(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('search_results') +
                                   '?q=product_name&page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['product_list']) == 3)
