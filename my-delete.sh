#!/usr/bin/bash

set -euo pipefail

# エラーが発生した際の処理を行う関数
handle_error() {
    echo "エラーが発生しました。終了します。"
    exit 1
}

# エラー発生時にhandle_error関数を呼び出す設定
trap 'handle_error' ERR

instance_ids=($(aws ec2 describe-instances --filters "Name=key-name,Values=key-23745140" | grep -e "InstanceId" | awk -F'"' '{print $4}'))


# インスタンスIDのリストが空の場合、エラーとして処理
if [ ${#instance_ids[@]} -eq 0 ]; then
    echo "対象のインスタンスが見つかりませんでした。"
    exit 1
fi

# リスト内のインスタンスIDをもとに、削除
for id in "${instance_ids[@]}"; do
    aws ec2 terminate-instances --instance-ids $id
done


# バケットを空にする
aws s3 rm s3://report.aws-s23745140.com --recursive

# バケットを消去する
aws s3 rb s3://report.aws-s23745140.com