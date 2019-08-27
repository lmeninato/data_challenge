# My Notes

To do:
- [x] Need to assert correct ordering:
if index i > j, then row_i\[year\] <= row_j\[year\]
if index i > j, then row_i\[month\] <= row_j\[month\]
if index i > j, then row_i\[value\] <= row_j\[value\]
with more time, i'd want to do a check that dates are decreasing
data quality is high, so I will skip those assertions
I will ensure that for a dates, rows are in decreasing order of value.
- [x] Add running monthly average:
Note that the formula for a row's average column is the sum of previous values, divided by
the number of months since the first occurrence of a border-measure combination.
Case to consider: what if the previous value occurs more than one month previously?
Do we fill-forward missing values, or interpolate, or fill-backward? Assume value for missing months is 0.

- Add logging for errors, profiling time to run parts of code.


# Insight Instructions
## Input Dataset

For this challenge, you will be given an input file, `Border_Crossing_Entry_Data.csv`, that will reside in the top-most `input` directory of your repository.

The file contains data of the form:

```
Port Name,State,Port Code,Border,Date,Measure,Value,Location
Derby Line,Vermont,209,US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,POINT (-72.09944 45.005)
Norton,Vermont,211,US-Canada Border,03/01/2019 12:00:00 AM,Trains,19,POINT (-71.79528000000002 45.01)
Calexico,California,2503,US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346158,POINT (-115.49806000000001 32.67889)
Hidalgo,Texas,2305,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,156891,POINT (-98.26278 26.1)
Frontier,Washington,3020,US-Canada Border,02/01/2019 12:00:00 AM,Truck Containers Empty,1319,POINT (-117.78134000000001 48.910160000000005)
Presidio,Texas,2403,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,15272,POINT (-104.37167 29.56056)
Eagle Pass,Texas,2303,US-Mexico Border,01/01/2019 12:00:00 AM,Pedestrians,56810,POINT (-100.49917 28.70889)
```
See the [notes from the Bureau of Transportation Statistics](https://data.transportation.gov/Research-and-Statistics/Border-Crossing-Entry-Data/keg4-3bc2) for more information on each field.

For the purposes of this challenge, you'll want to pay attention to the following fields:
* `Border`: Designates what border was crossed
* `Date`: Timestamp indicating month and year of crossing
* `Measure`: Indicates means, or type, of crossing being measured (e.g., vehicle, equipment, passenger or pedestrian)
* `Value`: Number of crossings

## Expected Output
Using the input file, you must write a program to
* Sum the total number of crossings (`Value`) of each type of vehicle or equipment, or passengers or pedestrians, that crossed the border that month, regardless of what port was used.
* Calculate the running monthly average of total crossings, rounded to the nearest whole number, for that combination of `Border` and `Measure`, or means of crossing.

Your program must write the requested output data to a file named `report.csv` in the top-most `output` directory of your repository.

For example, given the above input file, the correct output file, `report.csv` would be:

```
Border,Date,Measure,Value,Average
US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346158,114487
US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,0
US-Canada Border,03/01/2019 12:00:00 AM,Trains,19,0
US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,172163,56810
US-Canada Border,02/01/2019 12:00:00 AM,Truck Containers Empty,1319,0
US-Mexico Border,01/01/2019 12:00:00 AM,Pedestrians,56810,0

```

The lines should be sorted in descending order by
* `Date`
* `Value` (or number of crossings)
* `Measure`
* `Border`

The column, `Average`, is for the running monthly average of total crossings for that border and means of crossing in all previous months.
In this example, to calculate the `Average` for the first line (i.e., running monthly average of total pedestrians crossing the US-Mexico Border in all of the months preceding March),
you'd take the average sum of total number of US-Mexico pedestrian crossings in February `156,891 + 15,272 = 172,163` and January `56,810`,
and round it to the nearest whole number `round(228,973/2) = 114,487`
