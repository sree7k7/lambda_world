#!/bin/bash

# Get the list of all available regions
regions=$(aws ec2 describe-regions --query "Regions[].{Name:RegionName}" --output text)

# Run cdk bootstrap for each region
for region in $regions
do
  npx cdk bootstrap aws://$1/$region
done