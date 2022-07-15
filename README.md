# nrjson2graphql

### Dashboard JSON converter. 

Helps to use existing Dashboard as a template for newRelicUploader Taurus plugin.
Details : https://github.com/doctornkz/newrelicUploader

### Mechanic
Processing JSON as a simple string, escaping double quotes, adding GraphQL mutation header.

### How to use:

```
$ /usr/bin/python3 nrjson2graphql/nrjson2graphql.py tests/dashboard1.json
mutation {dashboardCreate(accountId: ACCOUNT_PLACE_HOLDER, dashboard:{
    name: 'Load Tests [PROJECT_PLACE_HOLDER]'
    description: null,
    permissions: "PUBLIC_READ_WRITE",
    pages: [
      {
        name: "One Page to Rule Them All",
        description: null,
        widgets: [
          {
            title: "counter by status code",
            layout: {
              column: 1,
              row: 1,
              width: 6,
              height: 2
            },
            linkedEntityGuids: null,
            visualization: {
              id: "viz.table"
            },
            rawConfiguration: {
              dataFormatters: [],
              facet: {
                showOtherSeries: false
              },
              nrqlQueries: [
                {
                  accountId: ACCOUNT_PLACE_HOLDER
                  query: "SELECT sum(bztcode) as count FROM Metric FACET rc as HTTP_CODE where project like 'PROJECT_PLACE_HOLDER'"
...
```

Reroute STDOUT to file, define file in load.yaml and that's it:
```
$ /usr/bin/python3 nrjson2graphql/nrjson2graphql.py tests/dashboard1.json > dashboard_tpl.gql

$ cat load.yaml
execution:

## Siege example:
- executor: siege
  concurrency: 3 
  iterations: 10
  scenario: simplest
scenarios:
  simplest:
    requests:
    - https://example.com/

reporting:
  - module: newrelic

modules:
    newrelic:
      project: my-ticket-12345 # jira-ticket|pack name|etc. 
      dashboard-template-path: dashboard_tpl.gql # template path/filename for new dashboard.

```
