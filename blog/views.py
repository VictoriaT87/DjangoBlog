from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post

# Create your views here.


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):

        # filter post only showing active
        queryset = Post.objects.filter(status=1)
        # get published post with correct slug
        post = get_object_or_404(queryset, slug=slug)
        # get comments attached to post and filter by aprroved and order by oldest first
        comments = post.comments.filter(approved=True).order_by('created_on')
        # if logged in user liked post, set to true, otherwise false
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        # render to template, make dictionary for context
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked
            },
        )
