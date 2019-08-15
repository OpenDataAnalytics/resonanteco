# ResonantEco

## Develop environment setup

ResonantEco has server, client two components. They are located under *server* and *client* directory respectively.

### Prerequisite
* Pyhton 3.5+
* Mongodb running at the default port
* Node 8
* Clone this repo `git clone https://github.com/OpenDataAnalytics/resonanteco.git`

### Server

* `pip install -e ./resonanteco/server/`
* `girder build`
The girder interface will be available at http://localhost:8080/girder

### Client
The client is a [Vue CLI](https://cli.vuejs.org/) based application. All Vue-CLI options are available. 

* `cd ./resonanteco/client`
* `yarn install`
* `yarn serve`
* Navigate to `localhost:8081`
* Register user then login the system

#### linting
* `yarn lint`

### Data ingestion
* In the same python envrionment as the server
* Navigate to `server/data`
* `export GIRDER_MONGO_URI=mongodb://localhost:27017/girder-resonanteco` if you db is not the default girder
* execute `python ingest.py ./data`
