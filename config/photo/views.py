from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Photo
from create_profile.models import Profile
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect

from django.contrib import messages


class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'
    #
    # def get_queryset(self):
    #     return PhotoList.objects.filter(user=self.request.user)

class PhotoCreate(CreateView):
    model = Photo
    # fields = ['author','text', 'image']
    fields = ['text', 'image']

    template_name_suffix = '_create'
    # success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user.user_profile
        if form.is_valid():
            # 올바르다면
            # form : 모델폼
            form.instance.save()
            return redirect('photo:index')
        else:
            # 올바르지 않다면
            return self.render_to_response({'form': form})




class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_update'
    # success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user.user_profile:
            messages.warning(request, '수정할 권한이 없습니다.')
            return redirect('photo:detail')
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)

class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/photo/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user.user_profile:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return redirect('photo:detail')
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)


class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'


from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse


class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:    #로그인확인
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)


class PhotoLikeList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 내가 좋아요한 글을 보여주
        user = self.request.user
        queryset = user.like_post.all()
        return queryset



class PhotoMyList(ListView):
    model = Photo
    template_name = 'photo/photo_mylist.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoMyList, self).dispatch(request, *args, **kwargs)


