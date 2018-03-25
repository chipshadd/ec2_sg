Prequisites:
 - Boto3

Todo:
 - Manage instances by a filter
 - Manage instances by IPs

---
module: ec2_sg
short_description: Manage instance security groups
description:
	- Set, add, or remove security group(s) from instance(s).
options:
	groups:
		description:
			- A comma separated list of security groups that will either be applied to the instance(s) depending on the C(action) parameter.
		required: true
		default: null
	instanceid:
		description:
			- A comma separated list of instance IDs for which to apply the list of security groups to.
		required: true
		default: null
	region:
		description:
			- The AWS region in which the EC2 resources exist.
		required: false
		default: us-west-2
	action:
		description:
			- If C(set), the specified list of security groups will be applied to the specified list of instances. This will overwrite all of the security groups currently on the instance(s)
			- If C(add), the specified list of security groups will be added to the specified list of instance(s).
			- If C(remove), the specified list of security groups will be remove from the specified list of instance(s).
		required: true
		choices: [set, add, remove]

