import importlib
import os

urlpatterns = [
]

for entry in os.scandir(os.path.dirname(__file__)):
    if entry.is_file() and "__" not in entry.name:
        name = entry.name.split('.')[0]
        routingFile = importlib.import_module(__name__+"."+name)
        urlpatterns.extend(routingFile.urls)
