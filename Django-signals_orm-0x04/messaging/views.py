from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log user out before deleting
    user.delete()    # Triggers post_delete signal
    return redirect('/')  # Redirect to home page after deletion
