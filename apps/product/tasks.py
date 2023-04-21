from django.core.mail import send_mail
from django.db.models import Count
from apps.product.models import Product
from apps.rating.models import User
from cinema import settings

from celery import shared_task


@shared_task
def send_top_films_email():
    # Get the top 5 rated films
    top_films = Product.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5]
    users = User.objects.all()
    # Create the email message
    message = "Here are the top rated films of the week:\n\n"

    mail_subject = "Top week films"

    for i, film in enumerate(top_films, start=1):
        message += f"{i}. {film.title}\n"
    for user in users:
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
