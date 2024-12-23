import uvicorn

def Run():
    """
    Run the FastAPI server.
    """
    uvicorn.run(
        "app.app:create_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True  # Use the factory option to call the create_app function
    )

if __name__ == "__main__":
    Run()
