from urllib import response
from sqlalchemy import delete
from models import People
from models import Cars
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Person(Resource):
#Função para buscar o registro de pessoa via CPF:
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

#Função para atualizar o registro de pessoa via CPF:
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
        people.save()
        
        response = {
                'name':people.name,
                'cpf':people.cpf,
                'age':people.age,
                'phone':people.phone,
                'cars_quantity':people.cars_quantity
            }
        
        return response

#Função para deletar o registro de pessoa via CPF:
    def delete(self, cpf):
        people = People.query.filter_by(cpf=cpf).first()
        message = 'Cadastro de CPF: {} excluido com sucesso'.format(people.cpf)
        people.delete()
        return {
            'status':'sucess',
            'message':message
        }


class FindAllPeople(Resource):

#Função para buscar todos os registros de pessoas:
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

#Função para registrar pessoa:
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



class Car(Resource):

#Função para buscar o registro de veículo via placa:
    def get(self, license_plate):
        car = Cars.query.filter_by(license_plate = license_plate).first()
        try:
            response = {
                'license_plate': car.license_plate,
                'color_car': car.color_car,
                'model_car': car.model_car,
                'people_id': car.people_id 
            } 
        except AttributeError:
                response = {
                'status':'error',
                'mensagem': 'Veículo não encontrado!' 
                }
        return response
        
#Função para atualizar o registro de veículo via placa:
    def put(self, license_plate):
        car = Cars.query.filter_by(license_plate=license_plate).first()
        data = request.json
        if 'license_plate' in data:
            car.license_plate=data['license_plate']
        if 'color_car' in data:
            car.color_car=data['color_car']
        if 'model_car' in data:
            car.model_car=data['model_car']
        if 'people_id' in data:
            car.people_id=data['people_id']
        car.save()

        response={
            'license_plate': car.license_plate,
            'color_car': car.color_car,
            'model_car': car.model_car,
            'people_id': car.people_id
        }
        return response

#Função para deletar o registro de veículo via placa:
    def delete(self, license_plate):
        car = Cars.query.filter_by(license_plate=license_plate).firts()
        mensagem = 'Cadastro de véiculo de placa {}, excluido com sucesso'.format(car.license_plate)
        car.delete()
        return {'status' : 'sucesso', 'mensagem': mensagem}

class FindAllCars(Resource):

#Função para buscar todos os registros de veículos:
    def get(self):
        car = Cars.query.all()
        response = [{
            'license_plate': i.license_plate, 'color_car': i.color_car, 'model_car': i.model_car,
            'people_id': i.people_id
            }for i in car]
        return response

class CreateRegistrationCar(Resource):

#Função para registrar veículo:
    def post(self):
        data = request.json
        car = Cars(
            license_plate=data['license_plate'],
            color_car=data['color_car'],
            model_car=data['model_car'],
            people_id=data['people_id']
        )
        car.save()
        response = {
            'license_plate': car.license_plate,
            'color_car': car.color_car,
            'model_car': car.model_car,
            'people_id': car.people_id
        }
        return response


#Rotas
api.add_resource(Person, '/people/<int:cpf>')
api.add_resource(FindAllPeople, '/people')
api.add_resource(CreatePeople, '/people')
api.add_resource(Car, '/cars/<string:license_plate>')
api.add_resource(FindAllCars, '/cars')
api.add_resource(CreateRegistrationCar, '/cars')

if __name__ == '__main__':
    app.run(debug=True)
