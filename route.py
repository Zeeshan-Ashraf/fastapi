from fastapi import FastAPI, HTTPException, status
import time


"""
TERMINOLOGY:
1. Path Parameters: api.com/users/{userId}
2. Query Parameters: api.com/products?category=electronics&sort=price
3. Request Parameters (General Term): path parameters, query parameters, form parameters & params in request body
"""

appo = FastAPI()




'''
home page:
GET 127.0.0.1:8000
'''
@appo.get("/")
async def root():   #async so that 2 diff request for "/" can be processed parallely instead of sequentially
    time.sleep(10)
    return {"message": "Root Message async after 10 seconds"}




'''
simple route
GET 127.0.0.1:8000/hello
'''
@appo.get("/hello")
async def hello():
    return {"message": "Hello World"}




'''
simple route with different HTTP status than default 200 OK
GET 127.0.0.1:8000/items
'''
@appo.get("/items")
def items():
    response = HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail={"message": ['a', 'b', 1]},
        headers={"Content-Type": "application/json"}
    )
    return response






data = []
'''
GET with path params with raise exception
GET 127.0.0.1:8000/items/1
'''
data.append("mango")
data.append("apple")

@appo.get("/items/{data_index}")  #name data_index should be same in method params as well
def get_item(data_index: int, dummy_var: bool = False):
    print("Useless Variable:" ,dummy_var)
    try:
        return data[data_index]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= e.__str__()
        )






'''
POST with query params
POST 127.0.0.1:8000/items?item=mango
'''
@appo.post("/items")
def items(item: str):
    data.append(item)
    return data






'''
GET with query params
GET 127.0.0.1:8000/items?item=mango
'''
@appo.get("/items2")
def items(item: str):
    data.append(item)
    return data





'''
GET & POST with Pydantic Object
POST expects JSON payload in Request Params body 
GET expects name of student to return Student() object in dictionary (i.e JSON) form

POST 127.0.0.1:8000/students  -d '{"name":"Zee","age":100}'
GET 127.0.0.1:8000/students/Zee
'''
from pydantic import BaseModel
class Student(BaseModel):
    name: str
    age: int = 18


student_db = {}

@appo.get("/students/{name}")
def get_student_pydantic(name: str) -> Student:
    return student_db[name]

'''
below 2 are also same it'll return data in same format of Student
'''
# @appo.get("/students/{name}")
# def get_student_pydantic(name: str):
#     return student_db[name]


# @appo.get("/students/{name}", response_model=Student)
# def get_student_pydantic(name: str):
#     return student_db[name]


'''
age value is not mandatory since default value is set to 10
age in str form also acceptable fastapi can parse str to int intrinsically but fails if non-integer, float etc
'''
@appo.post("/students")
def set_student_pydantic(student: Student) -> Student:
    student_db[student.name] = student
    return student
