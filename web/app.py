# 1. Library imports
import uvicorn
from fastapi import FastAPI, Request
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
def index():
    return {'message': 'Hello, stranger'}

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
