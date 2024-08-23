from collections import defaultdict
from typing import Dict, List

from django.shortcuts import render
from django.views.generic import TemplateView

from qmeter.client import MongoDBClient

class ScoreTable1View(TemplateView):
    template_name = "feedback/score_table.html"

    def get_context_data(self, **kwargs) -> Dict[str, List[Dict[str, any]]]:
        """
            - Methods type hint above, represents data format that will be used in table of html page
            - For explanation pipeline data format see READ.ME file
        """

        client = MongoDBClient()
        result: List[Dict] = client.get_score_data()

        # Convert result to the desired context data format
        branch_data: Dict[str, List]= defaultdict(list) # provides data structure like { any_key: [], any_key: [], ... }
        
        for document in result:
            branch_name = document.get("branch_name")
            service_data = {
                "service_name": document.get("service_name"),
                "score": document.get("score"),
                "ones": document.get("ones"),
                "twos": document.get("twos"),
                "threes": document.get("threes"),
                "fours": document.get("fours"),
                "fives": document.get("fives"),
                "total": document.get("total"),
            }
            branch_data[branch_name].append(service_data)
        
        data = [
            {
                "branch_name": branch_name,
                "services": services
            }
            for branch_name, services in branch_data.items()
        ]
        
        context= { "data": data }

        return context

class ScoreTable2View(TemplateView):
    template_name = "feedback/score_table.html"

    def get_context_data(self, **kwargs) -> Dict[str, List[Dict[str, any]]]:
        """
            - Methods type hint above, represents data format that will be used in table of html page
            - For explanation of pipeline data format see READ.ME file
            
        """
        client = MongoDBClient()
        result: List[Dict] = client.get_score_data_by_branch()
        context= { "data": result }

        return context