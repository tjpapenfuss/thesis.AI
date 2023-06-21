import boto3
import mimetypes

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

def upload_file_spaces(space_name, file_src, save_as, endpoint, access_key, secret_key, metadata=None, **kwargs):
    """
    :param spaces_client: Your DigitalOcean Spaces client from get_spaces_client()
    :param space_name: Unique name of your space. Can be found at your digitalocean panel
    :param file_src: File location on your disk
    :param save_as: Where to save your file in the space
    :param kwargs
    :return:
    """

    is_public = kwargs.get("is_public", False)
    content_type = kwargs.get("content_type")
    # meta = kwargs.get("meta")

    if not content_type:
        file_type_guess = mimetypes.guess_type(file_src)

        if not file_type_guess[0]:
            raise Exception("We can't identify content type. Please specify directly via content_type arg.")

        content_type = file_type_guess[0]

    extra_args = {
        'ACL': "public-read" if is_public else "private",
        'ContentType': content_type
    }
    s3 = boto3.client('s3',
                    endpoint_url=endpoint,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key)
    if isinstance(metadata, dict):
        extra_args["Metadata"] = metadata
    s3.upload_file(file_src, space_name, save_as, ExtraArgs=extra_args)
