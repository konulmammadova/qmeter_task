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
            - For example pipeline data format see READ.ME file
            [
                {
                    "branch_name": "user branch",
                    "service_name": "Customer service",
                    "ones": 26,
                    "twos": 10,
                    "threes": 20,
                    "fours": 10,
                    "fives": 18,
                    "total": 84,
                    "score": 9.523809523809524
                },
                {
                    "branch_name": "Branch 1",
                    "service_name": "Marketing Service",
                    "ones": 3,
                    "twos": 2,
                    "threes": 1,
                    "fours": 5,
                    "fives": 3,
                    "total": 14,
                    "score": -10.714285714285714
                }
            ]
        """

        client = MongoDBClient()
        result: List[Dict] = client.get_score_data()

        # Convert result to the desired context data format
        branch_data: Dict[str, List]= defaultdict(list) # provides data structure like { any_key: [], any_key: [], ... }
        
        for document in result:
            branch_name = document.get("branch_name") # using get, because some document branch names doesn't exist
            service_data = {
                "service_name": document["service_name"],
                "score": document["score"],
                "ones": document["ones"],
                "twos": document["twos"],
                "threes": document["threes"],
                "fours": document["fours"],
                "fives": document["fives"],
                "total": document["total"],
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
            - For example pipeline data format see READ.ME file
            {
            "branch_name": "Branch 1",
            "services":[
                    {
                        "service_name": "Customer service", 
                        "score": 6.25, 
                        "ones": 7, 
                        "twos": 4, 
                        "threes": 4, 
                        "fours": 3, 
                        "fives": 6, 
                        "total": 24
                    }, 
                    {
                        "service_name": "Marketing Service", 
                        "score": -10.714285714285714, 
                        "ones": 3, 
                        "twos": 2, 
                        "threes": 1, 
                        "fours": 5, 
                        "fives": 3, 
                        "total": 14
                    }, 
                    {
                        "service_name": "Quality of Service", 
                        "score": -100.0, 
                        "ones": 0, 
                        "twos": 0, 
                        "threes": 0, 
                        "fours": 0, 
                    "fives": 1, 
                        "total": 1
                    },
                ], 
            }
        """
        client = MongoDBClient()
        result: List[Dict] = client.get_score_data_by_branch()
        context= { "data": result }

        return context