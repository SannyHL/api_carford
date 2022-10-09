from urllib import response
from sqlalchemy import delete
from models import People
from models import Cars
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Person(Resource):
    def get(self, cpf):
        people = People.query.filter_by(cpf=cpf).first()
        try:
            response = {
                'name':people.name,
                'cpf':people.cpf,
                'age':people.age,
                'phone':people.phone,
                'cars_quantity':people.cars_quantity
            }
        except AttributeError:
            response = {
                'status':'error',
                'message': 'O CPF informado não foi encontrado!'
            }
        return response

    def put(self, cpf):
        people = People.query.filter_by(cpf=cpf).first()
        data = request.json
        if 'name' in data:
            people.name = data['name']
        if 'age' in data:
            people.age = data['age']
        if 'cpf' in data:
            people.cpf = data['cpf']
        if 'phone' in data:
            people.phone = data['phone']
        if 'email' in data:
            people.email = data['email']
        if 'cars_quantity' in data:
            people.cars_quantity = data['cars_quantity']
        
        response = {
                'name':people.name,
                'cpf':people.cpf,
                'age':people.age,
                'phone':people.phone,
                'cars_quantity':people.cars_quantity
            }
        
        return response

    def delete(self, cpf):
        people = People.query.filter_by(cpf=cpf).first()
        message = 'Cadastro de id {} excluido com sucesso'.format(people.id)
        people.delete()
        return {
            'status':'sucess',
            'message':message
        }

class FindAllPeople(Resource):
    def get(self):
        people = People.query.all()
        response = [{
            'name':i.name,
            'cpf':i.cpf,
            'age':i.age,
            'phone':i.phone,
            'cars_quantity':i.cars_quantity
        } for i in people]
        return response

class CreatePeople(Resource):
    def post(self):
        dados = request.json
        people = People(name = dados['name'], age = dados['age'], cpf = dados['cpf'], phone = dados['phone'], email = dados['email'], cars_quantity = dados['cars_quantity'])
        people.save()
        response = {
            
            'name':people.name,
            'cpf':people.cpf,
            'age':people.age,
            'phone':people.phone,
            'cars_quantity':people.cars_quantity
        }
        return response


api.add_resource(Person, '/people/<int:cpf>')
api.add_resource(FindAllPeople, '/people')
api.add_resource(CreatePeople, '/people')

if __name__ == '__main__':
    app.run(debug=True)
