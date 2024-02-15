from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    fees = db.Column(db.Integer)

    def __repr__(self):
        return f"Student(student_id='{self.student_id}', student_name='{self.student_name}', fees={self.fees})"

class GetStudent(Resource):
    def get(self):
        students = Student.query.all()
        stu_list = []

        for i in students:
            stu_data = {'Id': i.student_id, 'Name': i.student_name, 'Fees' : i.fees}
            stu_list.append(stu_data)
    
        return {'Students' : stu_list}, 200

class AddStudent(Resource):
    def post(self):
        if request.is_json:
            new_student = Student(student_id=request.json['student_id'], student_name=request.json['student_name'], fees=request.json['fees'])
        db.session.add(new_student)
        db.session.commit()
        return make_response(jsonify({'message': 'Student added successfully'}), 201)

class UpdateStudentFees(Resource):
    def put(self, id):
        if request.is_json:
            stu = Student.query.get(id)
            if stu is None:
                return {'Error': 'Not Found'}, 404
            else:
                stu.fees = request.json['fees']
                db.session.commit()
                return 'Updated', 200
        else:
            return {"Error": 'Requested must be JSON'}, 400

class DeleteStudent(Resource):
    def delete(self,id):
        stu = Student.query.get(id)
        if stu is None:
            return {'error': 'not found'}, 404
        db.session.delete(stu)
        db.session.commit()
        return f'{id} is deleted from table', 200      

api.add_resource(GetStudent, '/')
api.add_resource(AddStudent, '/add')
api.add_resource(UpdateStudentFees, '/fee-update/<int:id>')
api.add_resource(DeleteStudent, '/delete/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)

