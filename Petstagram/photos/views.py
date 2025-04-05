from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.defaulttags import comment

from Petstagram.common.forms import CommentForm
from Petstagram.photos.forms import PhotoCreateForm, PhotoEditForm
from Petstagram.photos.models import Photo


# Create your views here.
def photo_add(request):
    form = PhotoCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        photo = form.save(commit=False)
        photo.user = request.user
        photo.save()
        form.save_m2m()
        return redirect('index')
    context = {
        "form": form,
    }
    return render(request, template_name='../templates/photo/photo-add-page.html', context=context)


@login_required
def photo_details(request, pk):
    photo = Photo.objects.get(pk=pk)
    likes = photo.like_set.all()
    comments = photo.comment_set.all()
    comment_form = CommentForm()
    photos_liked_by_user = likes.filter(user=request.user)
    all_liked_photos_by_request_user = [like.to_photo_id for like in request.user.like_set.all()]
    owner = photo.user
    context = {
        "photo": photo,
        "likes": likes,
        "comments": comments,
        "comment_form": comment_form,
        "photos_liked_by_user": photos_liked_by_user,
        'all_liked_photos_by_request_user': all_liked_photos_by_request_user,
        "owner": owner,
    }
    return render(request, template_name='../templates/photo/photo-details-page.html', context=context)


def photo_edit(request, pk):
    photo = Photo.objects.get(pk=pk)
    if request.method == "GET":
        form = PhotoEditForm(instance=photo, initial=photo.__dict__)
    else:
        form = PhotoEditForm(request.POST or None, request.FILES or None, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('photo-details', pk=pk)

    context = {
        "form": form,
    }
    return render(request, template_name='../templates/photo/photo-edit-page.html', context=context)


def photo_delete(request, pk):
    photo = Photo.objects.get(pk=pk)
    photo.delete()
    return redirect('index')