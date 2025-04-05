from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Petstagram.accounts.models import PetstagramUser
from Petstagram.common.forms import CommentForm
from Petstagram.common.models import Comment
from Petstagram.pets.models import Pet
from Petstagram.pets.forms import PetForm, PetDeleteForm


# Create your views here.
def add_pet(request):
    form = PetForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        pet = form.save(commit=False)
        pet.user = request.user
        pet.save()
        return redirect('profile-details', pk=request.user.pk)

    context = {
        "form": form,
    }
    return render(request, template_name='../templates/pet/pet-add-page.html', context=context)


@login_required
def pet_details(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    all_photos = pet.photo_set.all()
    comment_form = CommentForm()
    comments = Comment.objects.all()
    all_liked_photos_by_request_user = [like.to_photo_id for like in request.user.like_set.all()]
    owner = PetstagramUser.objects.get(username=username)
    context = {
        "pet": pet,
        "all_photos": all_photos,
        "comment_form": comment_form,
        "comments": comments,
        "all_liked_photos_by_request_user": all_liked_photos_by_request_user,
        "owner": owner,
    }
    return render(request, template_name='../templates/pet/pet-details-page.html', context=context)


def edit_pet(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    if request.method == "GET":
        form = PetForm(instance=pet, initial=pet.__dict__)
    else:
        form = PetForm(request.POST, request.FILES , instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet-details', username, pet_slug)

    context = {'form': form}
    return render(request, template_name='../templates/pet/pet-edit-page.html', context=context)


def delete_pet(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    if request.method == "POST":
        pet.delete()
        return redirect('profile-details', pk=request.user.pk)
    form = PetDeleteForm(initial=pet.__dict__)
    context = {'form': form}
    return render(request, template_name='../templates/pet/pet-delete-page.html', context=context)
