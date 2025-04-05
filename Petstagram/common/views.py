from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

from Petstagram.common.forms import CommentForm, SearchForm
from Petstagram.common.models import Like, Comment
from Petstagram.photos.models import Photo


# Create your views here.
def index(request):
    all_photos = Photo.objects.all()
    comment_form = CommentForm()
    search_form = SearchForm(request.POST or None)
    user = request.user

    if user.is_authenticated:
        all_liked_photos_by_request_user = [like.to_photo_id for like in user.like_set.all()]
    else:
        all_liked_photos_by_request_user = []
    if search_form.is_valid():
        all_photos = all_photos.filter(tagged_pets__name__icontains=search_form.cleaned_data['pet_name'])
    context = {
        'all_photos': all_photos,
        'comment_form': comment_form,
        'search_form': search_form,
        'all_liked_photos_by_request_user': all_liked_photos_by_request_user,
    }
    return render(request, template_name='../templates/common/home-page.html', context=context)


@login_required
def like_functionality(request, photo_id):
    photo = Photo.objects.get(id=photo_id)

    liked_object = Like.objects.filter(to_photo_id=photo_id, user=request.user).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo=photo, user=request.user)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')


@login_required
def copy_link_clipboard(request, photo_id):
    copy(request.META['HTTP_HOST'] + resolve_url('photo-details', photo_id))

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')


@login_required
def add_comment(request, photo_id):
    if request.method == 'POST':
        photo = Photo.objects.get(id=photo_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_photo = photo
            comment.user = request.user
            comment.save()

        return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')