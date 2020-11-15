from django.db import models


class UploadedModel(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    model_type = models.CharField(max_length=32)
    target_type = models.CharField(max_length=32)
    model_file_name = models.CharField(max_length=128)
    scheme_file_name = models.CharField(max_length=128)
    model_file_path = models.CharField(max_length=128)
    scheme_file_path = models.CharField(max_length=128)

    def __str__(self):
        return self.name

 
class Dataset(models.Model):
    description = models.TextField()
    scheme_file_name = models.CharField(max_length=128)
    scheme_file_path = models.CharField(max_length=128)
    upload_date = models.DateField(auto_now=True, null=True)
    dataset_group = models.CharField(max_length=64)
    dataset_file_path = models.CharField(max_length=128, default="", editable=False)
    dataset_file_name = models.CharField(max_length=128, default="", editable=False)

    def __str__(self):
        return self.dataset_group + " " + str(self.upload_date)



class Experiment(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    dataset_group = models.CharField(max_length=64)
    pairwise_raitings = models.TextField()
    singular_raitings = models.TextField()


class ModelExperimentConnection(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    model = models.ForeignKey(UploadedModel, on_delete=models.CASCADE)


class ModelBenchmark(models.Model):
    model = models.ForeignKey(UploadedModel, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    order = models.IntegerField()
    metrics = models.TextField()