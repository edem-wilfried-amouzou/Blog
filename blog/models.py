from multiprocessing import context
import re
from bs4 import BeautifulSoup

from django.db import models
from django.utils.html import escape
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from datetime import date
from modelcluster.models import ParentalKey, ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from django import forms
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.search import index


class BlogIndexPage(Page):
    description = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("description")]

    def get_context(self, request):
        context = super().get_context(request)
        blogposts = self.get_children().live().order_by("-first_published_at")
        context["blogposts"] = blogposts
        return context


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey("BlogPostPage", related_name="tagged_items",
                                 on_delete=models.CASCADE)

class BlogPostPage(Page):
    date = models.DateField("Post Date", default=date.today)
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField("blog.Author", blank=True)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    def main_image(self):
        thumbnail_image = self.image_gallery.first()
        if thumbnail_image:
            return thumbnail_image.image
        else:
            return None

    def get_table_of_contents(self):
        """Extrait les en-têtes du body et génère une table des matières"""
        if not self.body:
            return []
        
        soup = BeautifulSoup(self.body, 'html.parser')
        headings = []
        
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(heading.name[1])
            text = heading.get_text(strip=True)
            
            if not text:
                continue
            
            # Générer un ID unique à partir du texte
            heading_id = re.sub(r'[^\w\s-]', '', text.lower().strip())
            heading_id = re.sub(r'[-\s]+', '-', heading_id)
            heading_id = heading_id.strip('-')
            
            headings.append({
                'level': level,
                'text': text,
                'id': heading_id
            })
        
        return headings
    
    def get_body_with_ids(self):
        """Retourne le body avec les IDs ajoutés aux en-têtes"""
        if not self.body:
            return self.body
        
        soup = BeautifulSoup(self.body, 'html.parser')
        
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = heading.get_text(strip=True)
            
            if text:
                heading_id = re.sub(r'[^\w\s-]', '', text.lower().strip())
                heading_id = re.sub(r'[-\s]+', '-', heading_id)
                heading_id = heading_id.strip('-')
                heading['id'] = heading_id
        
        return str(soup.decode())

    content_panels = Page.content_panels + [FieldPanel("date"),
                                            FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
                                            FieldPanel("intro"),
                                            FieldPanel("body"),
                                            InlinePanel("image_gallery", label="gallery images"),
                                            FieldPanel("tags")
                                            ]

    search_fields = Page.search_fields + [index.SearchField("intro") ]

class BlogPageImageGallery(Orderable):
    page = ParentalKey(BlogPostPage, related_name="image_gallery", on_delete=models.CASCADE)
    image = models.ForeignKey("wagtailimages.Image", related_name="+", on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, blank=True)

    panels = [FieldPanel("image"), FieldPanel("caption")]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey("wagtailimages.Image", related_name="+", on_delete=models.CASCADE)
    panels = [FieldPanel("name"), FieldPanel("author_image")]

    def __str__(self):
        return self.name

class TagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get("tag")
        blogposts = BlogPostPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context["blogposts"] = blogposts
        return context