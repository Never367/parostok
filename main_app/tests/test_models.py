from django.test import TestCase

from main_app.models import Category, SubCategory, Product, ProductPrice, ProductImage, BannerPromotion


class AbstractProductsTest:

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='category_name',
                                               slug='category_slug',
                                               image='category_picture.jpg')
        cls.subcategory = SubCategory.objects.create(category=cls.category,
                                                     name='subcategory_name',
                                                     slug='subcategory_slug')
        cls.product = Product.objects.create(category=cls.category,
                                             subcategory=cls.subcategory,
                                             name='product_name',
                                             slug='product_slug',
                                             status_product='actual')
        cls.product_price = ProductPrice.objects.create(product=cls.product,
                                                        product_age='1_year',
                                                        product_container='1_l',
                                                        price='250')
        cls.product_image = ProductImage.objects.create(product=cls.product,
                                                        image='product_picture.jpg')


class CategoryModelTest(AbstractProductsTest, TestCase):

    def test_str(self):
        self.assertEquals(str(self.category), 'category_name')

    def test_get_absolute_url(self):
        self.assertEquals(self.category.get_absolute_url(), '/category_slug/')

    def test_image_folder(self):
        self.assertEquals(self.category.image_folder('image.jpg'),
                          'category_slug/category_slug.jpg')


class SubCategoryModelTest(AbstractProductsTest, TestCase):

    def test_str(self):
        self.assertEquals(str(self.subcategory), 'subcategory_name')

    def test_get_absolute_url(self):
        self.assertEquals(self.subcategory.get_absolute_url(),
                          '/category_slug/subcategory_slug/')


class ProductModelTest(AbstractProductsTest, TestCase):

    def test_str(self):
        self.assertEquals(str(self.product), 'product_name')

    def test_get_absolute_url(self):
        self.assertEquals(self.product.get_absolute_url(),
                          '/category_slug/subcategory_slug/product_slug/')

    def test_indexing(self):
        self.assertEquals(self.product.indexing(), {'_id': 33, '_source':
            {'name': 'product_name', 'id': 33, 'status_product': 'actual'}})


class ProductPriceModelTest(AbstractProductsTest, TestCase):

    def test_str(self):
        self.assertEquals(str(self.product_price), '250')


class ProductImageModelTest(AbstractProductsTest, TestCase):

    def test_image_folder(self):
        self.assertEquals(self.product_image.image_folder('image.jpg'),
                          'product_slug/product_slug.jpg')

    def test_image_tag(self):
        self.assertEquals(self.product_image.image_tag(),
                          '<img src="/media/product_picture.jpg" width="150" height="150" />')

    def test_str(self):
        self.assertEquals(str(self.product_image), 'product_picture.jpg')


class BannerPromotionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.banner = BannerPromotion.objects.create(name='banner_name',
                                                    link='banner_link',
                                                    image='banner_picture.jpg',
                                                    image_mobile='banner_picture_mobile.jpg')

    def test_image_folder(self):
        self.assertEquals(self.banner.image_folder('image.jpg'),
                          'Банери/banner_name/banner_name.jpg')

    def test_str(self):
        self.assertEquals(str(self.banner), 'banner_name')
