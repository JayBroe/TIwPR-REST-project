from flask import Flask, json, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import uuid
import datetime

from sqlalchemy import false

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.before_first_request
def create_table():
    db.create_all()

class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	name = db.Column(db.String(20), nullable=False)
	surname = db.Column(db.String(20), nullable=False)
	indexx = db.Column(db.String(10), nullable=False)
	email = db.Column(db.String(28), nullable=False)
	is_studying = db.Column(db.Boolean, default=False)
	proposal=db.relationship('Proposal', backref='owner', lazy='dynamic',foreign_keys = 'Proposal.student_id')
	annoucement=db.relationship('Announcement', backref='ogl1', lazy='dynamic', foreign_keys = 'Announcement.student_id')

	def __repr__(self):
		return f'Student <{self.indexx}>'

class Proposal(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	nr = db.Column(db.String(6), nullable=False)
	name = db.Column(db.String(20), nullable=False)
	student_id=db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
	decision=db.relationship('Decision', backref='owner1', lazy='dynamic')
	
	def __repr__(self):
		return f'Proposal: <{self.name}>'

class Decision(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	acceptance = db.Column(db.Boolean, default=False)
	nr_decision = db.Column(db.String(6), nullable=False)
	proposal_id = db.Column(db.Integer, db.ForeignKey('proposal.id'), nullable=False)

	def __repr__(self):
		return f'Decyzja: <{self.acceptance}>'

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(20), nullable=False) 
    surname = db.Column(db.String(20), nullable=False)
    teacher_id = db.Column(db.String(6), nullable=False)
    email = db.Column(db.String(28), nullable=False)
    degree = db.Column(db.String(20), nullable=False)
    subject=db.relationship('Subject', backref='owner2', lazy='dynamic', foreign_keys = 'Subject.teacher_id')
    announcement=db.relationship('Announcement', backref='ogl2', lazy='dynamic', foreign_keys = 'Announcement.teacher_id')
    def __repr__(self):
        return f'Prowadzacy: <{self.email}>'

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), nullable=False)
    p_id = db.Column(db.String, nullable=False)
    form = db.Column(db.String(20),nullable=False)
    teacher_id=db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)

    def __repr__(self):
        return f'Przedmiot: <{self.name}>'

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    content = db.Column(db.String(30), nullable=False) 
    student_id=db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teacher_id=db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    data = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    
    def __repr__(self):
        return f'Ogloszenie: <{self.content}>'

@app.route('/')
def home():
	return {
		'message': 'Witamy w dziekanacie!'
	}


@app.route('/students/')
def get_students():
	return jsonify([
		{
			'name': student.name, 
            'surname': student.surname, 'indexx': student.indexx,
            'email': student.email, 'is study': student.is_studying
			} for student in Student.query.all()
	])
		
@app.route('/students/<id>/')
def get_student(id):
	print(id)
	student = Student.query.filter_by(indexx=id).first_or_404()
	return {
		    'name': student.name, 
            'surname': student.surname, 'indexx': student.indexx,
            'email': student.email, 'is stud': student.is_studying
		}

@app.route('/students/', methods=['POST'])
def create_student():	
	student = Student(
			name="",
            surname="",
			is_studying=False,
			email="", 
			indexx=str(random.randint(100000, 199999)),
		)
	db.session.add(student)
	db.session.commit()
	return {
			
			'name': student.name, 
            'surname': student.surname,
		    'email': student.email,  
		    'is stud': student.is_studying,
			'indexx': student.indexx,
	}, 201

@app.route('/students/<id>/', methods=['PUT'])
def update_student(id):
	data = request.get_json()
	student = Student.query.filter_by(indexx=id).first_or_404()
	student.name=data['name']
	student.surname=data['surname']
	if 'email' in data:
		return jsonify({
		'error': 'Bad Request',
		'message': 'Email generowany jest automatycznie'
		}), 400	
	student.email=data['name']+'.'+data['surname']+'@student.put.poznan.pl'
	student.is_studying=data['is stud']
	db.session.commit()
	return jsonify({
		'name': student.name, 
		'surname': student.surname,
        'indeks':student.indexx, 
		'is stud': student.is_studying,
		'email': student.email
		})

