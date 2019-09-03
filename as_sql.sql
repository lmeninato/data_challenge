select "Year", "Month", "Border", "Measure", "Value", 
COALESCE("Average", 0) as "Average"
from
(select "Year", "Month", "Border", "Measure", "Value",
LAG("avg_value") OVER
      (PARTITION BY "Measure", "Border" ORDER BY "Year", "Month")
      as "Average"
from
(select *,
ROUND(AVG("Value") OVER
      (PARTITION BY "Measure", "Border" ORDER BY "Year", "Month"))
       as avg_value
from
(select EXTRACT(YEAR FROM "Date") "Year",
	   EXTRACT(MONTH FROM "Date") "Month",
       "Border",
       "Measure",
       SUM("Value") AS "Value"
from border_crossings
group by "Year", "Month", "Border", "Measure")
as grouped_crossings)
as averaged_crossings)
as lagged_average_crossings
order by "Year" desc, "Month" desc, "Value" desc, "Border" desc, "Measure" desc;
