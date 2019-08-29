# Notes

My approach to the problem is to reduce the `input.csv` file containing `N` lines to `n` 
key-value pairs where `n << N`. This approach is efficient when many rows map to the same tuple. 
Each row is comprised of five relevant features: `Year`, `Month`, `Border`, `Measure`, and `Value`. 
We can parse each row as a key-value pair `(Year, Month, Border, Measure):Value`.
This approach is efficient when many rows map to the same tuple key. In the best case, all rows are
reduced to a single key-value pair (the value being the sum of the value field across all rows).
The time complexity would require reading O(N) lines and O(1) additional space to calculate and 
store the result in memory. In the worst case, each row is reduced a unique key-value pair. The read 
time would be the same, but the algorithm would require O(N) space to store each row. For datasets
larger than the system's available memory, this program would not be feasible. Later I will outline
some ideas for handling such data.

Keeping in mind this concern, I still implemented the solution by using this hashing trick. Due to the 
nature of the data, there is a pretty reasonable upper bound on the additional space required to store
the key-value pairs. The `Month` and `Border` fields can only have 12 and 2 unique possible values, respectively.
For the `Year` field, there is likely going to be less than 100 valid values. Similarly, while there could
be an arbitrary quantity of unique `Measure` fields, the Transportation Website lists less than 15 possible
measures. Assuming each field requires less than 100 bytes of storage, the upper bound on memory required
to store a hash table of the reduced key-value pairs would be 12\*2\*100\*15 = 36K \* (100 bytes) or approximately
3.6MB of memory (this could be dramatically lower, if we used something like a Huffman Coding to store each
unique field value as the minimal amount of bytes). 

With this setup in place, the remaining steps are fairly simple. Thanks to hashing our key-value pairs, we can track
the first occurrence of a `(Measure, Border)` pair and the corresponding running total value for the pair.
Then the running monthly average is `(previous_total)/(current_month - first_month)`. Then we format and add each row
to a list, then sort in descending order in the following manner:
* `Date`
* `Value` 
* `Measure`
* `Border`

Then we write each row in the list of lists to `results.csv`.

## Streaming Algorithm

The main concern over using a streaming algorithm is without a date ordering we would still have to store N rows in
the worst case (either in memory, or by writing to a temporary table on a disk). With some ordering this approach
would work well, and for a problem where the hashing trick does not have such a small upper bound on the additional
space required a streaming algorithm would be necessary to not exhaust the system's memory (or to avoid read/write
from disk for temporary storage).



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