@app.route('/students/<id>/', methods=['PATCH'])
def patch_student(id):
	data = request.get_json()
	student = Student.query.filter_by(indexx=id).first_or_404()
	if 'name' in data:
		student.name=data['name']
	if 'surname' in data:
		student.surname=data['surname']
	if 'email' in data:
		return jsonify({
		'error': 'Bad Request',
		'message': 'Email generowany jest automatycznie'
		}), 400	
	if 'is stud' in data:
		student.is_studying=data['is stud']	
	if 'indexx' in data:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Nr indeksu nie podlega zmianie'
		}), 400	
	db.session.commit()
	return jsonify({
		'name': student.name, 
		'surname': student.surname,
        'indeks':student.indexx, 
		'is stud': student.is_studying,
		'email': student.email
		})

@app.route('/students/<id>/', methods=['DELETE'])
def delete_student(id):
	data = request.get_json()
	student = Student.query.filter_by(indexx=id).first_or_404()
	if not student:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Student nie istnieje'
		}), 400
	db.session.delete(student)
	db.session.commit()
	return {
		'success': 'Student o nr indeksie '+ student.indexx +' zostal usuniety pomyslnie.'
	}

@app.route('/proporsals/')
def get_proposals():
	return jsonify([
		{
			'nr':proposal.nr,
			'nazwa': proposal.name, 
			'owner': {
				'indexx': proposal.owner.indexx,
				'name': proposal.owner.name,
				'surname': proposal.owner.surname,
				'email':proposal.owner.email,
		} 
			} for proposal in Proposal.query.all()
	])

@app.route('/proporsals/<id>/')
def get_proposal(id):
	print(id)
	proposal = Proposal.query.filter_by(nr=id).first_or_404()
	return {
			'nr':proposal.nr,
			'name': proposal.name, 
			'owner': {
				'indexx': proposal.owner.indexx,
				'name': proposal.owner.name,
				'surname': proposal.owner.surname,
				'email':proposal.owner.email
		} 
	}

@app.route('/proporsals/', methods=['POST'])
def create_proposal():
	data = request.get_json()
	if not 'indexx' in data:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Index of creator not given'
		}), 400
	student=Student.query.filter_by(indexx=data['indexx']).first()
	if not student:
		return {
			'error': 'Bad request',
			'message': 'Invalid indexx, no student with that indexx'
		}
	proposal = Proposal(
		nr = str(random.randint(0, 100)),
		name="",
		student_id=student.id,
	)
	db.session.add(proposal)
	db.session.commit()
	return {
		'nr': proposal.nr, 
		'name': proposal.name,
		'owner': {
			'indexx': proposal.owner.indexx,
			'name': proposal.owner.name,
			'surname': proposal.owner.surname 
		} 
	}, 201

@app.route('/proporsals/<id>/', methods=['PUT'])
def update_proposal(id):
	data = request.get_json()
	proposal = Proposal.query.filter_by(nr=id).first_or_404()
	proposal.name=data['name']
	db.session.commit()
	return {
		'nr': proposal.nr, 
		'name': proposal.name,
		'owner': {
			'indexx': proposal.owner.indexx,
			'name': proposal.owner.name,
			'surname': proposal.owner.surname 
		} 
	}, 201


@app.route('/proporsals/<id>/', methods=['DELETE'])
def delete_proposal(id):
	proposal = Proposal.query.filter_by(indexx=id).first_or_404()
	db.session.delete(proposal)
	db.session.commit()
	return {
		'success': 'Wniosek o  '+ proposal.nr +' zostal cofniety pomyslnie.'
	}


