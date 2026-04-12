from fastapi import FastAPI, Query, status
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="我的第一个 FastAPI 应用")


# ---------- 数据模型 ----------
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


# ---------- 模拟数据存储 ----------
tasks_db = []


# ---------- 路由定义 ----------
@app.get("/")
async def root():
    return {"message": "欢迎使用 FastAPI 任务管理 API"}


@app.get("/tasks", response_model=List[Task])
async def get_tasks(completed: Optional[bool] = None):
    """获取任务列表，可通过 ?completed=true 过滤"""
    if completed is None:
        return tasks_db
    return [t for t in tasks_db if t["completed"] == completed]


@app.post("/tasks")
async def create_task(task: Task):
    """创建新任务"""
    task_dict = task.model_dump()
    task_dict["id"] = len(tasks_db) + 1
    tasks_db.append(task_dict)
    return task_dict


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    """获取单个任务"""
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    return {"error": "Task not found"}


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    """更新任务"""
    for t in tasks_db:
        if t["id"] == task_id:
            t.update(task.model_dump())
            return t
    return {"error": "Task not found"}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """删除任务"""
    global tasks_db
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    return {"message": f"Task {task_id} deleted"}