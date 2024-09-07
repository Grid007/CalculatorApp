import json

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))  # Log the event object

    try:
        operation = event['pathParameters']['operation']
        a = int(event['pathParameters']['a'])
        b = int(event['pathParameters']['b'])
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'Missing key: {str(e)}'})
        }

    if operation == 'add':
        result = add(a, b)
    elif operation == 'subtract':
        result = subtract(a, b)
    elif operation == 'multiply':
        result = multiply(a, b)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid operation'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'result': result})
    }

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b
