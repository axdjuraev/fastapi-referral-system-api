from axabc.db import BaseRepoCollector
from src.db import repository as repo


class RepoCollection(BaseRepoCollector):
    users: repo.UsersRepository
    refferal_code: repo.RefferalCodeRepository
