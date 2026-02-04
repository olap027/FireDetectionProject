import serial
import smtplib
import time

# --- CONFIGURATION ---
# Reminder: 1st Verify and Upload the codes on Arduino before run this code!!!!!
PORT = 'COM5' #Verify what port display is working on arduino UNO
EMAIL_SENDER = "bib.ola0927@gmail.com"
EMAIL_RECEIVER = "pola92798@gmail.com"

# ERROR 535 FIX: This MUST be the 16-character code from Google, NOT your regular password.
# It usually looks like this: "abcd efgh ijkl mnop"
# open 2-way verification then copy the 16-character key
APP_PASSWORD = "sozx nruk vncw tdrh" 

try:
    ser = serial.Serial(PORT, 9600, timeout=1)
    print(f"Connected to Arduino on {PORT}")
    time.sleep(2) 
    ser.reset_input_buffer()
except Exception as e:
    print(f"Serial Connection Error: {e}")
    exit()

def send_notification():
    try:
        subject = "FIRE ALERT: Las Pinas Residence"
        body = "Warning! Fire detected by Arduino IR Sensor!"
        msg = f"Subject: {subject}\n\n{body}"

        print("Connecting to Gmail server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        
        # This is where Error 535 happens if APP_PASSWORD is wrong
        server.login(EMAIL_SENDER, APP_PASSWORD)
        
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg)
        server.quit()
        print("✅ Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("❌ Login Failed (Error 535): Your App Password is incorrect.")
        print("Go to Google Account > Security > App Passwords to generate a 16-character code.")
    except Exception as e:
        print(f"❌ Error: {e}")

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line == "FIRE_DETECTED":
                print("🔥 FIRE DETECTED! Attempting to send email...")
                send_notification()
                time.sleep(15) 
    except Exception as e:
        print(f"System Error: {e}")
        time.sleep(1)