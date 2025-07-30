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
    context = {
        "var_info": VAR_INFO["cars-price-estimation"]["vars"],
    }

    return render(request, "scoringForm.html", context)


@csrf_exempt
def score(request):
    """
    Render the score page for the data-driven content app.
    """
    var_info = VAR_INFO["cars-price-estimation"]["vars"]
    if request.method == "POST":
        # Handle form submission
        try:
            data = json.loads(request.body)
            clean_data = {}

            for key, value in data.items():
                element = next(filter(lambda x: x["label"] == key, var_info))
                if element["type"] == "number":
                    value = float(value)
                clean_data[element["name"]] = value

            scoring_results = score_data(clean_data, "cars_price_estimation")
            return JsonResponse(
                {
                    "status": "success",
                    "data": scoring_results,
                    "label": VAR_INFO["cars-price-estimation"]["output_label"],
                }
            )
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Invalid JSON data"}
        # scoring_results = score_data(request, "cars_price_estimation")
        # print("Scoring results:", scoring_results)
        # # Here you would typically process the data, e.g., save it to the database or perform calculations
        # return JsonResponse(
        #     {
        #         "best_price": 25000,  # Example static value, replace with actual logic
        #         "label": "Best price",
        #     }
        # )
        return None
    else:
        return JsonResponse(
            {"error": "Invalid request method. Please use POST."},
            status=400,
        )
