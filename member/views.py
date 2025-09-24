from django.contrib.auth import get_user_model, login
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
from member.forms import SignupForm, LoginForm
from utils.email import send_email
from django.conf import settings


User = get_user_model()
class SignupView(FormView):
    template_name = 'auth/signup.html'
    form_class = SignupForm
    # success_url = reverse_lazy('signup_done')

    def form_valid(self, form):
        user = form.save()
        # 이메일 발송
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)
        # print(signer_dump)
        #
        # decoded_user_email = signing.loads(signer_dump)
        # print(decoded_user_email)
        #
        # email = signer.unsign(decoded_user_email, max_age=60*30)
        # print(email)
        # http://localhost:8000/verify/?code=sjfhksjfhks

        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/verify/?code={signer_dump}'
        if settings.DEBUG:
            print(url)
        else:
            subject = '[Pystagram] 이메일 인증을 완료해주세요'
            message = f'다음 링크를 클릭해주세요. <a href="{url}">{url}</a>'
            send_email(subject, message, user.email )

        return render(
            self.request,
            'auth/signup_done.html',
            {'user': user}
        )

def verify_email(request):
    code = request.GET.get('code', '')
    # ''(공백을 넣는이유)'get'을 했을때, 'code'가 없으면 "None"값이 들어온다.
    # ''(공백)이 들어 오면 None==> ''(공백 string으로 들어온다.)

    signer = TimestampSigner()
    try:
        decoded_user_email = signing.loads(code)
        email = signer.unsign(decoded_user_email, max_age=60*30)
    except (TypeError, SignatureExpired):
        return render(request, 'auth/not_verified.html')

    user = get_object_or_404(User, email=email, is_active=False)
    user.is_active = True
    user.save()
    # TODO: 나중에 Redirect 시키기
    # return redirect(reverse('login'))
    return render(request, 'auth/email_verified_done.html', {'user': user})

class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    # TODO: 나중에 메인페이지로 Redirect 시키기
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.user
        # email = form.cleaned_data['email']
        # user = User.objects.get(email=email)
        login(self.request, user)

        next_page = self.request.GET.get('next')
        if next_page:
            return HttpResponseRedirect(next_page)

        return HttpResponseRedirect(self.get_success_url())
