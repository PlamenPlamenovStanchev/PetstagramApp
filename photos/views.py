from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from common.forms import CommentForm
from photos.forms import PhotoCreateForm, PhotoEditForm
from photos.models import Photo



class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoCreateForm
    success_url = reverse_lazy('home')
    template_name = 'photos/photo-add-page.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


#function base view option
#def photo_add_view(request: HttpRequest) -> HttpResponse:
#    form = PhotoCreateForm(request.POST or None, request.FILES or None)

#    if request.method == "POST" and form.is_valid():
#        form.save()
#        return redirect("home")

#    context = {
#        'form': form,
#        }

#    return render(request, 'photos/photo-add-page.html', context)


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photos/photo-details-page.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'comments': self.object.comment_set.all(),
            'comment_form': CommentForm(),
        })
        return super().get_context_data(**kwargs)


#function base view option
#def photo_details_view(request: HttpRequest, pk: int) -> HttpResponse:
#    photo = Photo.objects.get(pk=pk)
#    comments = photo.comment_set.all()
#    comment_form = CommentForm()

#    context = {
#        'photo': photo,
#        'comments': comments,
#        'comment_form': comment_form,
#    }
#    return render(request, 'photos/photo-details-page.html', context)



class PhotoEditView(UpdateView):
    model = Photo
    form_class = PhotoEditForm
    template_name = 'photos/photo-edit-page.html'
    success_url = reverse_lazy('home')

#def photo_edit_view(request: HttpRequest, pk: int) -> HttpResponse:
#    photo = Photo.objects.get(pk=pk)
#    form = PhotoEditForm(request.POST or None, instance=photo)

#    if request.method == "POST" and form.is_valid():
#        form.save()
#        return redirect('home')

#    context = {
#        'photo': photo,
#        'form': form,
#    }

#    return render(request, 'photos/photo-edit-page.html', context)
@login_required
def photo_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    photo = Photo.objects.get(pk=pk)

    if request.user.pk == photo.user.pk:
        photo.delete()
        return redirect('home')

    return HttpResponseForbidden()
