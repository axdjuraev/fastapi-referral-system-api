from axabc.db import BaseRepoCollector
from src.db import repository as repo


class RepoCollection(BaseRepoCollector):
    users: repo.UsersRepository
    referral_code: repo.ReferralCodeRepository
    otp_code: repo.OTPCodeRepository
