-- tests/assert_oem_rebate_allocations_match_bulk.sql
-- Validates that total allocated OEM rebates match the original unallocated bulk entries in GL Account 4950.

with bulk_source as (
    select 
        sum(gl.credit - gl.debit) as total_bulk
    from {{ ref('stg_journal_entries') }} gl
    join {{ ref('stg_accounts') }} a 
        on gl.account_id = a.account_id
    where a.account_number = 4950
      and gl.credit > 0
),

allocated_mart as (
    select 
        sum(allocated_rebate_amount) as total_allocated
    from {{ ref('fct_oem_rebate_allocations') }}
)

select 
    b.total_bulk,
    a.total_allocated,
    abs(b.total_bulk - a.total_allocated) as variance
from bulk_source b
cross join allocated_mart a
where abs(b.total_bulk - a.total_allocated) > 0.01