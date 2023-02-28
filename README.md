# DjangoOTPLogin
Login through OTP only

    [
        Deployed on Railway.app
        Mail Testing done on Mailtrap.io
        MYSQL provision on Railway.app
    ]

## API
    The following API endpoints are available.

#### Generate OTP
`POST /api/user/generateOTP/`
#### Verify OTP
`POST /api/user/generateOTP/`

#### Conditions Implemented
    [
        OTP once used cannot be used again.
        OTP valid for 5 minutes only.
        1 minute gap for another OTP request.
        5 consecutive wrong OTP will restrict the user login for 1 hour. 
    ]