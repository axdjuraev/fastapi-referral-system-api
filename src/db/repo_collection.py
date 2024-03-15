from axabc.db import BaseRepoCollector
from src.db import repository as repo


class RepoCollection(BaseRepoCollector):
    users: repo.UsersRepository
    referral_code: repo.RefferalCodeRepository
    otp_code: repo.OTPCodeRepository
