import boto3
import sys

org = boto3.client('organizations')

def get_account_id_by_ou(ouid):
    accounts = []
    next_token = 'Initial'
    while next_token is not None:
        if next_token is None or next_token == 'Initial':
            response = org.list_accounts_for_parent(ParentId=ouid)
        else:
            response = org.list_accounts_for_parent(ParentId=ouid, NextToken=next_token)
        next_token = response.get('NextToken')
        for account in response['Accounts']:
            accounts.append({'account_id': account['Id']})
    return accounts

def move_account(account_id, ouid):
    org.move_account(
        AccountId=account_id, 
        SourceParentId=ouid, 
        DestinationParentId='ou-hkry-3sd5bwja'
    )
    print(account_id + ':moved')
    return True

def close_account(account_id):
    org.close_account(
        AccountId=account_id
    )
    print(account_id + ':closed')
    return True

if __name__ == "__main__": 
    ouid = sys.argv[1]
    accounts = get_account_id_by_ou(ouid)
    for account in accounts:
        move_account(account_id, ouid)
        close_account(account_id)

    print('done')
