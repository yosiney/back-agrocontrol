from app.database import db
from datetime import datetime
from bson.son import SON

expense_collection = db["expenses"]

async def report_by_date(start_date: str = None, end_date: str = None, group_by: str = "month", category: str = None):
    match_filters = {}

    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        match_filters["date"] = {"$gte": start, "$lte": end}

    if category:
        match_filters["category"] = category

    match_stage = {"$match": match_filters} if match_filters else {}

    if group_by == "day":
        group_id = {
            "day": {"$dayOfMonth": "$date"},
            "month": {"$month": "$date"},
            "year": {"$year": "$date"}
        }
    elif group_by == "year":
        group_id = {"year": {"$year": "$date"}}
    else:  # default = month
        group_id = {"month": {"$month": "$date"}, "year": {"$year": "$date"}}

    pipeline = []
    if match_stage:
        pipeline.append(match_stage)
    pipeline.append({
        "$group": {
            "_id": group_id,
            "total_spent": {"$sum": "$cost"},
            "count": {"$sum": 1}
        }
    })
    pipeline.append({"$sort": SON([("_id.year", 1), ("_id.month", 1)])})

    results = await expense_collection.aggregate(pipeline).to_list(length=None)
    return results


async def report_by_category(start_date: str = None, end_date: str = None, category: str = None):
    match_filters = {}

    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        match_filters["date"] = {"$gte": start, "$lte": end}

    if category:
        match_filters["category"] = category

    match_stage = {"$match": match_filters} if match_filters else {}

    pipeline = []
    if match_stage:
        pipeline.append(match_stage)
    pipeline.append({
        "$group": {
            "_id": "$category",
            "total_spent": {"$sum": "$cost"},
            "count": {"$sum": 1}
        }
    })
    pipeline.append({"$sort": {"total_spent": -1}})

    results = await expense_collection.aggregate(pipeline).to_list(length=None)
    return results
