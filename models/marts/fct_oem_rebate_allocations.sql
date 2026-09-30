{{ config(materialized='table') }}

with gl_entries as (
    select * from {{ ref('stg_journal_entries') }}
),

accounts as (
    select * from {{ ref('stg_accounts') }}
),

skus as (
    select * from {{ ref('stg_skus') }}
),

-- 1. Isolate total vehicle sales revenue by Dealership and SKU
sku_sales as (
    select
        gl.dealership_id,
        gl.sku_id,
        sum(gl.credit - gl.debit) as total_sku_revenue
    from gl_entries gl
    join accounts a on gl.account_id = a.account_id
    where a.account_number in (4100, 4110) -- New & Used Vehicle Sales Accounts
      and gl.sku_id is not null
    group by 1, 2
),

-- 2. Calculate each SKU's percentage share of dealership vehicle sales
dealership_sales_totals as (
    select
        dealership_id,
        sku_id,
        total_sku_revenue,
        sum(total_sku_revenue) over (partition by dealership_id) as total_dealership_revenue,
        total_sku_revenue / nullif(sum(total_sku_revenue) over (partition by dealership_id), 0) as sales_weight
    from sku_sales
),

-- 3. Isolate the un-allocated bulk OEM rebate entries (Account 4950)
bulk_rebates as (
    select
        gl.journal_id,
        gl.posting_date,
        gl.dealership_id,
        gl.account_id,
        gl.credit - gl.debit as bulk_rebate_amount,
        gl.description
    from gl_entries gl
    join accounts a on gl.account_id = a.account_id
    where a.account_number = 4950
      and gl.credit > 0
)

-- 4. Allocate bulk rebates across SKUs based on sales weights
select
    md5(concat(cast(r.journal_id as varchar), '-', cast(s.sku_id as varchar))) as rebate_allocation_id,
    r.journal_id,
    r.posting_date,
    r.dealership_id,
    s.sku_id,
    r.account_id,
    r.bulk_rebate_amount,
    s.sales_weight,
    round(r.bulk_rebate_amount * s.sales_weight, 2) as allocated_rebate_amount,
    r.description
from bulk_rebates r
inner join dealership_sales_totals s 
    on r.dealership_id = s.dealership_id