from django.db import models
import uuid
from users.models import Profile
# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True,blank=True, on_delete=models.CASCADE)
    project_uuid = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True,blank=True)
    project_image = models.ImageField(null=True,blank=True,default='default.jpg')
    demo_link = models.CharField( max_length=1000,null=True,blank=True)
    source_link = models.CharField( max_length=1000,null=True,blank=True)
    tags = models.ManyToManyField('Tag', blank=True) # the quotes required as tag is defined below
    vote_total = models.IntegerField(default=0,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__profile_uuid',flat=True)
        print(queryset)
        return queryset 
    

    class Meta:
        ordering = ['-vote_total','title']
    

class Review(models.Model):
    
    VOTE_TYPE = (
        ('up','Up Vote'),
        ('down','Down Vote'),
    )

    review_uuid = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    body = models.TextField(null=True,blank=True)
    value = models.CharField(choices=VOTE_TYPE, max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['owner','project']] # it ensures that no single user can do multiple comments on same project

    def __str__(self):
        return self.value
    
class Tag(models.Model):
    tag_uuid = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    name = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
