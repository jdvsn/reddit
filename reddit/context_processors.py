from accounts.forms import LoginForm, UserForm

def add_my_login_form(request):
    return {
        'login_form': LoginForm(),
    }

def add_my_user_form(request):
    return {
        'user_form': UserForm(),
    }