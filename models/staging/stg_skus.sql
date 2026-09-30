with raw_skus as (
    select * from {{ ref('D_SKU') }}
),

staged as (
    select
        sku as sku_id,
        description as sku_description,
        sku_type as sku_type,
        supplier as supplier,
        department as department,
        class as class,
        subclass as subclass,
        unit_of_measure as unit_of_measure,
        active_flag as is_active,
        dealership_id as target_dealership_id
    from raw_skus
)

select * from staged