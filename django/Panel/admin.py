from django.contrib import admin
from Panel.models import UploadedModel, Dataset, Experiment, ModelExperimentConnection, ModelBenchmark

admin.site.register(UploadedModel)
admin.site.register(Dataset)
admin.site.register(Experiment)
admin.site.register(ModelExperimentConnection)
admin.site.register(ModelBenchmark)

