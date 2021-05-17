from flask_restful import Api

from api.plant import PlantAPI,PlantDelAPI

def create_route(api: Api):
    api.add_resource(PlantAPI, '/plant')
    api.add_resource(PlantDelAPI, '/plant/delete/<name>')
