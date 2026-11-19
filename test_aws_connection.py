import boto3

def test_connection():
    try:
        # Connect using the configured AWS credentials
        session = boto3.Session()
        sts = session.client("sts")
        identity = sts.get_caller_identity()

        print("\n========================================")
        print(" SUCCESS: Connected to AWS Account!")
        print("========================================")
        print("Account ID  :", identity.get("Account"))
        print("User ARN    :", identity.get("Arn"))
        print("User Name   :", identity.get("Arn").split("/")[-1])
        print("========================================\n")
        return True

    except Exception as error:
        print("\n========================================")
        print(" FAILED: Could not connect to AWS")
        print("========================================")
        print("Error details:", error)
        print("\nTip: Run 'aws configure' in terminal to enter your AWS Access Key and Secret.")
        print("========================================\n")
        return False

if __name__ == "__main__":
    test_connection()
