# Documentation for darts
### fastAPI: API to keep track of the scores and game types in darts


Test: Darts (should be capitalized)


This application has two generic endpoints:

| Method | URL Pattern           | Description             |
|--------|-----------------------|--------------------|
| GET    | /api/v1/darts/info         | Basic description of the application and container     |
| GET    | /api/v1/darts/health    | Health check endpoint     |



## CRUD Endpoints:
| Method | URL Pattern           | Description             | Example             |
|--------|-----------------------|--------------------|---------------------|
| GET    | /api/v1/darts         | List all darts     | /api/v1/darts       |
| GET    | /api/v1/darts/{id}    | Get darts by ID     | /api/v1/darts/42    |
| POST   | /api/v1/darts         | Create new darts    | /api/v1/darts       |
| PUT    | /api/v1/darts/{id}    | Update darts (full) | /api/v1/darts/42    |
| PATCH  | /api/v1/darts/{id}    | Update darts (partial) | /api/v1/darts/42 |
| DELETE | /api/v1/darts/{id}    | Delete darts        | /api/v1/darts/42    |


### Access the info endpoint
http://home.dev.com/api/v1/darts/info

### View test page
http://home.dev.com/darts/test/darts.html

### Swagger:
http://home.dev.com/api/v1/darts/docs