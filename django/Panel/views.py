from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from Panel.models import UploadedModel, Dataset, ModelExperimentConnection, Experiment, ModelBenchmark
from Panel.models_layer import check_dataset_dataset_compatibility, create_benchmark
from Panel.models_layer import check_model_dataset_compatibility
import json
import uuid
import os



def panel(request):
    if "id" not in request.session:
        return HttpResponseRedirect("/auth")

    um = UploadedModel.objects.all()
    ds = Dataset.objects.all()

    groups = list(Dataset.objects.order_by().values_list('dataset_group', flat=True).distinct())
    print("GROUPS: ", groups)
    grouped_datasets = []
    for group_name in groups:
        if Dataset.objects.filter(dataset_group=group_name).count() > 0:
            grouped_datasets.append(Dataset.objects.filter(dataset_group=group_name))    

    exp = Experiment.objects.all()
    return render(request, "Panel.html", {
            "uploaded_models": um, 
            "datasets": grouped_datasets, 
            "scheme": settings.SCHEME, 
            "domain": settings.DOMAIN,
            "experiments": exp,
        })


def handle_uploaded_file(f, destination_folder):
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
    
    filename = str(f)
    extention = filename.split(".")[-1]
    new_filename = str(uuid.uuid4()) + "." + extention
    destination_path = os.path.join(destination_folder, new_filename)


    with open(destination_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return new_filename, destination_path


def upload_model(request):
    if "id" not in request.session:
        return HttpResponseRedirect("/auth")

    if request.method == "POST":
        model_name = request.POST["name"]
        model_description = request.POST["description"]
        model_type = request.POST["model_type"]
        target_type = request.POST["target_type"]
        model_file = request.FILES["model_file"]
        scheme_file = request.FILES["scheme_file"]

        models_folder = os.path.join(settings.BASE_DIR, "static", "models")
        scheme_folder = os.path.join(settings.BASE_DIR, "static", "scheme")

        model_file_filename, model_file_path = handle_uploaded_file(model_file, models_folder)
        scheme_file_filename, scheme_file_path = handle_uploaded_file(scheme_file, scheme_folder)

        model = UploadedModel(name=model_name, description=model_description, model_type=model_type, 
            target_type=target_type, model_file_name=model_file_filename, model_file_path=model_file_path,
            scheme_file_name=scheme_file_filename, scheme_file_path=scheme_file_path)
        model.save()

        return render(request, "Message.html", {"type": "info", "title": "File uploaded", "description": "Model file was successfully uploaded on the server!"})

    return HttpResponseRedirect("/panel")        


def create_dataset(request):
    if "id" not in request.session:
        return HttpResponseRedirect("/auth")

    if request.method == "POST":
        group_name = request.POST["name"]
        model_description = request.POST["description"]
        scheme_file = request.FILES["scheme_file"]

        scheme_folder = os.path.join(settings.BASE_DIR, "static", "scheme")
        scheme_file_filename, scheme_file_path = handle_uploaded_file(scheme_file, scheme_folder)


        ds = Dataset(description=model_description, scheme_file_name=scheme_file_filename, scheme_file_path=scheme_file_path, dataset_group=group_name)
        ds.save()

        api_link = f"{settings.SCHEME}://{settings.DOMAIN}/panel/updateDataset/{ds.dataset_group}"

        message = f"You can use link <a href='{api_link}'>{api_link}</a> to update dataset."
        return render(request, "Message.html", {"type": "info", "title": "Dataset created", "description": message})

    return HttpResponseRedirect("/panel")     


def create_experiment(request):
    if "id" not in request.session:
        return HttpResponseRedirect("/auth")

    if request.method == "POST":
        dataset_group = request.POST["dataset_group"]
        experiment_name = request.POST["experiment_name"]
        experiment_description = request.POST["experiment_description"]

        dataset = Dataset.objects.filter(dataset_group=dataset_group)[0]

        experiment = Experiment(dataset_group=dataset_group, name=experiment_name, description=experiment_description)
        experiment.save()

        models = UploadedModel.objects.all()
        for model in models:
            if not check_model_dataset_compatibility(model, dataset):
                return render(request, "Message.html", {"type": "error", "title": "Dataset and model are incompatible"})

            if f"modelCheck{model.id}" in request.POST:
                mec = ModelExperimentConnection(model=model, experiment=experiment)
                mec.save()
            
        return HttpResponseRedirect(f"/panel/experiment/{experiment.id}")

    return HttpResponseRedirect("/panel")     


@csrf_exempt
def update_dataset(request, dataset_group):
    if request.method == "GET":
        return render(request, "UpdateDataset.html", {"dataset_group": dataset_group})
   
    dataset = request.FILES["dataset"]
    description = request.POST["description"]
    
    datasets_folder = os.path.join(settings.BASE_DIR, "static", "datasets")
    dataset_file_name, dataset_file_path = handle_uploaded_file(dataset, datasets_folder)

    ds = Dataset.objects.filter(dataset_group=dataset_group)[0]

    if not check_dataset_dataset_compatibility(dataset_file_path, ds.scheme_file_path):
        return JsonResponse({"ok": False, "error": "Dataset is incompatible!"})

    new_ds = Dataset(dataset_group=dataset_group, description=description, 
            scheme_file_name = ds.scheme_file_name, scheme_file_path = ds.scheme_file_path, 
            dataset_file_name=dataset_file_name, dataset_file_path=dataset_file_path,
        )
    new_ds.save()

    
    n_exp = Experiment.objects.filter(dataset_group=dataset_group)
    for exp in n_exp:
        models = ModelExperimentConnection.objects.filter(experiment=exp)
        benchmarks = {}
        for model in models:
            create_benchmark(model.model, new_ds)



    return JsonResponse({"ok": True})


def show_experiment(request, experiment_id):
    if "id" not in request.session:
        return HttpResponseRedirect("/auth")
    experiment = Experiment.objects.get(id=experiment_id)

    print("Experiment: ", experiment)

    dataset_group = experiment.dataset_group
    datasets = Dataset.objects.filter(dataset_group=dataset_group).order_by("upload_date")

    print("Datasets: ", datasets)

    if len(datasets) <= 1:
        return render(request, "Message.html", {"type": "error", "title": "No data for this experiment!", "description": "No uploaded data from API."})

    mec = ModelExperimentConnection.objects.filter(experiment=experiment)
    models = [ m.model for m in mec ]
    
    print("MODELS: ", models)

    metric_objects = []
    metrics = []
    for model in models:
        model_metrics = []
        model_metric_objects =[]
        for dataset in datasets:
            if ModelBenchmark.objects.filter(dataset=dataset, model=model).count() > 0:
                model_metric_objects.append(ModelBenchmark.objects.get(dataset=dataset, model=model))
                model_metrics.append(json.loads(model_metric_objects[-1].metrics))
        metric_objects.append(model_metric_objects)
        metrics.append(model_metrics)

    print("METRICS: ", metrics)


    data = {}
    for metric_name in metrics[0][0].keys():
        data[metric_name] = [json.dumps([metrics[mod_i][mon_i][metric_name] for mon_i, mon in enumerate(mod)]) for mod_i, mod in enumerate(metrics)]

    # model_metrics_by_name = []
    # for keklol in metrics:
    #     metrics_by_name = {}
    #     for metric_name in keklol[0].keys():
    #         metrics_by_name[metric_name] = json.dumps([met[metric_name] for met in keklol])
    #     model_metrics_by_name.append(metrics_by_name)


    return render(request, "Compare.html", {"metrics": metrics, "datasets": datasets,
        "models": models, "data": data, "experiment": experiment})