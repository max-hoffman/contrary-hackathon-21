# 1. Library imports
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import topshot_model

templates = Jinja2Templates(directory="web/templates")

# 2. Create the app object
app = FastAPI()
static_dir = "web/static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/', response_class=HTMLResponse)
async def read_url(request: Request, url: str = Form(...)):
    moment_id = url.split("/")[-1]
    values = topshot_model.evaluate(moment_id)
    current_price = values[2]
    buy = False
    if current_price < value[0]: buy = True
    return templates.TemplateResponse("result.html", {"request": request, "url": url, "value": values[0], "current_value": values[2], "img": values[1], "status": buy})
    #return values

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'message': f'Hello, {name}'}

@app.get("/predict/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    print(id)
    val = topshot_model.evaluate(id)
    return templates.TemplateResponse("prediction.html", {"request": request, "value": val})

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
