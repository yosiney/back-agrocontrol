from app.database import db
from bson import ObjectId

project_collection = db["projects"]

async def create_project(project):
    project_dict = project.dict() if hasattr(project, 'dict') else project
    result = await project_collection.insert_one(project_dict)
    return str(result.inserted_id)

async def list_projects():
    projects = []
    async for project in project_collection.find():
        project["_id"] = str(project["_id"])
        project["id"] = str(project["_id"])  # Para que coincida con el frontend
        projects.append(project)
    return projects

async def get_project(project_id: str):
    project = await project_collection.find_one({"_id": ObjectId(project_id)})
    if project:
        project["_id"] = str(project["_id"])
        project["id"] = str(project["_id"])  # Para que coincida con el frontend
    return project

async def update_project(project_id: str, project):
    result = await project_collection.update_one(
        {"_id": ObjectId(project_id)}, 
        {"$set": project}
    )
    return result.modified_count > 0

async def delete_project(project_id: str):
    result = await project_collection.delete_one({"_id": ObjectId(project_id)})
    return result.deleted_count > 0