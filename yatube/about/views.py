from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = "about/author.html"


class AboutTechView(TemplateView):
    template_name = "about/tech.html"


class JustStaticPage(TemplateView):
    template_name = "app_name/just_page.html"


class JustStaticPage(TemplateView):
    template_engine = "posts/post_detail.html"
