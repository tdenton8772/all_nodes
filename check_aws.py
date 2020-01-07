#! /usr/bin/python

import boto3
import json
client = boto3.client('ec2')

instances = []
VPC_ID = "vpc-0bd1dc1d2cae6b8a3"
add_per_student = 2

ip_addresses = []

def check_addresses():
	ec2 = boto3.resource('ec2')

	# Get information for all running instances
	running_instances = ec2.instances.filter(Filters=[
	{'Name': 'instance-state-name',
    'Values': ['running']},
	{'Name': 'vpc-id',
	'Values': [VPC_ID]}])

  	for instance in running_instances:
		ip_addresses.append(instance.private_ip_address)

	return ip_addresses

def create_students(ip_addresses):
	students = {}
	num_students = len(ip_addresses) / add_per_student
	for x in range(0, num_students):
		students[str(x+1)] = ip_addresses[x*add_per_student:(x+1)*add_per_student]
	return students

def write_nodes(students):
	with open("all_nodes.json", "w+") as f:
		j_students = json.dumps(students, indent=4)
		f.write(j_students)

if __name__ == "__main__":
	ip_addresses = check_addresses()
	students = create_students(ip_addresses)
	write_nodes(students)
