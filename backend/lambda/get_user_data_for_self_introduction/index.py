import json
import logging
import os

import boto3
from boto3.dynamodb.conditions import Key

# Loggerの初期設定
## 参考: https://www.sejuku.net/blog/23149
FORMAT = '%(asctime)s : %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)  # フォーマットの設定
LOGGER = logging.getLogger(__name__)  # loggingではなくLoggerを使うように設定
LOGGER.setLevel(logging.DEBUG)

# 環境変数からテーブル名を取得
## 参考: https://dev.classmethod.jp/articles/aws-lambda-env-variables/
USER_TABLE_NAME = os.environ.get("USER_TABLE_NAME")
# boto3でDynamoDBを操作するためのリソースを作成
## 参考: https://dev.classmethod.jp/articles/dynamodb-query-use-filterexpression/
DYNAMODB = boto3.resource('dynamodb')
# DynamoDBのテーブルを操作するためのオブジェクトを作成
USER_TABLE = DYNAMODB.Table(USER_TABLE_NAME)


def handler(event, context):
    # レスポンスの雛形
    response = {
        'statusCode': 200, # 成功時は200
        'body': '', # レスポンスボディの中身。最初は空
        'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        },
    }

    # 途中でエラーが発生した場合でも
    # 最後まで処理が進むようにtry-exceptで囲む
    try:
        ############################### [メイン処理] ###############################
        # クエリストリングから取得した値を変数へ格納
        query_val = event['queryStringParameters']['id']
        LOGGER.info("query_val: {0}".format(query_val))

        # DynamoDBテーブルからデータ取得するクエリを実行
        ## 参考: https://dev.classmethod.jp/articles/dynamodb-query-use-filterexpression/
        query_response = USER_TABLE.query(KeyConditionExpression=Key('id').eq(query_val))[
            "Items"
        ]
        LOGGER.info("query_response: {0}".format(query_response))

        # レスポンスの作成
        ## json モジュールの dumps 関数を使って、PythonオブジェクトをJSON文字列に変換する
        ## 参考: https://1-notes.com/python-json-encode-and-decode/
        response['body'] = json.dumps(query_response)
        response['statusCode'] = 200
    except Exception as err:
        # エラー時のレスポンスを作成する
        LOGGER.error("Error Message: {0}".format(err))

        # レスポンスの作成
        ## json モジュールの dumps 関数を使って、PythonオブジェクトをJSON文字列に変換する
        ## 参考: https://1-notes.com/python-json-encode-and-decode/
        response['body'] = json.dumps("Error Message: {0}".format(err))
        response['statusCode'] = 500
    return response


