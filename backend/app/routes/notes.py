from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.utils.dependencies import get_current_user
from app.database.mongodb import get_database

router = APIRouter()

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    note_dict = note.model_dump()
    note_dict["owner_id"] = str(current_user["_id"])
    note_dict["created_at"] = datetime.utcnow()
    note_dict["updated_at"] = datetime.utcnow()
    
    result = await db["notes"].insert_one(note_dict)
    created_note = await db["notes"].find_one({"_id": result.inserted_id})
    return created_note

@router.get("/", response_model=List[NoteResponse])
async def read_notes(current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    if current_user.get("role") == "admin":
        notes_cursor = db["notes"].find({})
    else:
        notes_cursor = db["notes"].find({"owner_id": str(current_user["_id"])})
    
    notes = await notes_cursor.to_list(length=100)
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(note_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    if not ObjectId.is_valid(note_id):
        raise HTTPException(status_code=400, detail="Invalid note ID")
    
    note = await db["notes"].find_one({"_id": ObjectId(note_id)})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    if current_user.get("role") != "admin" and note["owner_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: str, note_update: NoteUpdate, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    if not ObjectId.is_valid(note_id):
        raise HTTPException(status_code=400, detail="Invalid note ID")
        
    existing_note = await db["notes"].find_one({"_id": ObjectId(note_id)})
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    if current_user.get("role") != "admin" and existing_note["owner_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    update_data = {k: v for k, v in note_update.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await db["notes"].update_one({"_id": ObjectId(note_id)}, {"$set": update_data})
    updated_note = await db["notes"].find_one({"_id": ObjectId(note_id)})
    return updated_note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    if not ObjectId.is_valid(note_id):
        raise HTTPException(status_code=400, detail="Invalid note ID")
        
    existing_note = await db["notes"].find_one({"_id": ObjectId(note_id)})
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    if current_user.get("role") != "admin" and existing_note["owner_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    await db["notes"].delete_one({"_id": ObjectId(note_id)})
    return None
