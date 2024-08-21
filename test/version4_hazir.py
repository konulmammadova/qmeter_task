[
    {
        "$unwind": "$feedback_rate"
    },
    {
        "$group": {
            "_id": {
                "branch_name": "$branch.name",
                "service_name": "$feedback_rate.service.name"
            },
            "ones": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 1] }, 1, 0] }},
            "twos": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 2] }, 1, 0] }},
            "threes": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 3] }, 1, 0] }},
            "fours": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 4] }, 1, 0] }},
            "fives": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 5] }, 1, 0] }}
        }
    },
    {
        "$addFields": {
            "total": { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] },
            "weightedSum": {
                "$add": [
                    { "$multiply": ["$ones", 10] },
                    { "$multiply": ["$twos", 5] },
                    { "$multiply": ["$fours", -5] },
                    { "$multiply": ["$fives", -10] }
                ]
            }
        }
    },
    {
        "$addFields": {
            "score": {
                "$cond": {
                    "if": { "$gt": ["$total", 0] },
                    "then": {
                        "$multiply": [
                            { "$divide": [{ "$multiply": ["$weightedSum", 100] }, { "$multiply": ["$total", 10] }] },
                            1
                        ]
                    },
                    "else": 0
                }
            }
        }
    },
    {
        "$group": {
            "_id": "$_id.branch_name",
            "services": {
                "$push": {
                    "service_name": "$_id.service_name",
                    "score": "$score"
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "branch_name": "$_id",
            "services": 1
        }
    }
]