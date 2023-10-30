#!/usr/bin/bash

set -euo pipefail

instance_ids=($(aws ec2 describe-instances --filters "Name=key-name,Values=key-23745140" | grep -e "InstanceId" | awk -F'"' '{print $4}'))

# リスト内のインスタンスIDをもとに、削除
for id in "${instance_ids[@]}"; do
    echo "Instance ID: $id"
done

# バケットを空にする
aws s3 rm s3://report.aws-s23745140.com --recursive

# バケットを消去する
aws s3 rb s3://report.aws-s23745140.com