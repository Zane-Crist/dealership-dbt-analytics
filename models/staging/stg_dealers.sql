with raw_dealers as (

    select * from {{ ref('raw_dealers') }}

),

staged as (

    select
        "Dealership_ID" as dealership_id,
        "Dealership_Name" as dealership_name,
        "Primary_Brand" as primary_brand,
        "Active_Flag" as is_active
    from raw_dealers

)

select * from staged