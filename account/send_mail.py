from django.core.mail import send_mail


def send_confirmation_email(user, code):
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}'
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Что активировать ваш акккаунт нужно пройти код: '
        f'\n{full_link}'
        f'\nНе передовайте этот код никому!',
        'bekktur.35@gmail.com',
        [user],
        fail_silently=False,

    )

