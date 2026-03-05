from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import database
import os

app = FastAPI()

# Initialize database
database.init_db()

# Fix template path for deployment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Login Model
class Login(BaseModel):
    username: str
    password: str

# Camera Model
class Camera(BaseModel):
    place_name: str
    camera_name: str
    camera_mode: str


# Login Page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Dashboard Page
@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Login API
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


# Get Cameras
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


# Add Camera
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

    return JSONResponse(content={"message": "Camera added successfully"})
