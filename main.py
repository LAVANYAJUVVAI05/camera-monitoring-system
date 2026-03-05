from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import database

app = FastAPI()

database.init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


class Login(BaseModel):
    username: str
    password: str


class Camera(BaseModel):
    place_name: str
    camera_name: str
    camera_mode: str


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.post("/login")
def login(data: Login):
    db = database.get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data.username, data.password)
    )

    user = cur.fetchone()
    db.close()

    if user:
        return {"success": True}
    return {"success": False}


@app.get("/cameras")
def get_cameras():
    db = database.get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM cameras")
    rows = cur.fetchall()
    db.close()

    cameras = []
    for row in rows:
        cameras.append({
            "place_name": row["place_name"],
            "camera_name": row["camera_name"],
            "camera_mode": row["camera_mode"]
        })

    return cameras


@app.post("/cameras")
def add_camera(camera: Camera):
    db = database.get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO cameras (place_name, camera_name, camera_mode) VALUES (?, ?, ?)",
        (camera.place_name, camera.camera_name, camera.camera_mode)
    )

    db.commit()
    db.close()

    return JSONResponse(content={"message": "Camera added"})