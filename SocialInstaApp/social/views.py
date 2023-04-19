from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,ListView,DetailView,UpdateView,TemplateView,FormView
from django.contrib.auth.models import User
from social.models import UserProfile,Posts,Comments
from social.forms import RegistationForm,LoginForm,UserProfileForm,PostForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# Create your views here.

# Decerator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not  request.user.is_authenticated :
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
  
decs=[signin_required,never_cache]













@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
     model=Posts
     form_class=PostForm
     template_name="home.html"
     success_url=reverse_lazy("home")
     context_object_name="posts"

     def form_valid(self, form) :
         form.instance.user=self.request.user
         return super().form_valid(form)
    
     def get_queryset(self):
         return Posts.objects.all().order_by("-created_date")
     

     def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        userprofiles=UserProfile.objects.all()
        lst=[]
        for pro in userprofiles:
            for u in pro.Following.all():
                lst.append(u)
        print("followers count of loggined user",lst.count(self.request.user))
        context['fwsc']=lst.count(self.request.user)
        return context
                 
             
             
     
# for changing the orm query for any occation suchthat sorting or rechanging in a order we must override the method deg get_queryset?()
    
    
   



class SignUpView(CreateView):
    model=User
    template_name="register.html"
    form_class=RegistationForm
    success_url=reverse_lazy("signin")

@signin_required
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

class SignInView(FormView):
    form_class=LoginForm
    template_name="signin.html"

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                print(usr)
                login(request,usr)
                return redirect("home")
            else:
                return render(request,self.template_name,{"form":form})


@method_decorator(decs,name="dispatch")
class ProfileCreationView(CreateView):
    form_class=UserProfileForm
    template_name="profile-add.html"
    success_url=reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    


    # def post(self,request,*args,**kwargs):
    #     form=UserProfileForm(request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.instance.u

@method_decorator(decs,name="dispatch")
class MyProfileView(TemplateView):
    template_name="profile-detail.html"
   
@method_decorator(decs,name="dispatch")
class ProfileEditView(UpdateView):
    model=UserProfile
    form_class=UserProfileForm
    template_name="profile-edit.html"
    success_url=reverse_lazy("home")




@method_decorator(decs,name="dispatch")
class AddCommentView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        pst=Posts.objects.get(id=id)
        usr=request.user
        cmnt=request.POST.get("comment")
        Comments.objects.create(user=usr,post=pst,comment=cmnt)
        return redirect("home")
    
@method_decorator(decs,name="dispatch")
class AddLikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        pst=Posts.objects.get(id=id)
        pst.liked_by.add(request.user)
        pst.save()
        return redirect("home")
    
def following_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    usr=User.objects.get(id=id)
    request.user.profile.Following.add(usr)
    return redirect("home")