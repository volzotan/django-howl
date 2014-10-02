# howl

howl is a modular home automation application, aimed at providing a common platform for low cost sensors, actuators and interfaces.
Devices are added as django apps to the howl project. Non user-triggered actions can be fired via Celerys Periodic Tasks.

## Apps:

* Roomsensor: generic sensor with a REST interface
* MongoDB: adapter for MongoDB collections
* forecast: [forecast.io](www.forecast.io) app