from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from PIL import Image

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profiles/%y/%m/%d',default='profiles/default.jpg')
    def save(self,*args,**kwargs):
    
      img = Image.open(self.profile_pic.file)
      if img.height > 150 or img.width > 150:
         output_size = (150, 150)
         img.thumbnail(output_size)
         img.save(self.profile_pic.path)
      super().save(*args,**kwargs)

      



from ckeditor.fields import RichTextField
class CreatePost(models.Model):
    title=models.CharField(max_length=300,blank=False)
    content = RichTextField()
    created_at=models.DateField(auto_now_add=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering=["-created_at"]



# Optionally, you can create a custom admin class
class CreatePostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # Columns to display in the list view
    search_fields = ('title', 'author__username')  # Fields to include in the search box
    list_filter = ('created_at', 'author')  # Filters available in the right sidebar
    ordering = ('-created_at',)  # Default ordering in the admin list view
    fields = ('title', 'content', 'author')  # Fields to display in the detail view

# Register your model with the custom admin class
admin.site.register(CreatePost, CreatePostAdmin)