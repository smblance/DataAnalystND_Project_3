# DataAnalystND_Project_3
This is a Project 3 for Udacity Data Analyst NanoDegree.<br />
The project is about auditing and cleaning OpenStreetMap data, putting it into MongoDB and running some queries.

The python files are to be executed in the following order:<br />
sample_map.py -> makes sample of the Moscow - SW.osm, writing every 10th top-level element. Provided by Udacity<br />
osm_to_json.py -> saves Moscow - SW.osm as data.json, without cleaning.<br />
popular_tag.py -> makes a dict {tag:frequency of tag}.<br />
audit_json -> audits and cleans the data, writes into data_cleaned.json.<br />
json_to_db.py -> creates the MongoDB database and writes the cleaned data into it.<br />
query_db.py -> queries DB for some basic statistics about the dataset.<br />
additional_queries.py -> queries DB for bus stops with/without shelter, most popular leisure, sports, shops, cusines and amenities.
