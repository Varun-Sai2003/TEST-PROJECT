use this command to run:

# Data Masking Script

This repository contains a script, `datamask.py`, for masking sensitive data in an Excel file.

## Usage

To mask data in a given Excel file (`data.xlsx`) and output the masked data to another Excel file (`masked_data.xlsx`), you can use the following command:

```bash
python datamask.py data.xlsx masked_data.xlsx --columns name:name email:email phone:phone ssn:ssn credit_card:credit_card address:address date:date

