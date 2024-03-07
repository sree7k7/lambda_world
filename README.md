# lambda world

## To bootstrap AWS CDK in all regions
create a file, bootstrap.sh, execute sh bootstrap.sh
```
#!/bin/bash

# Get the list of all available regions
regions=$(aws ec2 describe-regions --query "Regions[].{Name:RegionName}" --output text)

# Run cdk bootstrap for each region
for region in $regions
do
  npx cdk bootstrap aws://ACCOUNT_ID/$region
done
```

> **Note:** pass account id for *ACCOUNT_ID*

