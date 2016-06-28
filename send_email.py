import httplib2
import os
import base64
import argparse
import oauth2client

from email.mime.text import MIMEText
from apiclient       import discovery
from apiclient       import errors
from oauth2client    import client
from oauth2client    import tools


# Give full access to the account
# Other scopes can be found here:
# https://developers.google.com/gmail/api/auth/scopes#gmail_scopes
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        credentials = tools.run_flow(flow, store, flags)
        
        print( "Storing credentials to", credential_path )
    return credentials


def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:

    # Decoding all the fields inside the dict
    for key in message:
      message[key] = message[key].decode()

    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print( 'Message Id: %s' % message['id'] )
    return message

  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode( message.as_string().encode() )}


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    sender = 'me'
    to = 'RECEIVER_EMAIL'
    subject = 'Test message'
    message_text = 'This works'
    
    # Creating message
    message = CreateMessage( sender, to, subject, message_text )
    
    # Sending message
    SendMessage( service, "me", message )

    print("done.")


if __name__ == '__main__':
    main()
