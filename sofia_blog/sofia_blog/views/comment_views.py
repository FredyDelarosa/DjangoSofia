from django.views.generic import ListView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from ..models.comment import Comment
from ..models.movie import Movie
from ..forms.comment_form import CommentForm

class CommentListView(ListView):
    model = Comment
    template_name = "comments/comment_list.html"
    context_object_name = "comments"

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Comment.objects.filter(movie_id=movie_id)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/comment_form.html"

    def form_valid(self, form):
        movie = get_object_or_404(Movie, id=self.kwargs['movie_id'])
        comment = form.save(commit=False)
        comment.movie = movie
        comment.user = self.request.user
        comment.save()
        return redirect('movie_detail', pk=movie.id)
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/comment_form.html"

    def get_success_url(self):
        movie = self.object.movie  # Obtener la película relacionada con el comentario
        if not movie or not movie.id:
            print(f"Error: Comentario {self.object.id} no tiene una película asociada.")  # Depuración
            return reverse_lazy('movie_list')  # Redirigir a la lista de películas si no hay una película válida
        
        print(f"Redirigiendo a movie_detail con ID: {movie.id}")  # Depuración
        return reverse_lazy('movie_detail', kwargs={'pk': movie.id})

    def test_func(self):
        return self.request.user == self.get_object().user  # Solo el autor puede editar

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "comments/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy('movie_detail', kwargs={'pk': self.object.movie.id})
