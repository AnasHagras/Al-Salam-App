import random
import string
import math


def generateOTP():
    # generate otp of 4 digits numbers
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return "1234"
    return OTP


def send_message_to_number(user, otp):
    # send otp to user
    pass
