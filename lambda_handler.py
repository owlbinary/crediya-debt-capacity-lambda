from mangum import Mangum
from app.adapters.api import app

handler = Mangum(app)
