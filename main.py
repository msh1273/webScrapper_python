from indeed import get_jobs as get_indeed_jobs
from stackof import get_jobs as get_stackof_jobs
from save import save_to_file


indeed_jobs = get_indeed_jobs()
so_jobs = get_stackof_jobs()

jobs = indeed_jobs + so_jobs

save_to_file(jobs)
