import json
import boto3

from botocore.exceptions import WaiterError
from botocore.waiter import WaiterModel
from botocore.waiter import create_waiter_with_client

mail_prefix='workshop'
mail_domain='example.com'
source_parent_id='r-xxxxx'
destination_parent_id='ou-xxxxxxx'
start=1
stop=50

delay = 2
max_attempts = 30
waiter_name = 'AccountCreated'
waiter_config = {
    'version': 2,
    'waiters': {
        'AccountCreated': {
            'operation': 'DescribeCreateAccountStatus',
            'delay': delay,
            'maxAttempts': max_attempts,
            'acceptors':[
                {
                    "matcher": "path",
                    "expected": "IN_PROGRESS",
                    "argument": "CreateAccountStatus.State",
                    "state": "retry"
                },
                {
                    "matcher": "path",
                    "expected": "SUCCEEDED",
                    "argument": "CreateAccountStatus.State",
                    "state": "success"
                },
                {
                    "matcher": "path",
                    "expected": "FAILED",
                    "argument": "CreateAccountStatus.State",
                    "state": "failure"
                }
            ],
        },
    },
}

waiter_model = WaiterModel(waiter_config)
org = boto3.client('organizations')
custom_waiter = create_waiter_with_client(
    waiter_name=waiter_name,
    waiter_model=waiter_model,
    client=org
)

for i in range(start, stop+1):
    str_i = str(i)
    response = org.create_account(
        Email='{mail_prefix}{i}@{mail_domain}'.format(
            mail_prefix=mail_prefix,
            i=str_i,
            mail_domain=mail_domain
        ),
        AccountName='{mail_prefix}{i}'.format(
            mail_prefix=mail_prefix,
            i=str_i
        ),
        RoleName='OrganizationAccountAccessRole'
    )
    print(response)
    create_account_request_id = response.get('CreateAccountStatus').get('Id')

    custom_waiter.wait(
        CreateAccountRequestId=create_account_request_id
    )

    response = org.describe_create_account_status(
        CreateAccountRequestId=create_account_request_id
    )

    account_id = response.get('CreateAccountStatus').get('AccountId')
    print(account_id)
    response = org.move_account(
        AccountId=account_id,
        SourceParentId=source_parent_id,
        DestinationParentId=destination_parent_id
    )
    print(response)