import uvicorn
from module_22.api.apidevelopment import app

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)
