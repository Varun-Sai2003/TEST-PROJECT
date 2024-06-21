import pandas as pd
import random
import string
import logging
from datetime import datetime
import argparse

# Set up logging
logging.basicConfig(filename='data_masking.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Masking functions
def mask_name(name):
    masked_name = ''.join(random.choices(string.ascii_uppercase, k=len(name)))
    logging.info(f'Masked name: {name} -> {masked_name}')
    return masked_name

def mask_email(email):
    try:
        local, domain = email.split('@')
        masked_local = ''.join(random.choices(string.ascii_lowercase + string.digits, k=len(local)))
        masked_email = masked_local + '@' + domain
        logging.info(f'Masked email: {email} -> {masked_email}')
        return masked_email
    except Exception as e:
        logging.error(f'Error masking email {email}: {e}')
        return email

def mask_phone(phone):
    phone_str = str(phone)
    masked_phone = ''.join(random.choices(string.digits, k=len(phone_str)))
    logging.info(f'Masked phone: {phone} -> {masked_phone}')
    return masked_phone

def mask_aadhar(aadhar):
    masked_aadhar = 'XXXX-XXXX-' + aadhar[-4:]
    logging.info(f'Masked aadhar: {aadhar} -> {masked_aadhar}')
    return masked_aadhar

def mask_credit_card(cc):
    masked_cc = 'XXXX-XXXX-XXXX-' + cc[-4:]
    logging.info(f'Masked credit card: {cc} -> {masked_cc}')
    return masked_cc

def mask_address(address):
    masked_address = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=len(address)))
    logging.info(f'Masked address: {address} -> {masked_address}')
    return masked_address

def mask_date(date):
    try:
        masked_date = (datetime.strptime(date, "%Y-%m-%d") + pd.DateOffset(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        logging.info(f'Masked date: {date} -> {masked_date}')
        return masked_date
    except Exception as e:
        logging.error(f'Error masking date {date}: {e}')
        return date

# Masking configuration
MASKING_FUNCTIONS = {
    'name': mask_name,
    'email': mask_email,
    'phone': mask_phone,
    'ssn': mask_ssn,
    'credit_card': mask_credit_card,
    'address': mask_address,
    'date': mask_date
}

def mask_data(df, columns_to_mask):
    for column, mask_function in columns_to_mask.items():
        if column in df.columns:
            logging.info(f'Start masking column: {column}')
            # Convert column to string if it is not already
            df[column] = df[column].astype(str)
            df[column] = df[column].apply(mask_function)
            logging.info(f'Finished masking column: {column}')
        else:
            logging.warning(f'Column {column} not found in dataset')
    return df

def main(input_file, output_file, columns_to_mask):
    # Read data from Excel file
    try:
        df = pd.read_excel(input_file)
        logging.info(f'Read data from {input_file}')
    except Exception as e:
        logging.error(f'Error reading {input_file}: {e}')
        return

    # Mask data
    df = mask_data(df, columns_to_mask)

    # Write masked data back to Excel file
    try:
        df.to_excel(output_file, index=False)
        logging.info(f'Written masked data to {output_file}')
    except Exception as e:
        logging.error(f'Error writing to {output_file}: {e}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Masking Tool")
    parser.add_argument('input_file', type=str, help='Path to the input Excel file')
    parser.add_argument('output_file', type=str, help='Path to the output Excel file')
    parser.add_argument('--columns', type=str, nargs='+', help='Columns to mask with their respective functions in format column:function')

    args = parser.parse_args()

    # Parse columns to mask
    columns_to_mask = {}
    if args.columns:
        for col_func in args.columns:
            try:
                col, func = col_func.split(':')
                if func in MASKING_FUNCTIONS:
                    columns_to_mask[col] = MASKING_FUNCTIONS[func]
                else:
                    logging.warning(f'Masking function {func} not recognized')
            except ValueError:
                logging.error(f'Invalid format for column:function {col_func}')
    
    main(args.input_file, args.output_file, columns_to_mask)
