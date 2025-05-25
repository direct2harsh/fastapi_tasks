from fastapi import APIRouter, Depends, status,HTTPException,Query
from sqlalchemy import desc
from sqlalchemy.orm import Session 
from auth.auth_config import validate_current_user
from db.connection import get_db
from db.schema import Tasks
from models.auth_models import AuthenticatedUser
from models.tasks_models import CreateTask, PaginatedTasksResponse, UpdateTask
from uuid import UUID
from typing import Optional
from datetime import datetime,timezone



router = APIRouter(prefix="/tasks",tags=["Tasks"])

""" User id based task creation is not done here as creating user was not part of this assignment and only one task table was in picture.
    But it can be easily achived, by adding a new Table with foreign key relation with userID and the tasks UUID.    
"""

@router.get("/get",)
async def all_task(
    last_task_id: Optional[UUID]= Query(
        None,
        description="UUID of the next_task from the previous page"
    ) ,last_task_at: Optional[datetime]= Query(
        None,
        description="Timestamp of the next_task_at from the previous page in (UTC)"
    ), 
    db:Session =Depends(get_db), user: AuthenticatedUser = Depends(validate_current_user)):
    LIMIT:int = 10

    query = db.query(Tasks)
    if last_task_at and last_task_id:
        query = query.filter(
            (Tasks.created_at < last_task_at) |
            (Tasks.created_at == last_task_at)
        )
   
    query = query.order_by(desc(Tasks.created_at),desc(Tasks.id))
    tasks = query.limit(LIMIT+1).all()

    has_more = False
    next_task_id = None
    next_task_created_at = None
    for item in tasks:
        print(item.created_at)

    if(len(tasks)>LIMIT):
        # Then there are more item in database
        has_more=True
        # The tasks are already sorted by created item,so taking the last item.
        next_task_id = tasks[-1].id
        next_task_created_at = tasks[-1].created_at
        tasks = tasks[:LIMIT] # removing the last one

    return PaginatedTasksResponse(
    tasks=tasks,
    next_task_id=next_task_id,
    next_task_created_at=next_task_created_at,
    has_more=has_more
)
 


@router.post("/create")
async def create_tasks(task:CreateTask, db:Session= Depends(get_db),user: AuthenticatedUser = Depends(validate_current_user)):
    try:
        new_task:Tasks = Tasks(title=task.title, description= task.description,status=task.status,created_at = datetime.now(timezone.utc) )    
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except Exception as e:  
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong at our end.") 
    return new_task



@router.put("/update")
async def update_tasks(task:UpdateTask, db:Session= Depends(get_db),user: AuthenticatedUser = Depends(validate_current_user)):   
    
    try:
        update_task =  db.query(Tasks).filter(Tasks.id == task.id).first()    

        if update_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="task with provided id not found")
                                
        update_task.title = task.title
        update_task.status = task.status
        update_task.updated_at = datetime.now(timezone.utc)
        db.commit()
    except HTTPException:
        raise                  
    except Exception as e: 
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong at our end.") 
        
    return "Task Updated"



@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id:UUID,db:Session=Depends(get_db),user: AuthenticatedUser = Depends(validate_current_user)):
      
    try:
        delete_task =  db.query(Tasks).filter(Tasks.id == id).first()

        if delete_task is None:           
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="task with provided id not found") 
         
        db.delete(delete_task)
        db.commit()
    except HTTPException:
        raise    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong at our end.")   

     


