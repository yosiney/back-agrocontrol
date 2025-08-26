from fastapi import APIRouter, HTTPException, Body
from app.models.project_model import Project
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", summary="Create a new project")
async def create_project(project: Project):
    project_id = await project_service.create_project(project)
    return {"id": project_id, "message": "Project created successfully"}

@router.get("/", summary="List all projects")
async def list_projects():
    return await project_service.list_projects()

@router.get("/{project_id}", summary="Get project by ID")
async def get_project(project_id: str):
    project = await project_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", summary="Delete project")
async def delete_project(project_id: str):
    deleted = await project_service.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}

@router.patch("/{project_id}", summary="Update a project")
async def patch_project(project_id: str, project: dict = Body(...)):
    updated = await project_service.update_project(project_id, project)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found or no changes made")
    return {"id": project_id, "message": "Project updated successfully"}

# services/project_service.py
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