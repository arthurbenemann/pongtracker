# pongtracker

Build wiht:
`docker build --tag test .`

Run with:
`docker run --rm -p 8080:5000 -e URL_GSHEET="Google sheet URL"`, 

Google sheets is used as the database, it should be shared as `Viewer` for `anyone with the link`. Example table below:

|win	|loss	| date
|--|--|--|
|A | B|	20240701|
|A | C|	|
|D | B|	|
|AC | CB| 20240702	|
|CB | AD| 	|
