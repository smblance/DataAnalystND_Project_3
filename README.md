# DataAnalystND_Project_3
This is a Project 3 for Udacity Data Analyst NanoDegree.

The project is about auditing and cleaning OpenStreetMap data, putting it into MongoDB and running some queries.

The python files are to be executed in the following order:

sample_map.py -> makes sample of the Moscow - SW.osm, writing every 10th top-level element.

osm_to_json.py -> saves Moscow - SW.osm as data.json, without cleaning.

popular_tag.py -> makes a dict {tag:frequency of tag}.

audit_json -> audits and cleans the data, writes into data_cleaned.json.

json_to_db.py -> creates the MongoDB database and writes the cleaned data into it.

query_db.py -> queries DB for some basic statistics about the dataset.

additional_queries.py -> queries DB for bus stops with/without shelter, most popular leisure, sports, cusines and amenities.
