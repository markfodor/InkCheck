import gpsoauth

# use the following guide to obtain token:
# https://github.com/rukins/gpsoauth-java/blob/b74ebca999d0f5bd38a2eafe3c0d50be552f6385/README.md#receiving-an-authentication-token
email = 'somebody@gmail.com' # use your own mail address
android_id = '0123456789abcdef' # just leave it as it is
token = '...'  # insert the oauth_token here

master_response = gpsoauth.exchange_token(email, token, android_id)
master_token = master_response['Token']  # if there's no token check the response for more details

# use the printed value in the Google Keep config in the 'password' field
print(master_token)

auth_response = gpsoauth.perform_oauth(
    email, master_token, android_id,
    service='sj', app='com.google.android.keep',
    client_sig='...')
token = auth_response['Auth']
