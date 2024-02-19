# myproject/context_processors.py

from user.models import *  # Adjust this import based on your app's structure
 
def random_user_ids(request):
    if request.user.is_authenticated:
        current_user = request.user
        following_ids = Following.objects.filter(main_user=current_user).values_list('following_to', flat=True)
        random_user_ids = User.objects.exclude(pk=current_user.pk).exclude(is_superuser=True).exclude(pk__in=following_ids).order_by('?')[:3]
    else:
        random_user_ids = []  # Or any default value you prefer
    return {'random_user_ids': random_user_ids}