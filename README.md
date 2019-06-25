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
* `npm install`
* `npm run serve`
* Navigate to `localhost:8081`
* Register user then login the system

#### linting
* `npm run lint`
