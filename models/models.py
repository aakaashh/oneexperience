from google.appengine.ext import ndb
import logging

class School(ndb.Model):
	school_name=ndb.StringProperty(indexed=False,required=True)
	school_address=ndb.StringProperty(indexed=False)
	school_pincode=ndb.IntegerProperty(indexed=False)
	school_code=ndb.StringProperty(required=True)

class Classroom(ndb.Model):
	class_name=ndb.StringProperty(required=True)
	class_section=ndb.StringProperty()

	def get_attendance_dates(self):
		query_set = Attendance.query(projection=[Attendance.attendance_date], distinct=True, ancestor=self.key)
		attendance_dates = [i.attendance_date for i in query_set]
		return attendance_dates

	# def get_subjects(self):
	# 	all_subjects_objects=Subject.query(ancestor=self.key)
	# 	all_subjects=[i.subject_name for i in all_subjects_objects]


class Test_Information(ndb.Model):
	test_date=ndb.DateProperty(required=True)
	test_max_marks=ndb.IntegerProperty(indexed=False,required=True)
	test_name=ndb.StringProperty(indexed=True)

class Subject(ndb.Model):
	subject_name=ndb.StringProperty(required=True)

class Class_Working(ndb.Model):
	attendance_date=ndb.DateProperty(required=True)
	working_status=ndb.StringProperty(required=True, choices=["Working","Not Working"])

class Student(ndb.Model):
	student_name=ndb.StringProperty(required=True)
	student_gender=ndb.StringProperty(indexed=False, choices=["Male","Female"], required=True)
	student_roll_number=ndb.IntegerProperty(required=True)
	student_date_of_birth=ndb.DateProperty(indexed=False)
#	student_ID=ndb.StringProperty(required=True)
	def get_caretakers(self):
		caretakers=Caretaker.query(ancestor=self.key).fetch()
		return caretakers

	def get_attendance_status(self,class_working_object):
		class_working_key=class_working_object.key
		if class_working_object.working_status == "Not Working":
			return "Holiday"
		else:
			student_attendance=Student_Attendance.query(Student_Attendance.attendance_information==class_working_key,ancestor=self.key).get()
			if student_attendance:
				return "Absent"
			else:
				return "Present"

	def get_student_marks(self,test_key):
		marks=Student_Test.query(Student_Test.test_information==test_key,ancestor=self.key).get().test_marks
		return marks



class Student_Test(ndb.Model):
	test_marks=ndb.IntegerProperty(indexed=False,required=True)
	test_information=ndb.KeyProperty(kind='Test_Information',required=True)

class Student_Attendance(ndb.Model):
	attendance_information=ndb.KeyProperty(kind='Class_Working', required=True)

class Caretaker(ndb.Model):
	caretaker_title=ndb.StringProperty(indexed=False,required=True,choices=["Mr","Mrs","Ms","Miss"])
	caretaker_name=ndb.StringProperty(indexed=False,required=True)
	caretaker_relatonship=ndb.StringProperty(indexed=False,required=True,choices=["Father","Mother","Guardian"])
	caretaker_email_id=ndb.StringProperty(indexed=False)
	caretaker_phone_no=ndb.IntegerProperty(indexed=False)
