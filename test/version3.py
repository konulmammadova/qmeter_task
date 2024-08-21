[
    # Unwind the feedback_rate array
    { "$unwind": "$feedback_rate" },
    
    # Group by branch name and service name
    {
        "$group": {
            "_id": {
                "branch_name": "$branch.name",
                "service_name": "$feedback_rate.service.name"
            },
            "rate_options": { "$push": "$feedback_rate.rate_option" }
        }
    },
    
    # Calculate the score based on the rate_options
    {
        "$project": {
            "_id": 0,
            "branch_name": "$_id.branch_name",
            "service_name": "$_id.service_name",
            "score": {
                "$multiply": [
                    100,
                    {
                        "$divide": [
                            {
                                "$add": [
                                    {
                                        "$multiply": [
                                            { "$size": { "$filter": { "input": "$rate_options", "as": "rate", "cond": { "$eq": [ "$$rate", 1 ] } } } },
                                            10
                                        ]
                                    },
                                    {
                                        "$multiply": [
                                            { "$size": { "$filter": { "input": "$rate_options", "as": "rate", "cond": { "$eq": [ "$$rate", 2 ] } } } },
                                            5
                                        ]
                                    },
                                    {
                                        "$multiply": [
                                            { "$size": { "$filter": { "input": "$rate_options", "as": "rate", "cond": { "$eq": [ "$$rate", 3 ] } } } },
                                            0
                                        ]
                                    },
                                    {
                                        "$multiply": [
                                            { "$size": { "$filter": { "input": "$rate_options", "as": "rate", "cond": { "$eq": [ "$$rate", 4 ] } } } },
                                            -5
                                        ]
                                    },
                                    {
                                        "$multiply": [
                                            { "$size": { "$filter": { "input": "$rate_options", "as": "rate", "cond": { "$eq": [ "$$rate", 5 ] } } } },
                                            -10
                                        ]
                                    }
                                ]
                            },
                            {
                                "$cond": [
                                    { "$gt": [ { "$size": "$rate_options" }, 0 ] },
                                    { "$size": "$rate_options" },
                                    1
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    },
    
    # Group by branch name and combine scores for services
    {
        "$group": {
            "_id": "$branch_name",
            "services": {
                "$push": {
                    "service_name": "$service_name",
                    "score": "$score"
                }
            }
        }
    }
]