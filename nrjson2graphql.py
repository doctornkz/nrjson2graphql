import re
import sys

# Global place holders:
account_placeholder = 'ACCOUNT_PLACE_HOLDER'
project_placeholder = 'PROJECT_PLACE_HOLDER'
dashboard_title = 'Load Tests [' + project_placeholder + ']'


class JsonGraphQLConverter:

    def __init__(self):
        pass

    def string_formatter(self, json_string):
        return re.sub('"(.*)":', r'\1:', json_string)

    def account_placeholding(self, string):
        return re.sub('(accountId: )\d*,', 'accountId: ' + account_placeholder, string)

    def title_render(self, string):
        return re.sub('name: .*', f"name: '{dashboard_title}'", string, 1)

    def project_placeholding(self, string):
        return re.sub("project like '(.*)'", f"project like '{project_placeholder}'", string)

    def header(self, body_json):
        header = f'mutation {{dashboardCreate(accountId: {account_placeholder}, dashboard:'
        return header + body_json + '\n}'

if __name__ == "__main__":

    if len(sys.argv) == 1:                         
        print('''Usage: python3 nrjson2graphql.py [dasboard json file from NewRelic]
        python3 nrjson2graphql.py dashboard.json > dashboard.gql''')
        exit()                                                                                       
    else:
        filename = sys.argv[1]                                                                                                                                                                    
        
    try:
        with open(filename, "r") as f:
            base_string = f.read()
            converter = JsonGraphQLConverter()
            # Convert plain JSON to GraphQL body
            gql = converter.string_formatter(base_string)
            # Replace current dashboard name with template
            title = converter.title_render(gql)
            # Convert dumpled account_id with placeholder
            acc = converter.account_placeholding(title)
            # Convert dumpled project name with placeholder
            prj = converter.project_placeholding(acc)
            # Add GraphQL mutation footer
            mutation = converter.header(prj)

            # Print document to STDOUT
            print(mutation)

            f.close()

    except Exception as e:
        print("Parse log processing error: ", e)
        exit(1)


