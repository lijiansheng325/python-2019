#! /usr/bin/python
# Filename: inherit.py
class SchoolMember:
	''' Represents any schoolmember. '''
	def __init__(self , name, age,stature):
		self.name = name
		self.age = age
		self.stature = stature
		
		print '(Initialized SchoolMember: % s)' % self.name
	def tell(self):
		''' Tell my details. '''
		print ' Name: "%s" Age: "%s" stature:"%s" \n' % (self.name, self.age,self.stature),
e = SchoolMember("Chen",41,178)
e.tell()
class Teacher(SchoolMember):
	''' Represents a teacher. '''
	def __init__(self , name, age, stature,salary):
		SchoolMember.__init__(self , name, age,stature)
		self.salary = salary
		print ' (Initialized Teacher: %s)' %self.name
	def tell(self):
		SchoolMember.tell(self)
		print ' Salary: "%d"' %self.salary
class Student (SchoolMember):
	''' Represents a student. '''
	def __init__(self , name, age,stature, marks):
		SchoolMember.__init__(self , name, age,stature)
		self.marks = marks
		print ' (Initialized Student : %s)' % self.name
	def tell (self):
		SchoolMember.tell(self)
		print ' Marks: "% d"' % self.marks
		


t = [Teacher(' Mrs.Shrividya', 40,167,20000),Teacher(' Mr.Shrividya', 49,180,3000),Teacher(' Mrs.x', 40,177,50000)]
s = Student (' Swaroop' , 22, 150,75)
print # prints a blank line
for x in t:
	x.tell()

s.tell() # works for both Teachers and Students