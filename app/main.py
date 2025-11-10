from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Booking System API",
    description="Sistema profissional de reservas - DeveloperBruNao",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Booking System API 🏨", "developer": "DeveloperBruNao"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "booking-system"}