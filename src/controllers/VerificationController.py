import os
from twilio.rest import Client

def verification():
    account_sid = "AC71fe53ec2dfed522c750de17b5fcdbaf"
    auth_token = "2de456c412533d905b2e76fcc8f5c935"
    verify_sid = "VAbd25cf8f908bd1c0619dfeca506ccfb1"
    verified_number = "+528186816362"

    client = Client(account_sid, auth_token)

    verification = client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to=verified_number, channel="sms")
    print(verification.status)
    otp_code = input("Please enter the OTP:")

    verification_check = client.verify.v2.services(verify_sid) \
    .verification_checks \
    .create(to=verified_number, code=otp_code)
    print(verification_check.status)

verification()