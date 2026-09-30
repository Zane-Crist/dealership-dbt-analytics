with raw_accounts as (

    select * from {{ ref('D_Accounts') }}

),

staged as (

    select
        "Account_ID" as account_id,
        "Account_Number" as account_number,
        "Account_Description" as account_name,
        "Account_Type" as account_type,
        "Account_Group" as account_group
    from raw_accounts

)

select * from staged