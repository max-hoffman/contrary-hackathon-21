# 1. Library imports
import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

import topshot_model

templates = Jinja2Templates(directory="templates")

# 2. Create the app object
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, stranger'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'message': f'Hello, {name}'}

@app.get("/predict/{url}", response_class=HTMLResponse)
async def read_item(request: Request, url: str):
    val = topshot_model.evaluate(request)
    return templates.TemplateResponse("prediction.html", {"request": request, "value": val})

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
