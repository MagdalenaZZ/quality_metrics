import argparse
import csv
from collections import defaultdict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def analyze_samples(input_file):
    if not os.path.isfile(input_file) or os.path.getsize(input_file) == 0:
        print("The input file does not exist or is empty.")
        return

    origins = defaultdict(lambda: {'total': 0, 'failed': 0, 'failed_samples': []})
    
    with open(input_file, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            origin = row['sample'][:2]
            origins[origin]['total'] += 1
            
            if float(row['pct_covered_bases']) < 95.0 or row['qc_pass'] == 'FALSE':
                origins[origin]['failed'] += 1
                origins[origin]['failed_samples'].append(row['sample'])  # Keep track of failed samples
                
    for origin, counts in origins.items():
        if counts['total'] > 0:
            failed_pct = (counts['failed'] / counts['total']) * 100
            if failed_pct > 5:
                send_email(origin, failed_pct, counts['failed_samples'])  # Pass failed samples to the email function

def send_email(origin, failed_pct, failed_samples):
    email_map = {'DN': 'dn@gmail.com', 'DC': 'dc@gmail.com', 'DT': 'dt@gmail.com', 'DD': 'dd@gmail.com'}
    email_to = email_map.get(origin, 'qualitymetrics98@gmail.com')
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "qualitymetrics98@gmail.com"
    smtp_password = "your_app_password"
    
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email_to
    msg['Subject'] = f"Sample Quality Alert for Origin {origin}"
    
    # Construct the email body with failed samples listed
    body = f"Attention: Over 5% of samples from origin {origin} have failed the quality check. ({failed_pct:.2f}% failed)\n\nID of failed samples:\n" + "\n".join(failed_samples)
    msg.attach(MIMEText(body, 'plain'))
    print("EMAIL:",smtp_user, email_to, f"Sample Quality Alert for Origin {origin}", body, "\n" )   
 
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, email_to, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {email_to}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Analyze sample quality from an input file and notify if failures exceed threshold.")
    parser.add_argument("input_file", help="Input CSV file containing sample data.")
    args = parser.parse_args()
    
    analyze_samples(args.input_file)

if __name__ == '__main__':
    main()




