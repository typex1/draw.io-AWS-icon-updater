import sys
from lxml import etree
import datetime
import os
import time
import string

# alias to be created e.g. for bash:
# drawio-updater='python3 ~/git/CodeCommit/AWS-Services/Python/PythonXML/1-drawio-Updater_v2.py' 
# usage example to run in the background:
# drawio-updater ${PWD}/my-presentation.drawio > /dev/null 2>&1 &

changed=False
debug=False
sleepTime=2

if len(sys.argv) == 2:
        inputFile = sys.argv[1]
else:
        print ("usage: "+sys.argv[0]+" <draw.io filename>")
        exit(1)

def replaceWords(s):
    if s == "Cloudwatch 2": s= "CloudWatch"
    if s == "Auto Scaling2": s= "Auto Scaling"
    if s == "User": s= "Client"
    if s == "Users": s= "Clients"
    if s == "Sqs": s= "SQS"
    if s == "Sns": s= "SNS"
    if s == "Rds": s= "RDS"
    if s == "Bucket With Objects": s= "S3 Bucket"
    if s == "Eks": s= "Elastic Kubernetes Service"
    if s == "Ecs": s= "Elastic Container Service"
    if s == "Shape=connector": s= "x"
    if s == "Rule 3": s= "Rule"
    if s == "Auto Scaling2": s= "Auto Scaling"
    if s == "Ecr": s= "ECR"
    if s == "Permissions": s= "Policy"
    if s == "Table": s="DynamoDB Table"
    if s == "Api Gateway": s="API Gateway"
    return s

document = etree.parse(inputFile)
if document.xpath("/mxfile/diagram/mxGraphModel/root/mxCell"):
    print('draw.io file is not compressed, OK! Starting infinite loop - stop it with CTRL-c')
    pass
else:
    print('No mxCell entries exist. Is file compressed?')

# mxCell example entry containing resIcon:
# <mxCell id="5SKlDZPlu5r67-xeIEg6-1" value="Kinesis Data Steams"
#style="points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;gradientColor=#945DF2;gradientDirection=north;fillColor=#5A30B5;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;
#shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.kinesis_data_streams;" vertex="1" parent="Kydxhn0Gta8QPN5GZ85B-1">

# mxCell entry containing shape and NOT resourceIcon:
# <mxCell id="5SKlDZPlu5r67-xeIEg6-0" value="Lambda Function" style="outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#D05C17;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;
#shape=mxgraph.aws4.lambda_function;" vertex="1" parent="Kydxhn0Gta8QPN5GZ85B-1">

# infinite loop, stop it with CTRL-c:
while True:
    document = etree.parse(inputFile)
    for mxCell in document.xpath("/mxfile/diagram/mxGraphModel/root/mxCell"):
        id=mxCell.attrib['id']
        #print('value = '+mxCell.attrib['id'])
        if str(id) != "0" and str(id) != "1":
            #print('value = '+mxCell.attrib['id'])
            #print('keys() = '+str(mxCell.attrib.keys()))
            #print('values() = '+str(mxCell.attrib.values()))
            keys=str(mxCell.attrib.keys())
            values=str(mxCell.attrib.values())
            if 'style' in keys and 'shape' in values and 'image' not in values and 'gcp' not in values:
                for i in str(mxCell.attrib.values()).split(';'):
                    if 'resIcon' in i:
                        # example: resIcon=mxgraph.aws4.kinesis_data_streams;
                        name = i.split('.')[-1]
                        if mxCell.attrib['value']=='':
                            if(debug):
                                print('empty resIcon name = '+name)
                            #mxCell.attrib['value'] = name.replace('_',' ').capitalize()
                            mxCell.attrib['value'] = replaceWords(string.capwords(name.replace('_',' ')))#.replace(" ",'&lt;br&gt;')
                            changed=True
                    elif 'shape' in i and 'resourceIcon' not in i and 'connector' not in i:
                        name = i.split('.')[-1]
                        if mxCell.attrib['value']=='':
                            if(debug):
                                print('empty shape icon name = '+name)
                            #mxCell.attrib['value'] = name.replace('_',' ').capitalize()
                            mxCell.attrib['value'] = replaceWords(string.capwords(name.replace('_',' ')))#.replace(" ",'&lt;br&gt;')
                            changed=True

    root = document.getroot()

    # in case of test mode, write changes to different file:
    #f = open('drawio-mod.xml', 'w')

    if(changed):
        f = open(inputFile, 'w')
        f.write(etree.tostring(root, pretty_print=True).decode("utf-8"))
        f.close()
        if(debug):
            print("file updated")
        changed=False
    else:
        pass
        changed=False
        if(debug):
            print("file unchanged")
    time.sleep(sleepTime)
