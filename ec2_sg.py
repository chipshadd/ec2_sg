#!/usr/bin/python2
DOCUMENTATION = '''
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
'''




import json
from ansible.module_utils.basic import AnsibleModule
try: 
	import boto3
	from botocore.exceptions import ClientError, EndpointConnectionError
	HAS_BOTO = True
except ImportError:
	HAS_BOTO = False



def set_SG(instance, groups, ec2):	
	server = ec2.Instance(instance)
	server.modify_attribute(Groups=groups)

def manage_SG(instance, groups, state, ec2):
	server = ec2.Instance(instance)
	group_list = [group['GroupId'] for group in server.security_groups]
	for i in groups:
		if state == "add":
			if i.strip() not in group_list:
				group_list.append(i)
		if state == "remove":
			if i.strip() in group_list:
				group_list.remove(i)
	server.modify_attribute(Groups=group_list)

def get_Instances(ec2, filters):
	instanceArray = []
	try:
		

def main():
	argument_spec = dict(
			groups = dict(type='list'),
			instanceid = dict(required=True, type='list'),
			region = dict(default='us-west-2',type='str'),
			filters = dict(type='dict'),
			ip = dict(type='list'),
			action = dict(choices=['add', 'remove', 'set'], required=True, type='str')
	)

	module = AnsibleModule(argument_spec=argument_spec,mutually_exclusive=[['instanceid','ip'],['instanceid','filter'],['ip','filter']])
	groups = module.params.get('groups')
	instanceid = module.params.get('instanceid')
	filters = module.params.get('filters')
	region = module.params.get('region')
	ip = module.params.get('ip')
	state = module.params.get('action')
	#Gotta have boto
	if not HAS_BOTO:
		module.fail_json(msg="You need boto3")
	
	#Mandatory parameters
	if not (instanceid or filters):
		module.fail_json(msg="You must provide instanceID(s) or a filter")
	if not state:
		module.fail_json(msg="State argument must be defined")
	
	#Connect to AWS
	ec2 = boto3.resource('ec2', region_name=region)
	if ip:
		module.fail_json(msg="IP argument not enabled yet.")
	if filters:
		module.fail_json(msg="Filters argument not enabled yet.")

	if state == "set":
		for instance in instanceid:
			set_SG(instance.strip(), groups, ec2)
	else:
		for instance in instanceid:
			manage_SG(instance.strip(), groups, state, ec2)
	module.exit_json(msg="Done")
if __name__ == '__main__':
	main()

	
		
