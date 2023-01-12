from django.contrib import messages
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import urlsafe_base64_decode

from main_app.models import Product, BannerPromotion
from .models import Profile, WishList
from .tasks import user_register
from .forms import LoginForm, PasswordChangeFormBase, PasswordResetFormBase,\
    SetPasswordFormBase, UserRegistrationForm, UserEditForm, ProfileEditForm


UserModel = get_user_model()
user_account = {'Особисті дані': '/account/edit/',
                'Замовлення': '/account/orders/',
                'Список бажань': '/account/wish_list/'}


class LoginViewBase(auth_views.LoginView):

    form_class = LoginForm
    template_name = 'main.html'
    extra_context = {'banners': BannerPromotion.objects.all(),
                     'products': Product.objects.exclude(status_product='not_actual')}


class LogoutViewBase(auth_views.LogoutView):

    template_name = 'main.html'


class PasswordChangeViewBase(auth_views.PasswordChangeView):

    form_class = PasswordChangeFormBase


class PasswordResetViewBase(auth_views.PasswordResetView):

    form_class = PasswordResetFormBase
    html_email_template_name = 'registration/password_reset_email.html'


class PasswordResetConfirmViewBase(auth_views.PasswordResetConfirmView):

    form_class = SetPasswordFormBase


def register(request):

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Creating a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.email = new_user.username
            new_user.is_active = False
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            # start an asynchronous task
            current_site = get_current_site(request)
            use_https = request.is_secure()
            user_register.delay(new_user.email, current_site.domain, use_https)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


class RegisterConfirmView(auth_views.PasswordResetConfirmView):

    form_class = SetPasswordFormBase
    template_name = 'account/register_confirm.html'
    reset_url_token = 'register-success'

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
            user.is_active = True
            user.save()
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
            context['user_register'] = self.user
        else:
            context.update({
                'form': None,
                'title': 'Підтвердження ел. пошти',
                'validlink': False,
            })
        return context


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            request.user.email = request.POST['username']
            user_form.save()
            profile_form.save()
            messages.success(request, 'Особисті дані успішно збережено',
                             extra_tags='alert alert-success text-center')
        else:
            user_email = request.POST['username']
            if get_object_or_404(UserModel, username=user_email):
                messages.error(request, 'Ел. пошта вже використовується',
                               extra_tags='alert alert-danger text-center')
            else:
                messages.error(request, 'Помилка оновлення профілю',
                               extra_tags='alert alert-danger text-center')
    else:
        user_form = UserEditForm(instance=request.user,
                                 initial={
                                     'first_name': request.user.first_name,
                                     'last_name': request.user.last_name,
                                     'username': request.user.username
                                 })
        profile_form = ProfileEditForm(instance=request.user,
                                       initial={
                                           'phone_number': request.user.profile.phone_number,
                                           'city': request.user.profile.city,
                                           'address': request.user.profile.address,
                                           'postal_code': request.user.profile.postal_code
                                       })
    return render(request, 'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'user_account': user_account})


@login_required
def orders(request):
    user_orders = request.user.orders.all()
    paginator = Paginator(user_orders, 10)
    page_number = request.GET.get('page', 1)
    try:
        paginate_orders = paginator.page(page_number)
    except PageNotAnInteger:
        paginate_orders = paginator.page(1)
    except EmptyPage:
        paginate_orders = paginator.page(paginator.num_pages)
    return render(request, 'account/orders.html', {'orders': paginate_orders,
                                                   'user_account': user_account,
                                                   'paginator': paginator})


@login_required
def wish_list(request):
    user_wish_list = WishList.objects.get_or_create(user=request.user)[0]
    paginator = Paginator(user_wish_list.product.all(), 12)
    page_number = request.GET.get('page', 1)
    try:
        paginate_wish_list = paginator.page(page_number)
    except PageNotAnInteger:
        paginate_wish_list = paginator.page(1)
    except EmptyPage:
        paginate_wish_list = paginator.page(paginator.num_pages)
    return render(request, 'account/wish_list.html',
                  {'user_wish_list': paginate_wish_list,
                   'user_account': user_account,
                   'paginator': paginator})


@login_required()
def wish_list_add(request, product_id):
    user_wish_list = WishList.objects.get_or_create(user=request.user)[0]
    product = get_object_or_404(Product, id=product_id)
    user_wish_list.product.add(product)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def wish_list_remove(request, product_id):
    user_wish_list = WishList.objects.get_or_create(user=request.user)[0]
    product = get_object_or_404(Product, id=product_id)
    user_wish_list.product.remove(product)
    return redirect(request.META.get('HTTP_REFERER'))
