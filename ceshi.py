import requests
def get_access_token(client_id,client_secret,code):
    # 访问Token令牌
    TOKEN_URL = 'https://iam.gongshu.gov.cn/bam-protocol-service/oauth2/getToken'
    params={
            "code": code,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',

            }
    headers = {
            "Accept":"application/json",
            "Content-Type":"application/x-www-form-urlencoded",
            "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
    res = requests.post(url = TOKEN_URL,data=params,params = {"state":1},headers=headers)
    return res
if __name__ == "__main__":
    client_id= "qllsj"
    client_secret = "5ca6d687b49f4a1cae1aeaa4aa286991"
    code = "73f87e8e1f034828c21026288ec12ca7"
    res =get_access_token(client_id,client_secret,code)
    print(res)
