import boto3
import botocore.exceptions


class SsmParameterStore:
    def __init__(self, region: str = None):
        self.region = (
            region or boto3.Session().region_name
        )  # if region not specified, will set region as region of the EC2 instance
        self.ssm = boto3.client("ssm", region_name=self.region)

    def get_parameter(self, parameter_name: str) -> str:
        try:
            response = self.ssm.get_parameter(Name=parameter_name, WithDecryption=True)
            return response["Parameter"]["Value"]
        except botocore.exceptions.ClientError as e:
            print(f"Error fetching parameter '{parameter_name}': {e}")
            return None  # Return None instead of raising an exception
