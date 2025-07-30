import json

from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators import clickjacking
from django.views.decorators.csrf import csrf_exempt

from .constants import VAR_INFO
from .utils.score_data import score_data


# Create your views here.
@clickjacking.xframe_options_exempt
def index(request):
    """
    Render the index page for the data-driven content app.
    """
    app_name = request.GET.get("app_name")
    context = {
        "var_info": VAR_INFO[app_name]["vars"],
        "app_name": app_name,
    }

    return render(request, "scoringForm.html", context)


@csrf_exempt
def score(request):
    """
    Render the score page for the data-driven content app.
    """
    if request.method == "POST":
        # Handle form submission
        try:
            data = json.loads(request.body)
            app_name = data["app_name"]
            data.pop("app_name")
            var_info = VAR_INFO[app_name]["vars"]
            module = VAR_INFO[app_name]["published_model_name"]
            output_label = VAR_INFO[app_name]["output_label"]
            clean_data = {}

            for key, value in data.items():
                element = next(filter(lambda x: x["label"] == key, var_info))
                if element["type"] == "number":
                    value = float(value)
                clean_data[element["name"]] = value

            scoring_results = score_data(clean_data, module)
            return JsonResponse(
                {
                    "status": "success",
                    "data": scoring_results,
                    "label": output_label,
                }
            )
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Invalid JSON data"}
        return None
    else:
        return JsonResponse(
            {"error": "Invalid request method. Please use POST."},
            status=400,
        )
