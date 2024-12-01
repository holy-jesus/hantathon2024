from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from checker import Checker
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

checker = Checker()
app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

class SiteURL(BaseModel):
    url: str = None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/check/", response_class=JSONResponse)
async def read_site(site_url: SiteURL):
    print(site_url)
    # result = await checker.run_tests(site_url.url)
    # return {"result": result}

    # Здесь будет логика для анализа URL.
    
    # Условно, что то вроде:
    response_data = {
        "rating": 85,
        "issues": [
            "Недостаточный контраст текста",
            "Отсутствие альтернативного текста для изображений",
            "Нарушенная структура заголовков",
        ],
        "reportLink": site_url.url
    }

    # response_data = {""}
    
    return response_data


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return {"detail": exc.detail, "status_code": exc.status_code}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
