with raw_employees as (

    select * from {{ ref('raw_employees') }}

),

staged as (

    select
        "Employee_ID" as employee_id,
        "Employee_Name" as employee_name,
        "Employee_Type" as employee_type,
        "Dealership_ID" as dealership_id,
        "Hire_Date"::date as hire_date,
        "Active_Flag" as is_active
    from raw_employees

)

select * from staged