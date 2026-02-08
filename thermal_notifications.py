import serial
import smtplib
import time

# --- CONFIGURATION ---
PORT = 'COM5' 
EMAIL_SENDER = "bib.ola0927@gmail.com"
EMAIL_RECEIVER = "kiesheila.11@gmail.com"
APP_PASSWORD = "sozx nruk vncw tdrh" 

try:
    ser = serial.Serial(PORT, 9600, timeout=1)
    print(f"Connected to Arduino on {PORT}. Monitoring Relay State...")
    time.sleep(2) 
    ser.reset_input_buffer()
except Exception as e:
    print(f"Serial Connection Error: {e}")
    exit()

def send_notification():
    try:
        subject = "RELAY TRIGGERED: Fire Alert at Las Pinas Residence"
        # Body updated to reflect that the Relay Pin activated the email
        body = "Warning! The Relay Pin (Pin 7) has been set to HIGH due to heat detection."
        msg = f"Subject: {subject}\n\n{body}"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(EMAIL_SENDER, APP_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg)
        server.quit()
        print("✅ Alert Email sent based on Relay State!")
    except Exception as e:
        print(f"❌ Error: {e}")

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            # This triggers only when the Arduino confirms the Relay is HIGH
            if line == "FIRE_DETECTED":
                print("🚨 RELAY ACTIVE! Sending email notification...")
                send_notification()
                time.sleep(10) # Wait 30s to prevent spamming your inbox
    except Exception as e:
        print(f"System Error: {e}")
        time.sleep(1)