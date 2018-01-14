from troposphere import Output, Ref, Template, Tags, Join
from troposphere.sns import Topic
import troposphere.ec2 as ec2


class Generator:

    def __init__(self):
        pass

    def __setup_template(self):
        """
        Produces a valid template instance which can then be print as json or yaml
        """
        template = Template()
        template.add_description("Service VPC - used for services")

        template.add_metadata({
            "Build": "development",
            "DependsOn": [],
            "Environment": "ApiDev",
            "Revision": "develop",
            "StackName": "ApiDev-Dev-VPC",
            "StackType": "InfrastructureResource",
            "TemplateBucket": "cfn-apidev",
            "TemplateName": "VPC",
            "TemplatePath": "ApiDev/Dev/VPC"
        })

        vpc = template.add_resource(
            ec2.VPC(
                "VPC",
                CidrBlock="10.0.0.0/16",
                EnableDnsHostnames="true",
                EnableDnsSupport="true",
                InstanceTenancy="default",
                Tags=self.__get_tags("ServiceVPC"),
            )
        )

        instance_sg = template.add_resource(
            ec2.SecurityGroup(
                "BastionSG",
                GroupDescription="Used for source/dest rules",
                Tags=self.__get_tags("VPC-Bastion-SG"),
                VpcId=Ref(
                    vpc
                )
            ),
        )

        cw_alarm_topic = template.add_resource(
            Topic(
                "CloudWatchAlarmTopic",
                TopicName="ApiDev-Dev-CloudWatchAlarms",
            )
        )

        dhcp_options = template.add_resource(
            ec2.DHCPOptions(
                "DhcpOptions",
                DomainName=Join(
                    "",
                    [
                        Ref("AWS::Region"),
                        ".compute.internal"
                    ]
                ),
                DomainNameServers=["AmazonProvidedDNS"],
                Tags=self.__get_tags("DhcpOptions"),
            )
        )

        gateway = template.add_resource(
            ec2.InternetGateway(
                "InternetGateway",
                Tags=self.__get_tags("InternetGateway")
            )
        )

        nat_emergency_topic = template.add_resource(
            Topic(
                "NatEmergencyTopic",
                TopicName="ApiDev-Dev-NatEmergencyTopic",
            )
        )

        vpc_dhcp_options_assoc = template.add_resource(
            ec2.VPCDHCPOptionsAssociation(
                "VpcDhcpOptionsAssociation",
                DhcpOptionsId=Ref(
                    dhcp_options
                ),
                VpcId=Ref(
                    vpc
                )
            )
        )

        vpc_gw_attachment = template.add_resource(
            ec2.VPCGatewayAttachment(
                "VpcGatewayAttachment",
                InternetGatewayId=Ref(
                    gateway
                ),
                VpcId=Ref(
                    vpc
                )
            )
        )

        vpc_network_acl = template.add_resource(
            ec2.NetworkAcl(
                "VpcNetworkAcl",
                Tags=self.__get_tags("NetworkAcl"),
                VpcId=Ref(
                    vpc
                )
            )
        )

        vpc_network_acl_rules = template.add_resource([
            ec2.NetworkAclEntry(
                "VpcNetworkAclInboundRulePublic443",
                CidrBlock="0.0.0.0/0",
                Egress="false",
                NetworkAclId=Ref(
                    vpc_network_acl
                ),
                PortRange=ec2.PortRange(
                    From="443",
                    To="443",
                ),
                Protocol="6",
                RuleAction="allow",
                RuleNumber=20001
            ),
            ec2.NetworkAclEntry(
                "VpcNetworkAclInboundRulePublic80",
                CidrBlock="0.0.0.0/0",
                Egress="false",
                NetworkAclId=Ref(
                    vpc_network_acl
                ),
                PortRange=ec2.PortRange(
                    From="80",
                    To="80",
                ),
                Protocol="6",
                RuleAction="allow",
                RuleNumber=20000
            ),
            ec2.NetworkAclEntry(
                "VpcNetworkAclOutboundRule",
                CidrBlock="0.0.0.0/0",
                Egress="true",
                NetworkAclId=Ref(
                    vpc_network_acl
                ),
                Protocol="-1",
                RuleAction="allow",
                RuleNumber=30000
            ),
            ec2.NetworkAclEntry(
                "VpcNetworkAclSsh",
                CidrBlock="127.0.0.1/32",
                Egress="false",
                NetworkAclId=Ref(
                    vpc_network_acl
                ),
                PortRange=ec2.PortRange(
                    From="22",
                    To="22",
                ),
                Protocol="6",
                RuleAction="allow",
                RuleNumber=10000
            )
        ])

        template.add_output([
            Output(
                "BastionSG",
                Value=Ref(instance_sg)
            ),
            Output(
                "CloudWatchAlarmTopic",
                Value=Ref(cw_alarm_topic)
            ),
            Output(
                "InternetGateway",
                Value=Ref(gateway)
            ),
            Output(
                "NatEmergencyTopicARN",
                Value=Ref(nat_emergency_topic)
            ),
            Output(
                "VPCID",
                Value=Ref(vpc)
            ),
            Output(
                "VPCName",
                Value=Ref("AWS::StackName")
            ),
            Output(
                "VpcNetworkAcl",
                Value=Ref(vpc_network_acl)
            )

        ])

        return template

    def __get_tags(self, name):
        """Generates common tags with the exception of the name parameter """
        return Tags(
            Environment="ApiDev",
            Name="ApiDev-Dev-"+name,
            Owner="Foo industries",
            Service="ServiceVPC",
            VPC="Dev",
        )

    def to_json(self):
        return self.__setup_template().to_json()

    def to_yaml(self):
        return self.__setup_template().to_json()
