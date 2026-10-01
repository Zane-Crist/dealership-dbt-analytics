with raw_journal_entries as (

    select * from {{ ref('raw_journal_entries') }}

),

staged as (

    select
        journal_id,
        posting_date::date as posting_date,
        dealership_id,
        account_id,
        sku as sku_id,
        employee_id,
        debit,
        credit,
        (debit - credit) as net_amount,
        description
    from raw_journal_entries

)

select * from staged