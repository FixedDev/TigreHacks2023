import os
from twilio.rest import Client

def verification(phonenumber):
    account_sid = "AC71fe53ec2dfed522c750de17b5fcdbaf"
    auth_token = "d13481033496d12a51e9e27eb4a4db89"
    verify_sid = "VAbd25cf8f908bd1c0619dfeca506ccfb1"
    verified_number = f"{phonenumber}"

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
    