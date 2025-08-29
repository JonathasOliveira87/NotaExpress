from userProfile.models import UserProfile

def pic_global(request):
    profile = None
    if request.user.is_authenticated:
        if UserProfile.objects.filter(user=request.user).exists():
            profile = UserProfile.objects.get(user=request.user)
    return {'profile': profile}