@app.route('/decisions/')
def get_decisions():
	return jsonify([
		{
			'acceptance': decision.acceptance, 
			'owner': {
				'nr': decision.owner1.nr,
				'name': decision.owner1.name,
		} 
			} for decision in Decision.query.all()
	])

@app.route('/decisions/<id>/')
def get_decision(id):
	decision = Decision.query.filter_by(nr=id).first_or_404()
	return {
		    'acceptance': decision.acceptance, 
            'owner':{
				'nr': decision.owner1.nr,
				'name': decision.owner1.name,
			}
		}

@app.route('/decisions/', methods=['POST'])
def create_decision():
	data = request.get_json()
	if not 'nr' in data:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Index nie został podany'
		}), 400
	proposal=Proposal.query.filter_by(nr=data['nr']).first()
	if not proposal:
		return {
			'error': 'Bad request',
			'message': 'Zły nr, nie ma wniosku o takim numerze'
		}, 400
	decision = Decision(
		acceptance=False,
		nr_decision=proposal.nr+'-',
		proposal_id=proposal.id,
	)
	db.session.add(decision)
	db.session.commit()
	return {
		'acceptance':decision.acceptance,
		'nr decision':decision.nr_decision,
		'owner': {
			'name': decision.owner1.name,
			'nr': decision.owner1.nr,
		} 
	}, 201

@app.route('/decisions/<id>/', methods=['PUT'])
def update_decision(id):
	data = request.get_json()
	decision = Decision.query.filter_by(nr_decision=id).first_or_404()
	decision.acceptance=data['acceptance']
	db.session.commit()
	return jsonify({
		'acceptance': decision.acceptance,
		'Identyfikator decision':decision.nr_decision, 
		'owner': {
			'name': decision.owner1.name,
			'nr': decision.owner1.nr,
		} 
		}), 201

@app.route('/decisions/<id>/', methods=['DELETE'])
def delete_decision(id):
	decision = Decision.query.filter_by(nr_decision=id).first_or_404()
	db.session.delete(decision)
	db.session.commit()
	return {
		'success': 'Decyzja o nr '+ decision.nr_decision + ' zostala pomyslnie cofnieta'
	}

@app.route('/teachers/')
def get_teachers():
	return jsonify([
		{
			'name': teacher.name, 
            'surname': teacher.surname, 
            'email': teacher.email,
			'id':teacher.teacher_id,
			} for teacher in Teacher.query.all()
	])
		
@app.route('/teachers/<id>/')
def get_teacher(id):
	print(id)
	teacher = Teacher.query.filter_by(teacher_id=id).first_or_404()
	return {
		    'name': teacher.name, 
            'surname': teacher.surname,
            'email': teacher.email,
			'id':teacher.teacher_id
		}

@app.route('/teachers/', methods=['POST'])
def create_teacher():
	teacher = Teacher(
			degree="",
			name="", 
            surname="", 
			email="",
			teacher_id=str(uuid.uuid4())
		)
	db.session.add(teacher)
	db.session.commit()
	return {
			'name': teacher.name, 
            'surname': teacher.surname,
		    'email': teacher.email,  
		    'id':teacher.teacher_id,
			'degree':teacher.degree
	}, 201



@app.route('/teachers/<id>/', methods=['PUT'])
def update_teacher(id):
	data = request.get_json()
	teacher = Teacher.query.filter_by(teacher_id=id).first_or_404()
	teacher.degree=data['degree']
	if not (data['degree'] =="Profesor" or data['degree'] =="Doktor" or data['degree'] =="Magister"):
		return {
			'error': 'Bad Request',
			'message': 'Należy wybrać spośród Profesora, doktora lub magistra!'
		}
	teacher.name=data['name']
	teacher.surname=data['surname']
	teacher.email=data['name']+'.'+data['surname']+'@put.poznan.pl'
	db.session.commit()
	return jsonify({
		'name': teacher.name, 
		'surname': teacher.surname,
		'email': teacher.email,
		'degree':teacher.degree,
		'id':teacher.teacher_id,
		})

