from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post


# Главная страница
def index(request):
    joke = ['Почему томат красный? Потому что он увидел салат!']

    # Получаем все посты из базы
    posts = Post.objects.all().order_by('-created_at')

    # Рендерим страницу
    return render(request, 'index.html', {
        'posts': posts,
        'joke': joke
    })


# Вход
def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error = 'Неверный пароль'
        except User.DoesNotExist:
            error = 'Пользователь с таким email не найден'

    return render(request, 'login.html', {'error': error})


# Регистрация
def register_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            error = 'Пароли не совпадают'
        elif User.objects.filter(username=username).exists():
            error = 'Имя пользователя уже занято'
        elif User.objects.filter(email=email).exists():
            error = 'Email уже зарегистрирован'
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')

    return render(request, 'register.html', {'error': error})


# Выход
def logout_view(request):
    logout(request)
    return redirect('login')


# Добавление/удаление из избранного
@login_required
def toggle_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.favorited_by.all():
        post.favorited_by.remove(request.user)
    else:
        post.favorited_by.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


# Лайк / дизлайк
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


# Страница избранного
@login_required
def favorites_view(request):
    posts = request.user.favorite_posts.all().order_by('-created_at')
    return render(request, 'favorites.html', {'posts': posts})

from .forms import PostForm
from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

