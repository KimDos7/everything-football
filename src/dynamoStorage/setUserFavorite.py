import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('UserDataStorage')


def updateUserFavoriteTeam(userName, digits, favTeam):
    
    response = table.put_item(
        Item={
            'Username': str(userName),
            'UsernameTag': str(digits),
            'favorite_team': favTeam
        }
    )

    response = table.get_item(
        Key={
            'Username': str(userName),
            'UsernameTag': str(digits)
        }
    )

    return response['Item']

def getUserFavoriteTeam(userName, digits):
    response = table.get_item(
        Key={
            'Username': str(userName),
            'UsernameTag': str(digits)
        }
    )

    print(response)
    return response['Item']['favorite_team']