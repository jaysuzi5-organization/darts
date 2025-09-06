from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from framework.db import get_db
from models.darts import darts, dartsCreate
from datetime import datetime, UTC

router = APIRouter()

def serialize_sqlalchemy_obj(obj):
    """
    Convert a SQLAlchemy ORM model instance into a dictionary.

    Args:
        obj: SQLAlchemy model instance.

    Returns:
        dict: Dictionary containing all column names and their values.
    """
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


@router.get("/api/v1/darts")
def list_darts(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    limit: int = Query(10, ge=1, le=1000, description="Number of records per page"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of darts records.

    Args:
        page (int): Page number starting from 1.
        limit (int): Maximum number of records to return per page.
        db (Session): SQLAlchemy database session.

    Returns:
        list[dict]: A list of serialized darts records.
    """
    try:
        offset = (page - 1) * limit
        darts_records = db.query(darts).offset(offset).limit(limit).all()
        return [serialize_sqlalchemy_obj(item) for item in darts_records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/api/v1/darts")
def create_record(
    darts_data: dartsCreate = Body(..., description="Data for the new record"),
    db: Session = Depends(get_db)
):
    """
    Create a new darts record.

    Args:
        darts_data (dartsCreate): Data model for the record to create.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The newly created darts record.
    """
    try:
        data = darts_data.model_dump(exclude_unset=True)
        new_record = darts(**data)
        new_record.create_date = datetime.now(UTC)
        new_record.update_date = datetime.now(UTC)

        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return serialize_sqlalchemy_obj(new_record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/api/v1/darts/{id}")
def get_darts_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single darts record by ID.

    Args:
        id (int): The ID of the record.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The matching darts record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(darts).filter(darts.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"darts with id {id} not found")
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/api/v1/darts/{id}")
def update_darts_full(
    id: int,
    darts_data: dartsCreate = Body(..., description="Updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Fully update an existing darts record (all fields required).

    Args:
        id (int): The ID of the record to update.
        darts_data (dartsCreate): Updated record data (all fields).
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated darts record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(darts).filter(darts.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"darts with id {id} not found")

        data = darts_data.model_dump(exclude_unset=False)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/api/v1/darts/{id}")
def update_darts_partial(
    id: int,
    darts_data: dartsCreate = Body(..., description="Partial updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Partially update an existing darts record (only provided fields are updated).

    Args:
        id (int): The ID of the record to update.
        darts_data (dartsCreate): Partial updated data.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated darts record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(darts).filter(darts.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"darts with id {id} not found")

        data = darts_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/api/v1/darts/{id}")
def delete_darts(id: int, db: Session = Depends(get_db)):
    """
    Delete a darts record by ID.

    Args:
        id (int): The ID of the record to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(darts).filter(darts.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"darts with id {id} not found")

        db.delete(record)
        db.commit()
        return {"detail": f"darts with id {id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
