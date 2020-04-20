# API for HR Managers to request, review and approve time off.

## Routes

### /api/leaves

**GET** : get leaves that have been recieved or sent by user

**POST** : create a new leave request

### /api/leaves/{id}

**PUT** : modify the given leave

**DELETE** : Delete the leave

**GET**: Get leave details

## Model

_id : Leave id
sender : Person who requested for the leave 
leave_type = TYpe of Leave
start_time = Start Date
end_time = End Date
manager = Person to whom request is sent
details = Additional Details
accepted = Boolean if accepted or not

