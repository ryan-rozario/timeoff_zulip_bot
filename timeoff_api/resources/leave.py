from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from database.models import Leave, User
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, LeaveAlreadyExistsError, InternalServerError, \
UpdatingLeaveError, DeletingLeaveError, LeaveNotExistsError
from datetime import datetime
import json


class LeavesApi(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        if "sender" in body:
            sender = body["sender"]
            leaves = Leave.objects(sender=sender, added_by=user_id)
        elif "manager" in body:
            manager = body["manager"]
            leaves = Leave.objects(manager=manager, added_by=user_id)

        leave_list=[]

        for leave in leaves:
            leave_list.append({"id":str(leave.id),"accepted":str(leave.accepted),"sender":str(leave.sender),"leave_type":str(leave.leave_type),"start_time":str(leave.start_time),"end_time":str(leave.end_time),"details":str(leave.details),"manager":str(leave.manager)})

        return leave_list, 200

    @jwt_required
    def post(self):
        try:
            #print(request)
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            sender = body["sender"]
            leave_type = body["leave_type"]
            start_time = datetime.strptime(body["start_time"], '%d/%m/%y')
            end_time = datetime.strptime(body["end_time"], '%d/%m/%y')
            manager = body["manager"]
            details = body["details"]
            #print(body)
            leave =  Leave(sender = sender, leave_type = leave_type,start_time = start_time,end_time = end_time,manager = manager,details = details, added_by=user)
            leave.save()
            user.update(push__leaves=leave)
            user.save()
            id = leave.id
            return {'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise LeaveAlreadyExistsError
        except Exception as e:
            raise InternalServerError
        
class LeaveApi(Resource):
    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            leave = Leave.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            Leave.objects.get(id=id).update(**body)
            leave = Leave.objects.get(id=id, added_by=user_id)
            #updated_leave = json.dumps(leave.__dict__)
            updated_leave={"id":str(leave.id),"sender":str(leave.sender),"leave_type":str(leave.leave_type),"start_time":str(leave.start_time),"end_time":str(leave.end_time),"details":str(leave.details),"manager":str(leave.manager)}
            print(updated_leave)
            return updated_leave, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise LeaveAlreadyExistsError
        except Exception as e:
            raise InternalServerError
    
    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            leave = Leave.objects.get(id=id, added_by=user_id)
            leave.delete()
            return '', 200
        except DoesNotExist:
            raise DeletingLeaveError
        except Exception:
            raise InternalServerError

    def get(self, id):
        try:
            leaves = Leave.objects.get(id=id).to_json()
            return Response(leaves, mimetype="application/json", status=200)
        except DoesNotExist:
            raise DeletingLeaveError
        except Exception:
            raise InternalServerError