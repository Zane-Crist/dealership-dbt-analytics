with journal_entries as (

    select * from {{ ref('stg_journal_entries') }}

),

accounts as (

    select * from {{ ref('stg_accounts') }}

),

dealers as (

    select * from {{ ref('stg_dealers') }}

),

employees as (

    select * from {{ ref('stg_employees') }}

),

skus as (

    select * from {{ ref('stg_skus') }}

),

fact_table as (

    select
        je.journal_id,
        je.posting_date,
        
        -- Dealer Dimensions
        d.dealership_id,
        d.dealership_name,
        d.primary_brand,
        
        -- Account Dimensions
        a.account_id,
        a.account_number,
        a.account_name,
        a.account_type,
        a.account_group,
        
        -- Employee Dimensions
        e.employee_id,
        e.employee_name,
        e.employee_type,
        
        -- SKU / Product Dimensions
        s.sku_id,
        s.sku_description,
        s.sku_type,
        s.department as sku_department,
        
        -- Financial Measures
        je.debit,
        je.credit,
        je.net_amount,
        je.description
    from journal_entries je
    left join accounts a on je.account_id = a.account_id
    left join dealers d on je.dealership_id = d.dealership_id
    left join employees e on je.employee_id = e.employee_id
    left join skus s on je.sku_id = s.sku_id

)

select * from fact_table