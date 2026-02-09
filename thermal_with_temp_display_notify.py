import serial
import smtplib
import time

# --- CONFIGURATION ---
PORT = 'COM6' 
EMAIL_SENDER = "bib.ola0927@gmail.com"
EMAIL_RECEIVER = "kiesheila.11@gmail.com"
APP_PASSWORD = "sozx nruk vncw tdrh" 

try:
    ser = serial.Serial(PORT, 9600, timeout=1)
    print(f"Connected to Arduino on {PORT}. Initializing...")
    # Wait for Arduino to finish resetting before clearing buffer
    time.sleep(3) 
    ser.reset_input_buffer()
    print("Monitoring active.")
except Exception as e:
    print(f"Serial Connection Error: {e}")
    exit()

def send_notification(temp_value):
    try:
        subject = f"🔥 FIRE ALERT: {temp_value}°C Detected"
        body = f"Warning! High heat detected at Las Piñas Residence.\n\nTemperature: {temp_value}°C\nRelay Pin 7 has been activated."
        msg = f"Subject: {subject}\n\n{body}"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(EMAIL_SENDER, APP_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg)
        server.quit()
        print(f"✅ Alert Email sent for {temp_value}°C!")
    except Exception as e:
        print(f"❌ Email Error: {e}")

last_email_time = 0

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            # Check for the ALERT tag
            if line.startswith("ALERT:"):
                # Extract the temperature number after the colon
                current_temp = line.split(":")[1]
                
                print(f"🚨 FIRE DETECTED! Temperature: {current_temp}°C")
                
                # Cooldown: Only send email once every 60 seconds
                if time.time() - last_email_time > 60:
                    send_notification(current_temp)
                    last_email_time = time.time()
            
            elif line.startswith("NORMAL:"):
                current_temp = line.split(":")[1]
                print(f"Status: Normal ({current_temp}°C)")

    except Exception as e:
        print(f"System Error: {e}")
        time.sleep(1)

