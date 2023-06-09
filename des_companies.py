def des_companies(rows):
    class Company:
        def __init__(self, identify: int, title: str, founded: str, field: str):
            self.identify = identify
            self.title = title
            self.founded = founded
            self.field = field
            self.workers: list[Worker] = []

    class Worker:
        def __init__(self, identify: int, f_name: str, s_name: str, age: int, education: str):
            self.identify = identify
            self.f_name = f_name
            self.s_name = s_name
            self.age = age
            self.education = education

    companies_dict = {}
    workers_dict = {}

    for row in rows:
        c_id = row['c_id']
        title = row['title']
        founded = row['founded']
        field = row['field']

        company = None
        if c_id in companies_dict:
            company = companies_dict[c_id]
        else:
            company = Company(c_id, title, founded, field)
            companies_dict[c_id] = company

        w_id = row['w_id']
        f_name = row['f_name']
        s_name = row['s_name']
        age = row['age']
        education = row['education']

        worker = None
        if w_id in workers_dict:
            worker = workers_dict[w_id]
        else:
            worker = Worker(w_id, f_name, s_name, age, education)
            workers_dict[w_id] = worker

        if w_id is not None:
            if worker not in company.workers: 
                company.workers.append(worker)

    return list(companies_dict.values())
