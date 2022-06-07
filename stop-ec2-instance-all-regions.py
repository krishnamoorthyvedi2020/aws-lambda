def lambda_handler(event, context):
    
    import boto3
    
    region_names=[]
    # List all regions
    
    client = boto3.client('ec2')
    region_names = [region['RegionName'] for region in client.describe_regions()['Regions']]
    print("List of region names : "+ str(region_names))
    
    #loop through each region, stop instance if running based on instance id    
    for r in region_names:

        #get list of running instances in particular region
        
        running_instances = []
        ec2client = boto3.client('ec2',region_name= r)
        response = ec2client.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if instance['State']['Name'] == 'running':
                  x = (instance["InstanceId"])
                  #print(x)
                  running_instances.append(x)
        #print("Running ins : "+str(running_instances))
        
        #for stop_ec2_id in running_instances:
        if len(running_instances)>0:
            ec2client.stop_instances(InstanceIds=running_instances)
            print('stopped your instances: ' + str(running_instances))
