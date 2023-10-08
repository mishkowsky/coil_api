from datetime import datetime
from typing import List
import uvicorn
from fastapi import Depends, HTTPException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session
from src import crud
from src.database.session import get_db
from src.schemas.coil import Coil, CoilCreate, GetCoilRequestBody, StatResponseBody, CoilUpdate, Range, CoilToUpdate

app = FastAPI()


@app.exception_handler(DatabaseError)
async def database_unavailable_exception(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )


@app.post('/coil', status_code=200, response_model=int)
def post_coil(new_coil: CoilCreate, db: Session = Depends(get_db)) -> int:
    """
    Create new coil with given length and weight characteristics
    """
    new_coil_db = crud.coil.create(db, obj_in=new_coil)
    return new_coil_db.id


@app.delete('/coil', status_code=204)
def delete_coil(coil_to_update: CoilToUpdate, db: Session = Depends(get_db)):
    """
    Delete coil with given id
    """
    coil_from_db = crud.coil.get(db=db, object_id=coil_to_update.id)
    if coil_from_db is None:
        raise HTTPException(status_code=404, detail=f"Coil with id={coil_to_update.id} not found")
    if coil_from_db.deleted_at is None:
        crud.coil.update(db=db, db_obj=coil_from_db, obj_in=CoilUpdate(deleted_at=datetime.now()))
    # else:
    #   coil was already deleted earlier,
    #   but the purpose of the call (delete coil with specific id) was achieved, so return 204


@app.get('/coil', status_code=200, response_model=List[Coil])
def get_coils(request: GetCoilRequestBody, db: Session = Depends(get_db)) -> List[Coil]:
    """
    Get a bunch of coils with characteristics that match given combination of ranges in request
    Start and end of each range are included
    """
    return crud.coil.get_coils_by_ranges(db, request)


@app.get('/coil/stats', status_code=200, response_model=StatResponseBody)
def get_stats(date_range: Range[datetime], db: Session = Depends(get_db)) -> StatResponseBody:
    """
    Get statistics for given range of dates
    Start and end of range are included
    """
    return crud.coil.get_stats(db=db, start_date=date_range.start, end_date=date_range.end)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
