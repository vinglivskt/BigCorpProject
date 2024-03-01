from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_email_verification import send_email

User = get_user_model()

from .forms import LoginForm, UserCreateForm, UserUpdateForm


# Register new user
def register_user(request):
    """
    Register a new user with the provided request object.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML page or a redirect to the email verification sent page.
    """
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')

            # Create new user
            user = User.objects.create_user(
                username=user_username, email=user_email, password=user_password
            )

            user.is_active = False

            send_email(user)

            return redirect('/account/email-verification-sent/')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form})


def login_user(request):
    """
    A function to handle user login. It takes a request object as a parameter and performs the login logic based on the request method and user authentication status.
    """
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect('shop:products')

    if request.method == 'POST':

        form = LoginForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account:dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect('account:login')
    context = {
        'form': form
    }
    return render(request, 'account/login/login.html', context)


def logout_user(request):
    """
    Logs out the user and redirects to the 'shop:products' page.

    Parameters:
    request : object
        The request object containing user information.

    Returns:
    object
        A redirect response to the 'shop:products' page.
    """
    logout(request)
    return redirect('shop:products')


@login_required(login_url='account:login')
def dashboard_user(request):
    """
    View for the dashboard user with login required.
    """
    return render(request, 'account/dashboard/dashboard.html')


@login_required(login_url='account:login')
def profile_user(request):
    """
    View for managing user profile. Requires user to be logged in. Uses UserUpdateForm to update user information.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('account:dashboard')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form
    }

    return render(request, 'account/dashboard/profile-management.html', context)


@login_required(login_url='account:login')
def delete_user(request):
    """
    This function deletes a user. It requires the request object as a parameter and does not return a value.
    """
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('shop:products')
    return render(request, 'account/dashboard/account-delete.html')