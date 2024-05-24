s3 = get_s3_connection()
response = s3.list_objects_v2(
    Bucket=os.getenv("s3_bucket_name"), Prefix="product_review/2024-05-24/"
)
if "Contents" in response:
    files = response["Contents"]
    for file in files:
        file_key = file["Key"]
        print(f"Fetching file: {file_key}")
        # 파일 가져오기
        # obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        # file_content = obj["Body"].read().decode("utf-8")  # 필요한 경우 디코딩
        # print(f"File content from {file_key}:\n{file_content}\n")
else:
    print("No files found")
