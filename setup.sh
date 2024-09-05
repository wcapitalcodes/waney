mkdir -p ~/.streamlit/

echo "\
openai_key="sk-proj-RAg2Per3rZ4DHUQzRWkcT3BlbkFJBuc9VXzjtydBaQ9XbTBC"\n\
[connections.gsheets]\n\
spreadsheet = "https://docs.google.com/spreadsheets/d/1gn1AtCZ5AZQ9qPrdBeD-fE0oYgQSVOm2we7GFsikbAk/edit?gid=0#gid=0"\n\
type = "service_account"\n\
project_id = "wani-chat"\n\
private_key_id = "cb8d0f897dc4244f97f48e5e1856bd1533c12a86"\n\
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDPbIlE92b9fEw0\n4QfwDqDgFy01JTE9ijzqVkibaPMesvDXb4AlkE7ceF4hyYrpWDexLHxu64sZn7/i\njW+OnEHGyinV00VbKdITuQ2Z88HRj1cFSsXzJ8TlyxfTJLlRTW+mqprhMw+wnvxI\nrf5GAry5ES70JsEAKG2YdEAv8DBjY0tJe7TnxAgEHoQrOP+mHa4EZkyYc1HtgAo8\n2w8ezqIBjCD4zZ23yWjN1p2uLh2u9wMb7FYz8i7E/uEkBXGgMwmQNk9n0Fr40U2h\ni13BaShGtFtpQGgx4bD6WlX/yjIJPCEVVW+60q8u1JVt7bcsEJ/iHhB7c+xjFclX\nkYWcv40tAgMBAAECggEAF9cdNeCLpVHefmto2qYLxoXTa9rQ/IZBdxugr8ARxXMC\nrHhDzc12yu9IvnBoN2asy//Vc3g+Hh1W1Ca2bjk2dC8zPMDSJWa6nwqzbgDuw3PK\nqDCObOKixlif7eQ4KoiQbyMHtx+Dy6SSUZYx9gEFiO3ZLDWyFB8Rbaba48ejACEp\n156PzcY+DINg2xHQxMPGtXaLbOUxrMJfKvPScQjzEBnmShGJlKhzte8lmQLkKcIk\nFZf4VrIsB6C540OsS3LungYR45cgvxM4NGvk4iHUBk6Dbe5bfOOEFyOiabkBycb/\nVUOPchnkCUrVaisY3pv2Qid92IcywGyU4JM33YVq4QKBgQD5nU9bUr8NE1tNiOax\nGPjw8CxAD5LlJl8gjYH4vSYHCn3/nmjley0mzakSVoiYC06142KwQ2muuGoSFrfm\niL40yrbd2y5oRyux/pmb7A866uxSuowsHDPOuUPig5UHiHGkTXN+W5iNV2A3I+ma\n66422wcvYZVcP5/hNk/oVlwUkQKBgQDUuu0sJffrKYnq2M/1dEOiAEBXFcu5mtwy\nDBinSTE+Msl3FYJz0PEBq0BnzfgrkjZVsUEbdS4xCdHY5CkkamRCvCDYqFkAo2hs\nbNF1xY68dwly9W+wBQ9W7FGee38nP20SrzZba4TCyxrkmhqS6CU0s8OYsW3A+Opq\n79q04xsM3QKBgCwyYl61JAbYqo3r84zf8xQWMn+VQlk4lhdZdu3n79fHT8/26HPZ\nf4EjYRBSKhVhyyoBfPPgu9Gn7YAObblv9N28FuzpZiooj+AQSHqHLZstBXMQfMlC\npRmxTAfLbJPM4PJKlGyHI1fDZNHelfpMSKiF15vYF24iBdkGmNd2kw9BAoGAWYr9\nPjIVMxVfCk2M66KuvUghzQZNpKi8uwxAbFnwsl+qUcfqC1oNuEgfahJWvfBjkppz\n71zZvqaFgCg58SwfW7/Yi5oBLLWbxNfhKxOnS0lH3u3Uv2DB3jLHAFC3awvVm6HI\n3Z5aWawoe8UqHmA9GPv5/xHgQvQDqFOh2bYmsrkCgYBfraxnrYS/pLx6oy4swbV0\nCJwWBnlATBvxnGNbBS/9SczluLaruc85AKXOnsGNyJf8L3iRXhVKmDWZLVIuhq3i\nJr13AfzOcVHjS5WqxSoCSdhUPbKV9QM5PQC76Hn+ofMbq98d0mjG+uoop8wmuNqa\npyx4W5nla2a+3cYYSwdDKg==\n-----END PRIVATE KEY-----\n"\n\
client_email = "wanichat-serviceaccount-editor@wani-chat.iam.gserviceaccount.com"\n\
client_id = "100221046789518599855"\n\
auth_uri = "https://accounts.google.com/o/oauth2/auth"\n\
token_uri = "https://oauth2.googleapis.com/token"\n\
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"\n\
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/wanichat-serviceaccount-editor%40wani-chat.iam.gserviceaccount.com"\n\
universe_domain="googleapis.com"\n\
[mixpanel]\n\
token="2f1f39d0f6ffd5d3c068f25a9972386c"\n\
" > ~/.streamlit/secrets.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml