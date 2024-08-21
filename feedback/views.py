from django.shortcuts import render
from django.views.generic import TemplateView
from qmeter.client import get_score_data, get_service_scores_by_branch

class ScoreTable1View(TemplateView):
    template_name = 'score_table1.html'

    def get_context_data(self, **kwargs):
        result = get_score_data()
        print("HEREEEEEEEEEEEEEEEEEEEEEEE")
        print(result["data"][0])
        print(result)
        return result

class ScoreTable2View(TemplateView):
    template_name = 'score_table1.html'

    def get_context_data(self, **kwargs):
        result = get_service_scores_by_branch()
        # print(result)
        return result