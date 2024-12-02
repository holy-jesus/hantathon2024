import os
from pathlib import Path
from uuid import uuid4
import tempfile

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from checker import Checker


checker = Checker()
app = FastAPI()

path = Path(os.getenv("front"))


app.mount("/assets", StaticFiles(directory=path.parent / "assets"), name="assets")
files = []


class SiteURL(BaseModel):
    url: str = None


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return path.read_text()


@app.post("/check/", response_class=JSONResponse)
async def read_site(request: Request):
    url = (await request.body()).decode()
    results, file = await checker.run_tests(url)

    response = {"total": 0, "defiances": [], "recommendations": []}
    for result in results:
        response["total"] += result.percentage
        response[result.test.__name__] = result.percentage
        if result.percentage != 100.0:
            response["defiances"].append(result.test.DEFIANCE)
            response["recommendations"].append(result.test.RECOMMENDATION)
    response["total"] = response["total"] / len(results)
    response["file"] = str(uuid4()) + ".docx"
    with open(Path(tempfile.gettempdir()) / response['file'], "wb") as f:
        f.write(file.getvalue())
    files.append(response["file"])
    return response


@app.get("/files/{file:str}")
async def get_file(file: str):
    if file not in files:
        return
    return FileResponse(f"/tmp/{file}")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return {"detail": exc.detail, "status_code": exc.status_code}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
