import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from .models import UserActivateTokens

from django.contrib.sites.shortcuts import get_current_site
# from django.core.signing import dumps
from uuid import uuid4
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages




class RegistUserView(CreateView):
    template_name = os.path.join('accounts', 'regist.html')
    form_class = RegistForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        token = str(uuid4())
        user_activate_token = UserActivateTokens.objects.create(
            user=user, token=token, expired_at=datetime.now() + timedelta(days=1)
        )
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': token,
            'user': user,
        }

        subject = render_to_string('accounts/mail_template/create/subject.txt', context)
        message = render_to_string('accounts/mail_template/create/message.txt', context)
        from_email = "test8mizuki@gmail.com"
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)
        messages.info(self.request, "確認メールを送信しました。")
        return redirect('accounts:user_login')


class UserLoginView(FormView):
    template_name = os.path.join('accounts', 'user_login.html')
    form_class = UserLoginForm
    
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('task:task_home')
        else:
            messages.error(self.request, "アカウント認証に失敗しました。")
            return redirect('accounts:user_login')
        

class UserLogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:user_login')


def activate_user(request, token):
    user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)
    messages.info(request, "ユーザを有効化しました")
    return redirect('accounts:user_login')