@app.route('/teachers/<id>/', methods=['PATCH'])
def patch_teacher(id):
	data = request.get_json()
	teacher = Teacher.query.filter_by(teacher_id=id).first_or_404()

	if 'name' in data:
		teacher.name=data['name']
	if 'surname' in data:
		teacher.surname=data['surname']
	if 'degree' in data:
		teacher.surname=data['degree']
	if not (data['degree'] =="Profesor" or data['degree'] =="Doktor" or data['degree'] =="Magister"):
		return {
			'error': 'Bad Request',
			'message': 'Należy wybrać spośród Profesora, doktora lub magistra!'
		}
	
	db.session.commit()
	return jsonify({
		'name': teacher.name, 
		'surname': teacher.surname,
		'email': teacher.email,
		'degree':teacher.degree
		})

@app.route('/teachers/<id>/', methods=['DELETE'])
def delete_teacher(id):
	teacher = Teacher.query.filter_by(email=id).first_or_404()
	db.session.delete(teacher)
	db.session.commit()
	return {
		'success': 'Prowadzacy o  '+ teacher.name +' '+ teacher.surname +' zostal usuniety pomyslnie.'
	}

@app.route('/subjects/')
def get_subjects():
	return jsonify([
		{
			'name': subject.name, 
			'identyfikator':subject.p_id,
			'owner':{
				'name': subject.owner2.name,
				'surname': subject.owner2.surname,
				'email': subject.owner2.email
			}
			} for subject in Subject.query.all()
	])
		
@app.route('/subjects/<id>/')
def get_subject(id):
	print(id)
	subject = Subject.query.filter_by(name=id).first_or_404()
	return {
		    'name': subject.name, 
			'identyfikator':subject.p_id,
			'owner':{
				'name': subject.owner2.name,
				'surname': subject.owner2.surname,
				'email': subject.owner2.email
			}
		}


@app.route('/subjects/', methods=['POST'])
def create_subject():
	data = request.get_json()	
	teacher=Teacher.query.filter_by(teacher_id=data['teacher_id']).first()
	if not teacher:
		return {
			'error': 'Bad request',
			'message': 'Zły id, nie ma prowadzącego o takim id'
		}
	subject = Subject(
		name="", 
		form="",
		p_id=str(uuid.uuid4()),
		teacher_id=teacher.id,
	)
	db.session.add(subject)
	db.session.commit()
	return {
		'name': subject.name,
		'forma': subject.form,
		'identyfikator':subject.p_id,
		'owner': {
			'name': subject.owner2.name,
			'surname': subject.owner2.surname,
			'email': subject.owner2.email
		} 
	}, 201

@app.route('/subjects/<id>/', methods=['PUT'])
def update_subject(id):
	data = request.get_json()
	subject = Subject.query.filter_by(p_id=id).first_or_404()
	subject.name=data['name']
	subject.form=data['form']
	if not (data['form'] =="Wyklad" or data['form'] =="Cwiczenia" or data['form'] =="Laboratorium" or data['form'] =="Seminarium"):
		return {
			'error': 'Bad Request',
			'message': 'Należy wybrać spośród Wykład, Cwiczenia, Seminarium lub Laboratoria !'
		}
	db.session.commit()
	return jsonify({
		'name': subject.name, 
		'Forma': subject.form,
		"p_id": subject.p_id,
		'owner':{
			'Imie wykladowcy': subject.owner2.name,
			'Nazwisko wykladowcy':subject.owner2.surname
		}
		})

@app.route('/subjects/<id>/', methods=['PATCH'])
def patch_subject(id):
	data = request.get_json()
	subject = Subject.query.filter_by(p_id=id).first_or_404()
	if 'name' in data:
		subject.name=data['name']
	if 'form' in data:	
		subject.form=data['form']	
	db.session.commit()
	return jsonify({
		'name': subject.name, 
		'Forma': subject.form,
		'owner':{
			'name': subject.owner2.name,
			'Nazwisko wykladowcy':subject.owner2.surname
		}
		})

