from s3_Utility import uploadFileToS3

bucket_name = "brrrr-ai-photos"
file_path = "house_drawing.jpg"
key = "uploads/house_drawing.jpg"

uploadFileToS3(file_path, bucket_name, key)