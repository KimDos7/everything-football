import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table (
    TableName = 'UserDataStorage',
       KeySchema = [
           {
               'AttributeName': 'Username',
               'KeyType': 'HASH'
           },
           {
               'AttributeName': 'UsernameTag',
               'KeyType': 'RANGE'
           }
           ],
           AttributeDefinitions = [
               {
                   'AttributeName': 'Username',
                   'AttributeType': 'S'
               },
               {
                   'AttributeName':'UsernameTag',
                   'AttributeType': 'S'
               }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits':1,
                'WriteCapacityUnits':1
            }
          
    )
print(table)