@app.route('/subjects/<id>/', methods=['DELETE'])
def delete_subject(id):
	subject = Subject.query.filter_by(p_id=id).first_or_404()
	db.session.delete(subject)
	db.session.commit()
	return {
		'success': 'Przedmiot '+ subject.name +' zostal usuniety pomyslnie.'
	}

@app.route('/annoucements/')
def get_annoucements():
	return jsonify([
		{
			'tresc': annoucement.content,
		    'data': annoucement.data,
			'Dane adresatow': {
			'imie studenta':annoucement.ogl1.name,
			'nazwisko studenta':annoucement.ogl1.surname,
		},
			'Dane adresata':{
			'imie prowadzacego': annoucement.ogl2.name,
			'nazwisko prowadzacego': annoucement.ogl2.surname,
			},
			} for annoucement in Announcement.query.all()
	])
		
@app.route('/annoucements/<id>/')
def get_annoucement(id):
	print(id)
	annoucement = Announcement.query.filter_by(data=id).first_or_404()
	return {
			'tresc': annoucement.content,
		    'data': annoucement.data,
			'Dane adresatow': {
			'imie studenta':annoucement.ogl1.name,
			'nazwisko studenta':annoucement.ogl1.surname,
		},
			'Dane adresata':{
			'imie prowadzacego': annoucement.ogl2.name,
			'nazwisko prowadzacego': annoucement.ogl2.surname,
			},
	}


@app.route('/annoucements/', methods=['POST'])
def create_annoucement():
	data = request.get_json()
	student=Student.query.filter_by(indexx=data['indexx']).first()
	teacher=Teacher.query.filter_by(teacher_id=data['teacher_id']).first()
	if not student or not teacher:
		return {
			'error': 'Bad request',
			'message': 'Podane zostały złe dane identyfikujące'
		}
	annoucement = Announcement( 
		content="", 
		data=datetime.datetime.now(),
		teacher_id=teacher.id,
		student_id=student.id,
	)
	db.session.add(annoucement)
	db.session.commit()
	return {
		    'data': annoucement.data,
			'Dane adresatow': {
			'imie studenta':annoucement.ogl1.name,
			'nazwisko studenta':annoucement.ogl1.surname,
		},
			'Dane adresata':{
			'imie prowadzacego': annoucement.ogl2.name,
			'nazwisko prowadzacego': annoucement.ogl2.surname,
			},
			}, 201

@app.route('/annoucements/<id>/', methods=['PUT'])
def update_annoucement(id):
	data = request.get_json()
	annoucement = Announcement.query.filter_by(data=id).first_or_404()
	annoucement.content=data['content']
	db.session.commit()
	return jsonify({
			'content': annoucement.content,
		    'data': annoucement.data,
			'Dane adresatow': {
			'imie studenta':annoucement.ogl1.name,
			'nazwisko studenta':annoucement.ogl1.surname,
		},
			'Dane adresata':{
			'imie prowadzacego': annoucement.ogl2.name,
			'nazwisko prowadzacego': annoucement.ogl2.surname,
			},
	})

@app.route('/annoucements/<id>/', methods=['DELETE'])
def delete_annoucement(id):
	annoucement = Announcement.query.filter_by(data=id).first_or_404()
	db.session.delete(annoucement)
	db.session.commit()
	return {
		'success': 'Ogloszenie z dnia '+ annoucement.data +' zostalo wygaszone.'
	}

'''@app.route('/dezaktywujstudentow/', methods=['PATCH'])
def false_the_students():
	data = request.get_json()
	student = Student.query
	if 'name' in data:
		student.name=data['name']
	db.session.commit()
'''
if __name__ == '__main__':
	app.run()	
