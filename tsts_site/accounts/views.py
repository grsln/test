from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.views.generic import FormView
from .forms import SignUpForm


class RegisterFormView(FormView):
    form_class = SignUpForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        user = form.save()
        # Созданного пользователя добавляем в группу TstUsers
        my_group = Group.objects.get(name='TstUsers')
        my_group.user_set.add(user)
        #  Аутентификация зарегистрировавшегося пользователя
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)
