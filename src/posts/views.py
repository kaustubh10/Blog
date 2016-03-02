from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm
from .models import Post
def post_create(request):
	
	form = PostForm(request.POST or None, request.FILES or None)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form":form
	}
	return render(request,"form.html",context)

def post_retrieve(request, id):
	instance = get_object_or_404(Post,id=id)
	context = {
		"instance":instance,
		"title": "Detail"
	}
	return render(request,"detail.html",context)

def post_list(request):
	queryset = Post.objects.order_by('-timestamp')
	Count = Post.objects.count()
	paginator = Paginator(queryset, 2) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		lists = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		lists = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		lists = paginator.page(paginator.num_pages)

	context = {
		"count": Count,
		"object_list": queryset,
		"title": "list",
		"lists":lists
	}
	return render(request, "list.html",context)
	#return HttpResponse("<h1>Hello</h1>")

def post_update(request, id):
	instance = get_object_or_404(Post,id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"instance":instance,
		"title": instance.title,
		"form":form
	}
	return render(request,"form.html",context)

def post_delete(request, id):
	instance = get_object_or_404(Post,id=id)
	instance.delete()
	return redirect("/posts/")



# Create your views here.
