from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI()
class HelloWorld():
  def read_hello(self):
    return {"data": "Hello World"}
router = APIRouter()
router.add_api_route(
  '/api/v2', 
  endpoint = HelloWorld().read_hello, methods=["GET"])
app.include_router(router)

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
  # uvicorn.run("Orchestrator:app", host="127.0.0.1", port=9400, reload=True, root_path="/api/v2")
  # uvicorn.run("UserStatsRedis:app", host="127.0.0.1", port=9000, reload=True)
  # uvicorn.run("WordCheck:app", host="127.0.0.1", port=9100, reload=True)
  # uvicorn.run("WordValidation:app", host="127.0.0.1", port=9200, reload=True)
  # uvicorn.run("Play:app", host="127.0.0.1", port=9300, reload=True)