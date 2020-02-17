from django.template.loaders.app_directories import Loader as AppDirectoryLoader
from markdown import markdown


class MarkdownLoader(AppDirectoryLoader):
    def get_contents(self, origin):
        content = super().get_contents(origin)
        if origin.name.endswith(".md"):
            content = markdown(content)
        return content
