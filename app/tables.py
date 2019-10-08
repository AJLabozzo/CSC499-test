from flask_table import Table, Col

class Results(Table):
    id = Col('id', show=False)
    projectname = Col('Project')
    body = Col('Description')
    user_id = Col('User')
    department = Col('Department')
    
