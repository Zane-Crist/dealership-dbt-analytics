with stg_journals as (
    select * from {{ ref('stg_journal_entries') }}
)

select
    journal_id,          
    posting_date,        -- Foreign key to dim_date
    dealership_id,       -- Foreign key to dim_dealer
    account_id,          -- Foreign key to dim_account
    employee_id,         -- Foreign key to dim_employee
    sku_id,              -- Foreign key to dim_sku
    description,         -- Degenerate dimension (line memo / description)
    debit,               -- Numeric measure
    credit               -- Numeric measure
from stg_journals