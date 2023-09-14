from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from jnius import autoclass
from datetime import datetime
import smtplib


def send_email():
    fromaddr = "team.kapamia@gmail.com"
    toaddrs = "makumbamomanyi@gmail.com"
    msg = "IT WORKS!"
    username = "team.kapamia@gmail.com"
    password = "iqlwwsulekifybhf"  # Application specific password
    server = smtplib.SMTP('smtp.gmail.com:587')

    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def fetch_messages():
    try:
        SmsContract = autoclass("android.provider.Telephony$Sms")
        SmsInbox = autoclass("android.provider.Telephony$Sms$Inbox")
        cr = autoclass('org.kivy.android.PythonActivity').mActivity.getContentResolver()

        messages = []

        # Define the columns we want to retrieve from the SMS content provider
        projection = [SmsContract._ID, SmsContract.ADDRESS, SmsContract.BODY, SmsContract.DATE]

        # Query the SMS inbox to retrieve the SMS messages
        cursor = cr.query(SmsInbox.CONTENT_URI, projection, None, None, None)

        if cursor is not None:
            while cursor.moveToNext():
                sms_id = cursor.getLong(cursor.getColumnIndex(SmsContract._ID))
                address = cursor.getString(cursor.getColumnIndex(SmsContract.ADDRESS))
                body = cursor.getString(cursor.getColumnIndex(SmsContract.BODY))
                date = cursor.getLong(cursor.getColumnIndex(SmsContract.DATE))

                # Convert date timestamp to a human-readable format
                date_str = datetime.fromtimestamp(date / 1000.0).strftime('%Y-%m-%d %H:%M:%S')

                # Append the message details to the list
                messages.append({
                    "SMS ID": sms_id,
                    "Sender/Recipient": address,
                    "Body": body,
                    "Date": date_str
                })

            cursor.close()
            return messages
        else:
            return "No SMS messages found in the inbox."
    except:
         return "Negative state"

def fetch_contacts():
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        ContactsContract = autoclass("android.provider.ContactsContract")
        Contacts = autoclass("android.provider.ContactsContract$Contacts")
        Kinds = autoclass("android.provider.ContactsContract$CommonDataKinds$Phone")

        cr = PythonActivity.mActivity.getContentResolver()
        contact_names = []
        num = 0

        query1 = cr.query(Kinds.CONTENT_URI, None, None, None, None)

        while query1.moveToNext():
            if query1.getString(query1.getColumnIndex(Contacts.HAS_PHONE_NUMBER)):
                contact_names.append({
                    "contact name": query1.getString(query1.getColumnIndex(Contacts.DISPLAY_NAME)),
                    'contact number': query1.getString(query1.getColumnIndex(Kinds.NUMBER))
                })

        return contact_names

    except:
        return "Negative state"


class MyApp(App):
    def build(self):
    
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        self.label = Label(text="Remote Information", size_hint_y=None, height=dp(50))
        
        sms_button = Button(text="Display SMS Messages", size_hint_y=None, height=dp(50))
        sms_button.bind( on_press=self.display_messages)
        contact_button = Button(text="Display Contacts", size_hint_y=None, height=dp(50))
        contact_button.bind(on_press=self.display_contacts)
        email_button = Button(text="Send Email",size_hint_y=None, height=dp(50))
        email_button.bind( on_press=self.send_email)

        self.scroll_view = ScrollView(size_hint=(1, None), height=Window.height - dp(200))
        self.message_label = Label(text="", size_hint=(1, None), height=self.scroll_view.height)

        layout.add_widget(self.label)
        layout.add_widget(sms_button)
        layout.add_widget(contact_button)
        layout.add_widget(email_button)
        layout.add_widget(self.scroll_view)

        self.scroll_view.add_widget(self.message_label)

        return layout

    def display_messages(self, instance):
        messages = fetch_messages()
        messages_text = "".join(str(msg) for msg in messages)
        self.message_label.text = messages_text

    def display_contacts(self, instance):
        contacts = fetch_contacts()
        contacts_text = "".join(str(contact) for contact in contacts)
        self.message_label.text = contacts_text

    def send_email(self, instance):
        send_email()
        self.label.text = "Email sent successfully!"

if __name__ == "__main__":
    from kivy.core.window import Window
    Window.size = (360, 640)  # Set the window size suitable for a phone screen
    MyApp().run()






