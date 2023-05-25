import boto3

# Storing Data in DigitalOcean Spaces
def upload_to_spaces(bucket_name, object_name, data, endpoint, access_key, secret_key, metadata=None):
    s3 = boto3.client('s3',
                      endpoint_url=endpoint,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
    # Add metadata to the object
    if metadata:
        s3.put_object(Bucket=bucket_name, Key=object_name, Body=data, Metadata=metadata)
    else:
        s3.put_object(Bucket=bucket_name, Key=object_name, Body=data)


# Data Transformation
def transform_data(data):
    # Apply your business rules and logic for data transformation
    transformed_data = data.lower()  # Example transformation: convert to uppercase
    return transformed_data

