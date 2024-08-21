# with addField

[
  {
    $unwind: "$feedback_rate"
  },
  {
    $group: {
      _id: {
        branch_name: "$branch.name",
        service_name:
          "$feedback_rate.service.name"
      },
      
        ones: { $sum: { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 1] }, 1, 0]} },
        twos: { $sum: { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 2] }, 1, 0]} },
        threes: { $sum: { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 3] }, 1, 0]} },
        fours: { $sum: { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 4] }, 1, 0]} },
        fives: { $sum: { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 5] }, 1, 0]} }
    }
  },
  {
    $addFields: {
      score: {
        $cond: { if: { $gt: [{ $sum: ["$ones", "$twos", "$threes", "$fours", "$fives"] }, 0] },
          then: {
            $divide: [
              {
                $multiply: [
                  100,
                  {
                    $sum: [
                        { "$multiply": ["$ones", 10] },
                        { "$multiply": ["$twos", 5] },
                        { "$multiply": ["$fours", -5] },
                        { "$multiply": ["$fives", -10] }
                    ]
                  }
                ]
              },
              {
                $multiply: [
                  { "$sum": ["$ones", "$twos", "$threes", "$fours", "$fives"] },
                  10
                ]
              }
            ]
          },
          else: 0
        }
      }
    }
  },
  {
    $project: {
      _id: 0,
      branch_name: "$_id.branch_name",
      service_name: "$_id.service_name",
      score: 1
    }
  }
]