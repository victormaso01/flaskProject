from flasgger import Swagger, swag_from
from flask import jsonify, request
from src.config import db
from src.models.students import Student as Student
from src.config.db import session as ses


def swagger(app):
    return Swagger(app)
def init_api_routes(app):
    @app.route('/api/students', methods=['GET'])
    @swag_from({
        'summary': 'Obtiene la lista de estudiantes.',
        'responses': {
            200: {
                'description': 'Lista de estudiantes.',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'age': {'type': 'integer'},
                            'spec': {'type': 'string'}
                        }
                    }
                }
            }
        }
    })
    def get_students():
        students = ses.query(Student).all()
        students_list = [{"id": student.id, "name": student.name, "spec": student.spec, "age": student.age} for student
                         in students]
        return jsonify(students_list)

    @app.route('/api/student/<int:student_id>', methods=['GET'])
    @swag_from({
        'summary': 'Obtiene un estudiante por ID.',
        'parameters': [
            {
                'in': 'path',
                'name': 'student_id',
                'type': 'integer',
                'required': True,
                'description': 'ID del estudiante a obtener.'
            }
        ],
        'responses': {
            200: {
                'description': 'Estudiante encontrado.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'age': {'type': 'integer'},
                        'spec': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Estudiante no encontrado.'
            }
        }
    })
    def get_student_by_id(student_id):
        std = ses.query(Student).filter_by(id=student_id).first()
        if std is None:
            return jsonify({"error": "Not Found"}), 404
        else:
            return jsonify({'id': std.id, 'name': std.name, 'age': std.age, 'spec': std.spec})

    @app.route('/api/student', methods=['POST'])
    @swag_from({
        'summary': 'Agrega un nuevo estudiante.',
        'description': 'Agrega un nuevo estudiante con la información proporcionada.',
        'parameters': [
            {
                'in': 'body',
                'name': 'student_data',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'age': {'type': 'integer'},
                        'spec': {'type': 'string'}
                    },
                    'required': ['name', 'age', 'spec']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Estudiante agregado exitosamente.'
            }
        }
    })
    def post_student():
        student_data = request.get_json()
        std = Student(**student_data)
        ses.add(std)
        ses.commit()

        return jsonify({'name': std.name, 'age': std.age, 'spec': std.spec}), 201

    # Actualizar un estudiante por ID
    @app.route('/api/student/<int:student_id>', methods=['PUT'])
    @swag_from({
        'summary': 'Actualiza un estudiante por ID.',
        'parameters': [
            {
                'in': 'path',
                'name': 'student_id',
                'type': 'integer',
                'required': True,
                'description': 'ID del estudiante a actualizar.'
            },
            {
                'in': 'body',
                'name': 'student_data',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'age': {'type': 'integer'},
                        'spec': {'type': 'string'}
                    },
                    'required': ['name', 'age', 'spec']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Estudiante actualizado exitosamente.'
            },
            404: {
                'description': 'Estudiante no encontrado.'
            }
        }
    })
    def put_student(student_id):

        student_json = request.get_json()
        student_bd = ses.query(Student).filter_by(id=student_id).first()

        if student_bd is None:
            return jsonify({"error": "Not Found"}), 404
        else:
            student_bd.name = student_json['name']
            student_bd.age = student_json['age']
            student_bd.spec = student_json['spec']
            ses.commit()

            return jsonify({'name': student_bd.name, 'age': student_bd.age, 'spec': student_bd.spec}), 200

    @app.route('/api/student/<int:student_id>', methods=['DELETE'])
    @swag_from({
        'summary': 'Elimina un estudiante por ID.',
        'parameters': [
            {
                'in': 'path',
                'name': 'student_id',
                'type': 'integer',
                'required': True,
                'description': 'ID del estudiante a eliminar.'
            }
        ],
        'responses': {
            204: {
                'description': 'Estudiante eliminado exitosamente.'
            },
            404: {
                'description': 'Estudiante no encontrado.'
            }
        }
    })
    def delete_student(student_id):
        if student_id is None:
            return "Not Found", 404
        else:
            try:
                ses.query(Student).filter_by(id=student_id).delete()
                ses.commit()
                return '', 204
            except Exception as e:
                return jsonify(e)
