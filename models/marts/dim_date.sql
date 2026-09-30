{{ config(
    materialized='table'
) }}

with date_spine as (

    select 
        generate_series::date as date_day
    from generate_series(
        date '2020-01-01', 
        date '2030-12-31', 
        interval '1 day'
    )

),

final as (

    select
        date_day,
        
        -- Primary Key surrogate key (e.g., 20250101)
        cast(strftime(date_day, '%Y%m%d') as integer) as date_id,
        
        -- Year & Quarter attributes
        extract(year from date_day) as year_number,
        extract(quarter from date_day) as quarter_number,
        'Q' || extract(quarter from date_day) as quarter_name,
        
        -- Month attributes
        extract(month from date_day) as month_number,
        strftime(date_day, '%B') as month_name,
        strftime(date_day, '%b') as month_short_name,
        date_trunc('month', date_day)::date as first_day_of_month,
        last_day(date_day) as last_day_of_month,
        
        -- Day attributes
        extract(day from date_day) as day_of_month,
        extract(dayofyear from date_day) as day_of_year,
        
        -- Week attributes
        extract(dayofweek from date_day) as day_of_week_number, -- 0 = Sunday, 6 = Saturday in DuckDB
        strftime(date_day, '%A') as day_name,
        strftime(date_day, '%a') as day_short_name,
        extract(week from date_day) as week_of_year,
        
        -- Useful BI boolean flags for fast filtering
        case 
            when extract(dayofweek from date_day) in (0, 6) then true 
            else false 
        end as is_weekend,
        
        case 
            when date_day = last_day(date_day) then true 
            else false 
        end as is_month_end

    from date_spine

)

select * from final