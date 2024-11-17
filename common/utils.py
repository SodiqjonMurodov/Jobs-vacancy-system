from django.core.mail import send_mail

def send_confirmation_email(email, code):
    send_mail(
        subject = 'Код подтверждение',
        message=f'Ваш код подтверждения в системе поиска вакансий: {code}',
        html_message=f"""
            <p>Ваш код подтверждения в системе поиска вакансий:</p>
            <p><b>{code}</b></p>
            <p>Проверить приведенный выше код можно, перейдя по <a href="http://example.com/confirmation/12346">ссылке</a>.</p>
            """,
        from_email='murodovsodiq1800@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )
